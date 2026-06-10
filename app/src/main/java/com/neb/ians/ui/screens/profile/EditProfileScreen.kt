package com.neb.ians.ui.screens.profile

import androidx.compose.runtime.Composable
import com.neb.ians.ui.screens.auth.CompleteProfileScreen

@Composable
fun EditProfileScreen(
    onNavigateBack: () -> Unit
) {
    CompleteProfileScreen(
        onNavigateToHome = {},
        onNavigateBack = onNavigateBack
    )
}