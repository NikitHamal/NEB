package com.neb.ians.ui.screens.onboarding

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideOutHorizontally
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.MenuBook
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.Forum
import androidx.compose.material.icons.filled.School
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.AuthState
import com.neb.ians.ui.screens.settings.SettingsViewModel
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

private data class OnboardingPage(
    val icon: ImageVector,
    val title: String,
    val body: String
)

private val PAGES = listOf(
    OnboardingPage(
        icon = Icons.Filled.School,
        title = "Welcome to NEBians",
        body = "Nepal's learning community — study resources, discussions and smart tools in one place."
    ),
    OnboardingPage(
        icon = Icons.AutoMirrored.Filled.MenuBook,
        title = "Library, on the go",
        body = "Notes, past papers, model questions and textbooks — filter by subject and class, read offline."
    ),
    OnboardingPage(
        icon = Icons.Filled.Forum,
        title = "Learn together",
        body = "Ask questions, share answers and follow classmates, teachers and toppers."
    ),
    OnboardingPage(
        icon = Icons.Filled.AutoAwesome,
        title = "Meet Neby AI",
        body = "Summaries, quizzes, flashcards and study help — generated for whatever you're reading."
    )
)

@Composable
fun OnboardingScreen(
    authRepository: AuthRepository,
    settingsViewModel: SettingsViewModel,
    onNavigateToHome: () -> Unit,
    onNavigateToLogin: () -> Unit,
    onNavigateToCompleteProfile: () -> Unit
) {
    var page by remember { mutableIntStateOf(0) }
    val isLast = page == PAGES.lastIndex

    fun finish() {
        settingsViewModel.setOnboardingSeen(true)
    }

    val blobShift by rememberInfiniteTransition(label = "onboarding_blobs").animateFloat(
        initialValue = -1f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 5200, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "blob_shift"
    )

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.surface
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .statusBarsPadding()
        ) {
            Box(
                modifier = Modifier
                    .size(280.dp)
                    .offset(x = (blobShift * 28).dp, y = (-40).dp)
                    .align(Alignment.TopEnd)
                    .clip(CircleShape)
                    .background(
                        Brush.radialGradient(
                            colors = listOf(
                                MaterialTheme.colorScheme.primary.copy(alpha = 0.14f),
                                MaterialTheme.colorScheme.primary.copy(alpha = 0f)
                            )
                        )
                    )
            )
            Box(
                modifier = Modifier
                    .size(240.dp)
                    .offset(x = (blobShift * -20).dp, y = 120.dp)
                    .align(Alignment.CenterEnd)
                    .clip(CircleShape)
                    .background(
                        Brush.radialGradient(
                            colors = listOf(
                                MaterialTheme.colorScheme.tertiary.copy(alpha = 0.12f),
                                MaterialTheme.colorScheme.tertiary.copy(alpha = 0f)
                            )
                        )
                    )
            )

            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(horizontal = 24.dp)
                    .padding(top = 56.dp, bottom = 32.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                AnimatedContent(
                    targetState = page,
                    transitionSpec = {
                        (slideInHorizontally(animationSpec = tween(300)) { it / 3 } + fadeIn(tween(300)))
                            .togetherWith(slideOutHorizontally(animationSpec = tween(200)) { -it / 3 } + fadeOut(tween(200)))
                    },
                    label = "onboarding_page"
                ) { index ->
                    val item = PAGES[index]
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Surface(
                            modifier = Modifier.size(120.dp),
                            shape = CircleShape,
                            color = MaterialTheme.colorScheme.primaryContainer,
                            tonalElevation = 2.dp
                        ) {
                            Box(contentAlignment = Alignment.Center) {
                                Icon(
                                    imageVector = item.icon,
                                    contentDescription = null,
                                    modifier = Modifier.size(56.dp),
                                    tint = MaterialTheme.colorScheme.primary
                                )
                            }
                        }
                        Spacer(modifier = Modifier.height(32.dp))
                        Text(
                            text = item.title,
                            style = MaterialTheme.typography.titleLarge,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface,
                            textAlign = TextAlign.Center
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        Text(
                            text = item.body,
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            textAlign = TextAlign.Center,
                            modifier = Modifier.padding(horizontal = 8.dp)
                        )
                    }
                }

                Spacer(modifier = Modifier.weight(1f))

                Row(
                    horizontalArrangement = Arrangement.Center,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    PAGES.indices.forEach { index ->
                        val width by animateDpAsState(
                            targetValue = if (index == page) 24.dp else 8.dp,
                            animationSpec = tween(250),
                            label = "dot_$index"
                        )
                        Box(
                            modifier = Modifier
                                .padding(horizontal = 3.dp)
                                .size(width = width, height = 8.dp)
                                .clip(CircleShape)
                                .background(
                                    if (index == page) MaterialTheme.colorScheme.primary
                                    else MaterialTheme.colorScheme.outlineVariant
                                )
                        )
                    }
                }

                Spacer(modifier = Modifier.height(28.dp))

                if (isLast) {
                    Button(
                        onClick = {
                            finish()
                            navigateAfterOnboarding(
                                authRepository = authRepository,
                                onNavigateToHome = onNavigateToHome,
                                onNavigateToLogin = onNavigateToLogin,
                                onNavigateToCompleteProfile = onNavigateToCompleteProfile
                            )
                        },
                        modifier = Modifier.fillMaxWidth(),
                        colors = ButtonDefaults.buttonColors(
                            containerColor = MaterialTheme.colorScheme.primary,
                            contentColor = MaterialTheme.colorScheme.onPrimary
                        )
                    ) {
                        Text(
                            text = "Get Started",
                            style = MaterialTheme.typography.labelLarge,
                            modifier = Modifier.padding(vertical = 4.dp)
                        )
                    }
                } else {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        TextButton(
                            onClick = {
                                finish()
                                navigateAfterOnboarding(
                                    authRepository = authRepository,
                                    onNavigateToHome = onNavigateToHome,
                                    onNavigateToLogin = onNavigateToLogin,
                                    onNavigateToCompleteProfile = onNavigateToCompleteProfile
                                )
                            }
                        ) {
                            Text(text = "Skip", style = MaterialTheme.typography.labelLarge)
                        }
                        Button(
                            onClick = { page += 1 },
                            colors = ButtonDefaults.buttonColors(
                                containerColor = MaterialTheme.colorScheme.primary,
                                contentColor = MaterialTheme.colorScheme.onPrimary
                            )
                        ) {
                            Text(text = "Next", style = MaterialTheme.typography.labelLarge)
                        }
                    }
                }
            }
        }
    }
}

private fun navigateAfterOnboarding(
    authRepository: AuthRepository,
    onNavigateToHome: () -> Unit,
    onNavigateToLogin: () -> Unit,
    onNavigateToCompleteProfile: () -> Unit
) {
    kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.Main).launch {
        when (val state = authRepository.authState.first()) {
            is AuthState.Guest -> onNavigateToHome()
            is AuthState.Authenticated -> {
                if (state.isProfileComplete) onNavigateToHome()
                else onNavigateToCompleteProfile()
            }
            else -> onNavigateToLogin()
        }
    }
}
