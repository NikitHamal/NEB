package com.neb.ians.ui.screens.auth

import android.app.Activity
import android.content.Context
import android.content.ContextWrapper
import android.content.Intent
import android.net.Uri
import androidx.browser.customtabs.CustomTabsIntent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.credentials.CredentialManager
import androidx.credentials.CustomCredential
import androidx.credentials.GetCredentialRequest
import androidx.credentials.exceptions.GetCredentialCancellationException
import androidx.credentials.exceptions.GetCredentialException
import androidx.credentials.exceptions.NoCredentialException
import com.google.android.libraries.identity.googleid.GetGoogleIdOption
import com.google.android.libraries.identity.googleid.GetSignInWithGoogleOption
import com.google.android.libraries.identity.googleid.GoogleIdTokenCredential
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.OAuthResult
import com.neb.ians.ui.screens.onboarding.Reveal
import androidx.compose.material.icons.outlined.Close
import com.neb.ians.ui.theme.Poppins
import com.neb.ians.ui.theme.LocalNebAuthPalette
import com.neb.ians.ui.theme.nebAuthPalette
import kotlinx.coroutines.launch

private tailrec fun Context.findActivity(): Activity? = when (this) {
    is Activity -> this
    is ContextWrapper -> baseContext.findActivity()
    else -> null
}

private const val OAUTH_PREFS = "nebians_oauth_prefs"
private const val REQUEST_CODE_OAUTH_CUSTOM_TAB = 9041
private val GOOGLE_DIRECT_OAUTH_URL =
    "https://accounts.google.com/o/oauth2/v2/auth" +
        "?client_id=" + AuthRepository.GOOGLE_SERVER_CLIENT_ID +
        "&redirect_uri=https://nebians.consica.com.np/auth/google/callback/" +
        "&response_type=code" +
        "&scope=openid+email+profile" +
        "&prompt=select_account" +
        "&access_type=online" +
        "&state=mobile_google"
private const val GITHUB_DIRECT_OAUTH_URL =
    "https://github.com/login/oauth/authorize" +
        "?client_id=" + AuthRepository.GITHUB_CLIENT_ID +
        "&redirect_uri=" + AuthRepository.GITHUB_REDIRECT_URI +
        "&scope=read:user,user:email" +
        "&state=mobile_github"

private fun isTrueUserCancellation(e: GetCredentialCancellationException): Boolean {
    val msg = (e.message ?: "").lowercase()
    if (msg.isBlank()) return true
    if ("reauth" in msg || "28444" in msg || "developer" in msg || "10:" in msg || "unregistered" in msg) {
        return false
    }
    return "cancel" in msg || "12501" in msg || "user" in msg
}

@Suppress("DEPRECATION")
private fun isNativeGoogleIdConfigured(context: Context): Boolean {
    return runCatching {
        // Clear any legacy sticky disable flag from earlier builds so native Credential Manager is always tried.
        val prefs = context.getSharedPreferences(OAUTH_PREFS, Context.MODE_PRIVATE)
        val disableKey = "cred_mgr_disabled_v${com.neb.ians.BuildConfig.VERSION_CODE}"
        if (prefs.contains(disableKey)) {
            prefs.edit().remove(disableKey).apply()
        }
        val registered = com.neb.ians.BuildConfig.GOOGLE_ANDROID_CERT_HASHES
            .split(",")
            .map { it.trim().replace(":", "").lowercase() }
            .filter { it.length == 40 || it.length == 64 }
            .toSet()
        if (registered.isEmpty()) return true
        val pm = context.packageManager
        val sigs = if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.P) {
            val info = pm.getPackageInfo(context.packageName, android.content.pm.PackageManager.GET_SIGNING_CERTIFICATES).signingInfo
            if (info == null) emptyArray()
            else if (info.hasMultipleSigners()) info.apkContentsSigners
            else info.signingCertificateHistory
        } else {
            pm.getPackageInfo(context.packageName, android.content.pm.PackageManager.GET_SIGNATURES).signatures ?: emptyArray()
        }
        if (sigs.isEmpty()) return true
        val sha1Digest = java.security.MessageDigest.getInstance("SHA-1")
        val sha256Digest = java.security.MessageDigest.getInstance("SHA-256")
        sigs.any { sig ->
            val bytes = sig.toByteArray()
            val sha1 = sha1Digest.digest(bytes).joinToString("") { "%02x".format(it) }
            val sha256 = sha256Digest.digest(bytes).joinToString("") { "%02x".format(it) }
            sha1 in registered || sha256 in registered
        }
    }.getOrDefault(true)
}

