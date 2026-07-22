package com.neb.ians.ui.screens.auth

import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import com.airbnb.lottie.compose.LottieAnimation
import com.airbnb.lottie.compose.LottieCompositionSpec
import com.airbnb.lottie.compose.rememberLottieComposition
import com.neb.ians.R
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.AuthState
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.first

private const val SPLASH_DURATION_MS = 3_000L
private val SplashBackground = Color(0xFFE9EBF0)

@Composable
fun SplashScreen(
    authRepository: AuthRepository,
    onNavigateToHome: () -> Unit,
    onNavigateToLogin: () -> Unit,
    onNavigateToCompleteProfile: () -> Unit
) {
    val composition = rememberLottieComposition(
        spec = LottieCompositionSpec.RawRes(R.raw.nebians_splash)
    ).value

    LaunchedEffect(authRepository) {
        // Exact three-second SVG-matched cycle:
        // reveal -> hold -> un-reveal -> short blank gap.
        delay(SPLASH_DURATION_MS)

        when (val state = authRepository.authState.first()) {
            is AuthState.Guest -> onNavigateToHome()
            is AuthState.Authenticated -> {
                if (state.isProfileComplete) {
                    onNavigateToHome()
                } else {
                    onNavigateToCompleteProfile()
                }
            }
            else -> onNavigateToLogin()
        }
    }

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = SplashBackground
    ) {
        LottieAnimation(
            composition = composition,
            modifier = Modifier.fillMaxSize(),
            iterations = 1,
            contentScale = ContentScale.Crop
        )
    }
}
