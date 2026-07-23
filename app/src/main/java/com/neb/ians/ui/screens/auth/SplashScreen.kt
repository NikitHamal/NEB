package com.neb.ians.ui.screens.auth

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.R
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.AuthState
import kotlinx.coroutines.async
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.first

private const val SPLASH_DURATION_MS = 2_500L

@Composable
fun SplashScreen(
    authRepository: AuthRepository,
    onNavigateToHome: () -> Unit,
    onNavigateToLogin: () -> Unit,
    onNavigateToCompleteProfile: () -> Unit
) {
    val logoScale = remember { Animatable(0.5f) }
    val logoAlpha = remember { Animatable(0f) }
    val textAlpha = remember { Animatable(0f) }
    val textOffsetY = remember { Animatable(18f) }
    val taglineAlpha = remember { Animatable(0f) }

    LaunchedEffect(authRepository) {
        // Animate logo entrance with spring bounce
        async {
            logoAlpha.animateTo(1f, animationSpec = tween(400))
        }
        async {
            logoScale.animateTo(
                targetValue = 1f,
                animationSpec = spring(
                    dampingRatio = 0.6f,
                    stiffness = 300f
                )
            )
        }

        delay(300)

        // Animate NEBians title text reveal
        async {
            textAlpha.animateTo(1f, animationSpec = tween(500, easing = FastOutSlowInEasing))
        }
        async {
            textOffsetY.animateTo(0f, animationSpec = tween(500, easing = FastOutSlowInEasing))
        }

        delay(200)

        // Animate tagline fade-in
        async {
            taglineAlpha.animateTo(1f, animationSpec = tween(400))
        }

        delay(SPLASH_DURATION_MS - 900)

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
        color = MaterialTheme.colorScheme.surface
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .statusBarsPadding(),
            contentAlignment = Alignment.Center
        ) {
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                // Floating logo directly (NO card/Surface background)
                Image(
                    painter = painterResource(id = R.drawable.ic_nebians_logo),
                    contentDescription = "NEBians Logo",
                    modifier = Modifier
                        .size(108.dp)
                        .graphicsLayer {
                            scaleX = logoScale.value
                            scaleY = logoScale.value
                            alpha = logoAlpha.value
                        },
                    contentScale = ContentScale.Fit
                )

                Spacer(modifier = Modifier.height(24.dp))

                // Brand text "NEBians" with gradient brush
                Text(
                    text = "NEBians",
                    style = TextStyle(
                        fontSize = 38.sp,
                        fontWeight = FontWeight.Bold,
                        brush = Brush.horizontalGradient(
                            colors = listOf(
                                MaterialTheme.colorScheme.primary,
                                MaterialTheme.colorScheme.tertiary
                            )
                        ),
                        letterSpacing = 1.8.sp
                    ),
                    modifier = Modifier.graphicsLayer {
                        alpha = textAlpha.value
                        translationY = textOffsetY.value
                    }
                )

                Spacer(modifier = Modifier.height(6.dp))

                // Subtitle tagline
                Text(
                    text = "Nepali Learning Community",
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = FontWeight.Medium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    letterSpacing = 0.5.sp,
                    modifier = Modifier.graphicsLayer {
                        alpha = taglineAlpha.value
                    }
                )
            }
        }
    }
}

