package com.neb.ians.ui.screens.auth

import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.background
import androidx.compose.ui.draw.clip
import androidx.compose.runtime.getValue
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.theme.nebFastEffectsSpec
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.ClickableText
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Mail
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.R
import com.neb.ians.ui.theme.Poppins
import com.neb.ians.ui.theme.nebAuthPalette
import com.neb.ians.util.TactileType
import com.neb.ians.util.rememberTactileFeedback
import com.neb.ians.ui.components.NebLoaderSize
import com.neb.ians.ui.components.NebLoader

@Composable
fun AuthActionButtons(
    isDark: Boolean,
    isLoading: Boolean,
    loadingProvider: String?,
    onGoogleClick: () -> Unit,
    onGitHubClick: () -> Unit,
    onEmailClick: () -> Unit,
    onTermsClick: () -> Unit,
    onPrivacyClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val tactile = rememberTactileFeedback()
    val palette = nebAuthPalette(isDark)

    /**
     * Terms and Privacy are the brand blue, not ink. They are the only two links
     * on this screen, and a link that looks like the surrounding sentence is a
     * link nobody taps.
     */
    val linkColor = palette.brand

    /** The mail glyph is chrome, not a link, so it stays on the ink ramp. */

    Column(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        // Three equal pills, each one a pressable surface: scale spring and a haptic on touch.
        AuthProviderButton(
            label = "Continue with Google",
            enabled = !isLoading,
            loading = isLoading && loadingProvider == "google",
            container = if (isDark) Color(0xFF2A2B33) else Color(0xFFF1F1F3),
            content = if (isDark) Color(0xFFE4E1E9) else Color(0xFF1F1F21),
            tag = "google_login_button",
            onClick = onGoogleClick
        ) {
            Icon(
                painter = painterResource(id = R.drawable.ic_google),
                contentDescription = null,
                tint = Color.Unspecified,
                modifier = Modifier.size(22.dp)
            )
        }

        Spacer(modifier = Modifier.height(12.dp))

        AuthProviderButton(
            label = "Continue with GitHub",
            enabled = !isLoading,
            loading = isLoading && loadingProvider == "github",
            container = if (isDark) Color(0xFFE4E1E9) else Color(0xFF101012),
            content = if (isDark) Color(0xFF101012) else Color.White,
            tag = "github_login_button",
            onClick = onGitHubClick
        ) {
            Icon(
                painter = painterResource(id = R.drawable.ic_github),
                contentDescription = null,
                tint = if (isDark) Color(0xFF101012) else Color.White,
                modifier = Modifier.size(22.dp)
            )
        }

        Spacer(modifier = Modifier.height(12.dp))

        AuthProviderButton(
            label = "Continue with Email",
            enabled = !isLoading,
            loading = false,
            container = palette.brandSoft,
            content = palette.brand,
            tag = "email_login_button",
            onClick = onEmailClick
        ) {
            Icon(
                imageVector = Icons.Outlined.Mail,
                contentDescription = null,
                modifier = Modifier.size(22.dp),
                tint = palette.brand
            )
        }

        Spacer(modifier = Modifier.height(18.dp))

        // 4. Terms & Privacy Disclaimer (Poppins 500 normal, Poppins 600 bold links)
        val termsAnnotatedString = buildAnnotatedString {
            append("By continuing, you agree to our ")

            val termsStart = length
            append("Terms of Service")
            val termsEnd = length
            addStyle(
                style = SpanStyle(
                    fontFamily = Poppins,
                    color = linkColor,
                    fontWeight = FontWeight.SemiBold // Poppins 600
                ),
                start = termsStart,
                end = termsEnd
            )
            addStringAnnotation(
                tag = "TERMS",
                annotation = "terms",
                start = termsStart,
                end = termsEnd
            )

            append(" & ")

            val privacyStart = length
            append("Privacy Policy")
            val privacyEnd = length
            addStyle(
                style = SpanStyle(
                    fontFamily = Poppins,
                    color = linkColor,
                    fontWeight = FontWeight.SemiBold // Poppins 600
                ),
                start = privacyStart,
                end = privacyEnd
            )
            addStringAnnotation(
                tag = "PRIVACY",
                annotation = "privacy",
                start = privacyStart,
                end = privacyEnd
            )
        }

        ClickableText(
            text = termsAnnotatedString,
            style = MaterialTheme.typography.bodySmall.copy(
                fontFamily = Poppins,
                fontWeight = FontWeight.Medium, // Poppins 500
                fontSize = 12.sp,
                lineHeight = 18.sp,
                textAlign = TextAlign.Center,
                color = if (isDark) Color(0xFF9B9BA1) else Color(0xFF5C5C61)
            ),
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 8.dp),
            onClick = { offset ->
                termsAnnotatedString.getStringAnnotations(tag = "TERMS", start = offset, end = offset)
                    .firstOrNull()?.let {
                        tactile.perform(TactileType.LightTap)
                        onTermsClick()
                    }
                termsAnnotatedString.getStringAnnotations(tag = "PRIVACY", start = offset, end = offset)
                    .firstOrNull()?.let {
                        tactile.perform(TactileType.LightTap)
                        onPrivacyClick()
                    }
            }
        )
    }
}


@Composable
private fun AuthProviderButton(
    label: String,
    enabled: Boolean,
    loading: Boolean,
    container: Color,
    content: Color,
    tag: String,
    onClick: () -> Unit,
    icon: @Composable () -> Unit
) {
    val bg by animateColorAsState(
        targetValue = if (enabled || loading) container else container.copy(alpha = 0.5f),
        animationSpec = nebFastEffectsSpec(),
        label = "auth_provider_bg"
    )
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(56.dp)
            .testTag(tag)
            .clip(RoundedCornerShape(28.dp))
            .background(bg)
            .nebPressable(enabled = enabled, tactile = TactileType.ButtonTap, onClick = onClick),
        contentAlignment = Alignment.Center
    ) {
        if (loading) {
            NebLoader(size = NebLoaderSize.Inline, color = content)
        } else {
            Row(verticalAlignment = Alignment.CenterVertically) {
                icon()
                Spacer(modifier = Modifier.width(12.dp))
                Text(
                    text = label,
                    fontFamily = Poppins,
                    fontWeight = FontWeight.SemiBold,
                    fontSize = 15.sp,
                    letterSpacing = 0.15.sp,
                    color = content
                )
            }
        }
    }
}
