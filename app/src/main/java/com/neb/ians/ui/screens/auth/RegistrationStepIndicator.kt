package com.neb.ians.ui.screens.auth

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

data class RegistrationStepInfo(
    val title: String,
    val subtitle: String
)

val REGISTRATION_STEPS = listOf(
    RegistrationStepInfo(
        title = "Role & Identity",
        subtitle = "Tell us what brings you to NEBians"
    ),
    RegistrationStepInfo(
        title = "Basic Info",
        subtitle = "Personalize your public profile"
    ),
    RegistrationStepInfo(
        title = "Academic Details",
        subtitle = "Curate content tailored to your studies"
    )
)

@Composable
fun RegistrationStepIndicator(
    currentStep: Int,
    totalSteps: Int = 3,
    modifier: Modifier = Modifier
) {
    val currentStepInfo = REGISTRATION_STEPS.getOrElse(currentStep) {
        RegistrationStepInfo("Step ${currentStep + 1}", "")
    }

    Column(
        modifier = modifier.fillMaxWidth()
    ) {
        // Step label & percentage indicator
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column {
                Text(
                    text = "STEP ${currentStep + 1} OF $totalSteps",
                    style = MaterialTheme.typography.labelSmall.copy(
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 1.2.sp
                    ),
                    color = MaterialTheme.colorScheme.primary
                )
                Spacer(modifier = Modifier.height(2.dp))
                Text(
                    text = currentStepInfo.title,
                    style = MaterialTheme.typography.titleLarge.copy(
                        fontWeight = FontWeight.Bold,
                        letterSpacing = (-0.3).sp
                    ),
                    color = MaterialTheme.colorScheme.onSurface
                )
            }

            // Quick step dots badge
            Row(
                horizontalArrangement = Arrangement.spacedBy(6.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                for (i in 0 until totalSteps) {
                    val isDone = i < currentStep
                    val isCurrent = i == currentStep

                    val dotColor by animateColorAsState(
                        targetValue = when {
                            isDone -> MaterialTheme.colorScheme.primary
                            isCurrent -> MaterialTheme.colorScheme.primary
                            else -> MaterialTheme.colorScheme.outlineVariant
                        },
                        animationSpec = tween(300),
                        label = "dotColor"
                    )

                    val dotWidth by animateFloatAsState(
                        targetValue = if (isCurrent) 22f else 8f,
                        animationSpec = tween(300),
                        label = "dotWidth"
                    )

                    Box(
                        modifier = Modifier
                            .height(8.dp)
                            .width(dotWidth.dp)
                            .clip(CircleShape)
                            .background(dotColor)
                    )
                }
            }
        }

        if (currentStepInfo.subtitle.isNotBlank()) {
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = currentStepInfo.subtitle,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }

        Spacer(modifier = Modifier.height(14.dp))

        // Segmented step progress bar
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .height(4.dp),
            horizontalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            for (i in 0 until totalSteps) {
                val progress = when {
                    i < currentStep -> 1f
                    i == currentStep -> 1f
                    else -> 0f
                }
                val trackColor = if (progress > 0f) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant

                Box(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxHeight()
                        .clip(CircleShape)
                        .background(trackColor)
                )
            }
        }
    }
}
