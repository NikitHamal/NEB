package com.neb.ians.ui.screens.auth

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.util.TactileType
import com.neb.ians.util.rememberTactileFeedback

enum class LegalSheetType {
    TERMS,
    PRIVACY
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AuthLegalSheet(
    sheetType: LegalSheetType?,
    onDismiss: () -> Unit,
    isDark: Boolean
) {
    if (sheetType == null) return

    val tactile = rememberTactileFeedback()
    val isTerms = sheetType == LegalSheetType.TERMS

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        containerColor = if (isDark) Color(0xFF12151B) else Color(0xFFFFFFFF),
        contentColor = if (isDark) Color(0xFFF1F5F9) else Color(0xFF0F172A),
        shape = RoundedCornerShape(topStart = 28.dp, topEnd = 28.dp),
        dragHandle = {
            BottomSheetDefaults.DragHandle(
                color = if (isDark) Color(0xFF333D4F) else Color(0xFFD1D5DB)
            )
        }
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp)
                .padding(bottom = 32.dp)
        ) {
            // Header with title and close icon
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(bottom = 12.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text(
                        text = if (isTerms) "Terms of Service" else "Privacy Policy",
                        style = MaterialTheme.typography.titleLarge.copy(
                            fontWeight = FontWeight.Bold,
                            fontSize = 22.sp
                        ),
                        color = if (isDark) Color(0xFFF8FAFC) else Color(0xFF0F172A)
                    )
                    Text(
                        text = "NEBians Learning Platform • Nepal",
                        style = MaterialTheme.typography.labelMedium,
                        color = if (isDark) Color(0xFF94A3B8) else Color(0xFF64748B)
                    )
                }

                IconButton(
                    onClick = {
                        tactile.perform(TactileType.LightTap)
                        onDismiss()
                    }
                ) {
                    Icon(
                        imageVector = Icons.Default.Close,
                        contentDescription = "Close",
                        tint = if (isDark) Color(0xFF94A3B8) else Color(0xFF64748B)
                    )
                }
            }

            HorizontalDivider(
                color = if (isDark) Color(0xFF232A36) else Color(0xFFE5E7EB),
                modifier = Modifier.padding(bottom = 16.dp)
            )

            // Scrollable Content
            Column(
                modifier = Modifier
                    .weight(1f, fill = false)
                    .verticalScroll(rememberScrollState())
            ) {
                if (isTerms) {
                    LegalSection(
                        isDark = isDark,
                        title = "1. Acceptance of Terms",
                        content = "By accessing or using the NEBians mobile application, you agree to be bound by these Terms of Service. If you do not agree with any part of these terms, you may not use the service."
                    )
                    LegalSection(
                        isDark = isDark,
                        title = "2. Educational Purpose & Community",
                        content = "NEBians is an open educational platform designed for Nepali students, educators, and lifelong learners. All study materials, notes, model question solutions, and forum discussions are intended purely for personal learning and academic growth."
                    )
                    LegalSection(
                        isDark = isDark,
                        title = "3. Community Guidelines & Academic Integrity",
                        content = "Users must treat all learners and teachers with respect. Plagiarism, academic dishonesty, hate speech, harassment, and sharing copyrighted examination materials without authorization are strictly prohibited and may result in immediate suspension."
                    )
                    LegalSection(
                        isDark = isDark,
                        title = "4. User Accounts & Security",
                        content = "You are responsible for safeguarding your login credentials (Google, GitHub, or Email account). You agree to notify us immediately of any unauthorized access or security breach."
                    )
                    LegalSection(
                        isDark = isDark,
                        title = "5. Changes to Terms",
                        content = "We may revise these Terms occasionally to reflect feature additions or policy changes. Continued use of NEBians signifies your acceptance of any updated terms."
                    )
                } else {
                    LegalSection(
                        isDark = isDark,
                        title = "1. Information We Collect",
                        content = "When you register or sign in using Google, GitHub, or Email, we collect your display name, email address, profile avatar, and study grade/subjects to personalize your learning experience."
                    )
                    LegalSection(
                        isDark = isDark,
                        title = "2. How We Use Your Data",
                        content = "Your information is used solely to provide educational resources, synchronize your forum questions and answers, maintain your study bookmarks, and deliver relevant academic notifications."
                    )
                    LegalSection(
                        isDark = isDark,
                        title = "3. Data Privacy & Zero Selling",
                        content = "We do NOT sell, rent, or monetize your personal information to third parties or advertisers. Your academic records and account details remain confidential."
                    )
                    LegalSection(
                        isDark = isDark,
                        title = "4. Local & Offline Storage",
                        content = "NEBians stores your downloaded PDF syllabi, notes, and study bookmarks in an encrypted local database on your device, allowing you to study offline seamlessly."
                    )
                    LegalSection(
                        isDark = isDark,
                        title = "5. Your Rights & Account Deletion",
                        content = "You retain full ownership of your data. You may edit your profile, update your privacy visibility, or request permanent deletion of your account at any time via Settings."
                    )
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            Button(
                onClick = {
                    tactile.perform(TactileType.ButtonTap)
                    onDismiss()
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(48.dp),
                shape = RoundedCornerShape(24.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = if (isDark) Color(0xFF38BDF8) else Color(0xFF0284C7),
                    contentColor = Color.White
                )
            ) {
                Text(
                    text = "I Understand",
                    style = MaterialTheme.typography.titleSmall.copy(fontWeight = FontWeight.SemiBold)
                )
            }
        }
    }
}

@Composable
private fun LegalSection(
    isDark: Boolean,
    title: String,
    content: String
) {
    Column(modifier = Modifier.padding(bottom = 16.dp)) {
        Text(
            text = title,
            style = MaterialTheme.typography.titleSmall.copy(
                fontWeight = FontWeight.Bold,
                fontSize = 15.sp
            ),
            color = if (isDark) Color(0xFFF1F5F9) else Color(0xFF0F172A)
        )
        Spacer(modifier = Modifier.height(4.dp))
        Text(
            text = content,
            style = MaterialTheme.typography.bodyMedium.copy(
                fontSize = 13.5.sp,
                lineHeight = 19.sp
            ),
            color = if (isDark) Color(0xFF94A3B8) else Color(0xFF475569)
        )
    }
}