private fun extractGoogleIdToken(credential: androidx.credentials.Credential): String? = when {
    credential is GoogleIdTokenCredential -> credential.idToken
    credential is CustomCredential &&
        credential.type == GoogleIdTokenCredential.TYPE_GOOGLE_ID_TOKEN_CREDENTIAL ->
        runCatching { GoogleIdTokenCredential.createFrom(credential.data).idToken }.getOrNull()
    else -> null
}

private suspend fun requestGoogleIdTokenNatively(activityContext: Activity): String? {
    val credentialManager = CredentialManager.create(activityContext)
    val serverClientId = AuthRepository.GOOGLE_SERVER_CLIENT_ID
    // Tier 1: Bottom-sheet One Tap credential picker (GetGoogleIdOption)
    try {
        val oneTapOption = GetGoogleIdOption.Builder()
            .setFilterByAuthorizedAccounts(false)
            .setServerClientId(serverClientId)
            .setAutoSelectEnabled(false)
            .build()
        val result = credentialManager.getCredential(
            request = GetCredentialRequest.Builder().addCredentialOption(oneTapOption).build(),
            context = activityContext
        )
        extractGoogleIdToken(result.credential)?.takeIf { it.isNotBlank() }?.let { return it }
    } catch (e: GetCredentialCancellationException) {
        if (isTrueUserCancellation(e)) throw e
    } catch (_: NoCredentialException) {
        // Proceed to Tier 2 explicit Sign in with Google dialog
    } catch (_: GetCredentialException) {
        // Proceed to Tier 2 explicit Sign in with Google dialog
    } catch (_: Exception) {
        // Proceed to Tier 2 explicit Sign in with Google dialog
    }

    // Tier 2: Explicit "Sign in with Google" account chooser modal (GetSignInWithGoogleOption)
    val signInOption = GetSignInWithGoogleOption.Builder(serverClientId).build()
    val fallbackResult = credentialManager.getCredential(
        request = GetCredentialRequest.Builder().addCredentialOption(signInOption).build(),
        context = activityContext
    )
    return extractGoogleIdToken(fallbackResult.credential)?.takeIf { it.isNotBlank() }
}

