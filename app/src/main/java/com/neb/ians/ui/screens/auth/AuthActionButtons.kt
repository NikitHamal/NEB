package com.neb.ians.ui.screens.auth

import androidx.compose.foundation.BorderStroke
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
import com.neb.ians.util.TactileType
import com.neb.ians.util.rememberTactileFeedback

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

    // NEBians Brand Accent Colors
    val brandSapphire = Color(0xFF0D5CE5)
    val brandSapphireLight = Color(0xFF7CA8FF)
    val linkColor = if (isDark) brandSapphireLight else brandSapphire

    Column(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        // 1. Continue with Google (Exact official light-gray color, ZERO shadows)
        Button(
            onClick = {
                if (!isLoading) {
                    tactile.perform(TactileType.ButtonTap)
                    onGoogleClick()
                }
            },
            enabled = !isLoading,
            modifier = Modifier
                .fillMaxWidth()
                .height(54.dp)
                .testTag("google_login_button"),
            shape = RoundedCornerShape(27.dp),
            colors = ButtonDefaults.buttonColors(
                containerColor = if (isDark) Color(0xFF1E2430) else Color(0xFFF2F2F2),
                contentColor = if (isDark) Color(0xFFF1F5F9) else Color(0xFF1F1F1F),
                disabledContainerColor = Color(0xFFE2E4E8),
                disabledContentColor = Color(0xFF888888)
            ),
            border = if (isDark) BorderStroke(1.dp, Color(0xFF334155)) else null,
            elevation = ButtonDefaults.buttonElevation(
                defaultElevation = 0.dp,
                pressedElevation = 0.dp,
                focusedElevation = 0.dp,
                hoveredElevation = 0.dp
            )
        ) {
            if (isLoading && loadingProvider == "google") {
                CircularProgressIndicator(
                    modifier = Modifier.size(20.dp),
                    color = if (isDark) Color.White else Color(0xFF1F1F1F),
                    strokeWidth = 2.dp
                )
            } else {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.Center
                ) {
                    Icon(
                        painter = painterResource(id = R.drawable.ic_google),
                        contentDescription = "Google Logo",
                        tint = Color.Unspecified,
                        modifier = Modifier.size(22.dp)
                    )
                    Spacer(modifier = Modifier.width(12.dp))
                    Text(
                        text = "Continue with Google",
                        fontFamily = Poppins,
                        fontWeight = FontWeight.SemiBold, // Poppins 600
                        fontSize = 15.sp,
                        letterSpacing = 0.15.sp
                    )
                }
            }
        }

        Spacer(modifier = Modifier.height(12.dp))

        // 2. Continue with GitHub (Deep solid black background, ZERO shadows)
        Button(
            onClick = {
                if (!isLoading) {
                    tactile.perform(TactileType.ButtonTap)
                    onGitHubClick()
                }
            },
            enabled = !isLoading,
            modifier = Modifier
                .fillMaxWidth()
                .height(54.dp)
                .testTag("github_login_button"),
            shape = RoundedCornerShape(27.dp),
            colors = ButtonDefaults.buttonColors(
                containerColor = Color(0xFF0F1117),
                contentColor = Color.White,
                disabledContainerColor = Color(0xFF1E212A),
                disabledContentColor = Color(0xFF71717A)
            ),
            border = BorderStroke(
                width = 1.dp,
                color = if (isDark) Color(0xFF2B313F) else Color(0xFF222630)
            ),
            elevation = ButtonDefaults.buttonElevation(
                defaultElevation = 0.dp,
                pressedElevation = 0.dp,
                focusedElevation = 0.dp,
                hoveredElevation = 0.dp
            )
        ) {
            if (isLoading && loadingProvider == "github") {
                CircularProgressIndicator(
                    modifier = Modifier.size(20.dp),
                    color = Color.White,
                    strokeWidth = 2.dp
                )
            } else {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.Center
                ) {
                    Icon(
                        painter = painterResource(id = R.drawable.ic_github),
                        contentDescription = "GitHub Logo",
                        tint = Color.White,
                        modifier = Modifier.size(22.dp)
                    )
                    Spacer(modifier = Modifier.width(12.dp))
                    Text(
                        text = "Continue with GitHub",
                        fontFamily = Poppins,
                        fontWeight = FontWeight.SemiBold, // Poppins 600
                        fontSize = 15.sp,
                        letterSpacing = 0.15.sp
                    )
                }
            }
        }

        Spacer(modifier = Modifier.height(12.dp))

        // 3. Continue with Email (Strokes only, Poppins 600)
        OutlinedButton(
            onClick = {
                if (!isLoading) {
                    tactile.perform(TactileType.ButtonTap)
                    onEmailClick()
                }
            },
            enabled = !isLoading,
            modifier = Modifier
                .fillMaxWidth()
                .height(52.dp)
                .testTag("email_login_button"),
            shape = RoundedCornerShape(26.dp),
            colors = ButtonDefaults.outlinedButtonColors(
                containerColor = Color.Transparent,
                contentColor = if (isDark) Color(0xFFF1F5F9) else Color(0xFF1E293B)
            ),
            border = BorderStroke(
                width = 1.5.dp,
                color = if (isDark) Color(0xFF3B4861) else Color(0xFFCBD5E1)
            )
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.Center
            ) {
                Icon(
                    imageVector = Icons.Outlined.Mail,
                    contentDescription = "Email",
                    modifier = Modifier.size(20.dp),
                    tint = linkColor
                )
                Spacer(modifier = Modifier.width(10.dp))
                Text(
                    text = "Continue with Email",
                    fontFamily = Poppins,
                    fontWeight = FontWeight.SemiBold, // Poppins 600
                    fontSize = 14.5.sp
                )
            }
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
                color = if (isDark) Color(0xFF8896AB) else Color(0xFF64748B)
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
