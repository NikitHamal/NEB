package com.neb.ians.ui.screens.profile

import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.platform.LocalContext
import com.neb.ians.data.repository.SecurePrefs
import com.neb.ians.ui.screens.web.WebPortalScreen

@Composable
fun EditProfileScreen(
    onNavigateBack: () -> Unit
) {
    val context = LocalContext.current
    val token = remember { SecurePrefs.getAuthToken(context).orEmpty() }
    val editUrl = "https://nebians.consica.com.np/auth/token-login/?token=$token&next=/profile/edit/"

    WebPortalScreen(
        url = editUrl,
        onNavigateBack = onNavigateBack,
        onUrlChange = { currentUrl ->
            if (currentUrl.contains("/profile/") && !currentUrl.contains("/profile/edit")) {
                onNavigateBack()
            }
        }
    )
}