@Composable
fun LoginScreen(
    onNavigateToEmailAuth: () -> Unit,
    onClose: (() -> Unit)? = null,
    onNavigateToHome: (() -> Unit)? = null,
    onNavigateToOnboarding: (() -> Unit)? = null,
    authRepository: AuthRepository? = null
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val isDark = LocalNebAuthPalette.current.isDark

    var isLoading by remember { mutableStateOf(false) }
    var loadingProvider by remember { mutableStateOf<String?>(null) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var activeLegalSheet by remember { mutableStateOf<LegalSheetType?>(null) }
    var customTabsSession by remember { mutableStateOf<androidx.browser.customtabs.CustomTabsSession?>(null) }

    androidx.compose.runtime.LaunchedEffect(authRepository) {
        authRepository?.authState?.collect { state ->
            if (state is com.neb.ians.data.repository.AuthState.Authenticated) {
                isLoading = false
                loadingProvider = null
                if (state.isProfileComplete) onNavigateToHome?.invoke()
                else onNavigateToOnboarding?.invoke()
            }
        }
    }

    val customTabsPkg = remember(context) {
        runCatching {
            val preferred = listOf(
                "com.android.chrome",
                "com.brave.browser",
                "com.microsoft.emmx",
                "com.sec.android.app.sbrowser",
                "org.mozilla.firefox"
            )
            androidx.browser.customtabs.CustomTabsClient.getPackageName(context, preferred, true)
                ?: androidx.browser.customtabs.CustomTabsClient.getPackageName(context, null)
        }.getOrNull()
    }

    androidx.compose.runtime.DisposableEffect(customTabsPkg) {
        val pkg = customTabsPkg
        val appCtx = context.applicationContext
        var boundConn: androidx.browser.customtabs.CustomTabsServiceConnection? = null
        if (!pkg.isNullOrBlank()) {
            val conn = object : androidx.browser.customtabs.CustomTabsServiceConnection() {
                override fun onCustomTabsServiceConnected(
                    name: android.content.ComponentName,
                    client: androidx.browser.customtabs.CustomTabsClient
                ) {
                    runCatching {
                        client.warmup(0L)
                        val session = client.newSession(null)
                        val githubBundle = android.os.Bundle().apply {
                            putParcelable(
                                androidx.browser.customtabs.CustomTabsService.KEY_URL,
                                Uri.parse(GITHUB_DIRECT_OAUTH_URL)
                            )
                        }
                        session?.mayLaunchUrl(
                            Uri.parse(GOOGLE_DIRECT_OAUTH_URL),
                            null,
                            listOf(githubBundle)
                        )
                        customTabsSession = session
                    }
                }
                override fun onServiceDisconnected(name: android.content.ComponentName?) {
                    customTabsSession = null
                }
            }
            if (runCatching { androidx.browser.customtabs.CustomTabsClient.bindCustomTabsService(appCtx, pkg, conn) }.getOrDefault(false)) {
                boundConn = conn
            }
        }
        onDispose {
            boundConn?.let { runCatching { appCtx.unbindService(it) } }
        }
    }

    @Suppress("DEPRECATION")
    fun launchBrowserOAuth(provider: String) {
        val url = if (provider == "google") GOOGLE_DIRECT_OAUTH_URL else GITHUB_DIRECT_OAUTH_URL
        val uri = Uri.parse(url)
        try {
            val dm = context.resources.displayMetrics
            val sheetHeightPx = (dm.heightPixels * 0.88f).toInt().coerceAtLeast(480)
            val session = customTabsSession
            val builder = if (session != null) CustomTabsIntent.Builder(session) else CustomTabsIntent.Builder()
            val customTabsIntent = builder
                .setShareState(CustomTabsIntent.SHARE_STATE_OFF)
                .setShowTitle(true)
                .setUrlBarHidingEnabled(true)
                .setToolbarCornerRadiusDp(24)
                .setCloseButtonPosition(CustomTabsIntent.CLOSE_BUTTON_POSITION_END)
                .setColorScheme(if (isDark) CustomTabsIntent.COLOR_SCHEME_DARK else CustomTabsIntent.COLOR_SCHEME_LIGHT)
                .setInitialActivityHeightPx(sheetHeightPx, CustomTabsIntent.ACTIVITY_HEIGHT_DEFAULT)
                .build()
            if (!customTabsPkg.isNullOrBlank()) {
                customTabsIntent.intent.setPackage(customTabsPkg)
            }
            val activity = context.findActivity()
            if (activity != null) {
                customTabsIntent.intent.data = uri
                activity.startActivityForResult(customTabsIntent.intent, REQUEST_CODE_OAUTH_CUSTOM_TAB)
            } else {
                customTabsIntent.launchUrl(context, uri)
            }
        } catch (_: Exception) {
            try {
                context.startActivity(Intent(Intent.ACTION_VIEW, uri))
            } catch (_: Exception) {
                errorMessage = "No browser available for sign-in."
            }
        }
    }

    fun launchOAuth(provider: String) {
        if (isLoading) return
        errorMessage = null
        if (provider == "google" && authRepository != null && isNativeGoogleIdConfigured(context)) {
            isLoading = true
            loadingProvider = "google"
            scope.launch {
                try {
                    val activityContext = context.findActivity() ?: run {
                        launchBrowserOAuth("google")
                        return@launch
                    }
                    val idToken = requestGoogleIdTokenNatively(activityContext)
                    if (!idToken.isNullOrBlank()) {
                        when (val authResult = authRepository.signInWithGoogle(idToken)) {
                            is OAuthResult.Success -> {
                                if (authResult.isNewUser) onNavigateToOnboarding?.invoke()
                                else onNavigateToHome?.invoke()
                            }
                            is OAuthResult.Failure -> errorMessage = authResult.message
                        }
                    } else {
                        launchBrowserOAuth("google")
                    }
                } catch (e: GetCredentialCancellationException) {
                    if (!isTrueUserCancellation(e)) {
                        launchBrowserOAuth("google")
                    }
                } catch (_: GetCredentialException) {
                    launchBrowserOAuth("google")
                } catch (_: Exception) {
                    launchBrowserOAuth("google")
                } finally {
                    isLoading = false
                    loadingProvider = null
                }
            }
            return
        }

        isLoading = true
        loadingProvider = provider
        try {
            launchBrowserOAuth(provider)
        } finally {
            isLoading = false
            loadingProvider = null
        }
    }

    val palette = nebAuthPalette(isDark)
    val screenBg = palette.page

    BoxWithConstraints(
        modifier = Modifier
            .fillMaxSize()
            .background(screenBg)
            .statusBarsPadding()
            .navigationBarsPadding()
    ) {
        val heroHeight = (maxHeight * 0.44f).coerceIn(260.dp, 400.dp)

        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(bottom = 20.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Spacer(modifier = Modifier.height(12.dp))

            AuthHero(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(heroHeight),
                dark = isDark
            )

            Spacer(modifier = Modifier.height(8.dp))

            Reveal(active = true, index = 3) {
                Text(
                    text = buildAnnotatedString {
                        append("Welcome to ")
                        pushStyle(SpanStyle(color = palette.brand, fontWeight = FontWeight.SemiBold))
                        append("NEBians")
                        pop()
                    },
                    fontFamily = Poppins,
                    fontWeight = FontWeight.SemiBold,
                    fontSize = 28.sp,
                    letterSpacing = (-0.5).sp,
                    color = palette.ink,
                    textAlign = TextAlign.Center
                )
            }

            AnimatedVisibility(
                visible = !errorMessage.isNullOrBlank(),
                enter = fadeIn() + expandVertically(),
                exit = fadeOut() + shrinkVertically()
            ) {
                Text(
                    text = errorMessage ?: "",
                    fontFamily = Poppins,
                    fontWeight = FontWeight.Medium,
                    fontSize = 13.sp,
                    color = MaterialTheme.colorScheme.error,
                    textAlign = TextAlign.Center,
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(start = 24.dp, end = 24.dp, top = 12.dp)
                )
            }

            Spacer(modifier = Modifier.height(28.dp))

            Reveal(active = true, index = 5, rise = 40.dp, modifier = Modifier.fillMaxWidth()) {
                AuthActionButtons(
                    isDark = isDark,
                    isLoading = isLoading,
                    loadingProvider = loadingProvider,
                    onGoogleClick = { launchOAuth("google") },
                    onGitHubClick = { launchOAuth("github") },
                    onEmailClick = onNavigateToEmailAuth,
                    onTermsClick = { activeLegalSheet = LegalSheetType.TERMS },
                    onPrivacyClick = { activeLegalSheet = LegalSheetType.PRIVACY }
                )
            }
        }

        if (onClose != null) {
            androidx.compose.material3.IconButton(
                onClick = onClose,
                modifier = Modifier
                    .align(Alignment.TopEnd)
                    .padding(top = 4.dp, end = 4.dp)
            ) {
                androidx.compose.material3.Icon(
                    androidx.compose.material.icons.Icons.Outlined.Close,
                    contentDescription = "Close",
                    tint = palette.ink
                )
            }
        }

        AuthLegalSheet(
            sheetType = activeLegalSheet,
            onDismiss = { activeLegalSheet = null },
            isDark = isDark
        )
    }
}
