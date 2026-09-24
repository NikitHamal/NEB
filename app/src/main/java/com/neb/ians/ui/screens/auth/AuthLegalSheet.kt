package com.neb.ians.ui.screens.auth

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.ui.screens.legal.LegalSectionBlock
import com.neb.ians.ui.screens.legal.LegalTextColors
import com.neb.ians.ui.screens.legal.NebLegal
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
    val document = remember(sheetType) {
        NebLegal.documentFor(if (sheetType == LegalSheetType.TERMS) NebLegal.TERMS else NebLegal.PRIVACY)
    }
    val colors = remember(isDark) {
        LegalTextColors(
            heading = if (isDark) Color(0xFFF5F5F6) else Color(0xFF0A0A0B),
            body = if (isDark) Color(0xFF9B9BA1) else Color(0xFF5C5C61),
            marker = if (isDark) Color(0xFFC9C9CD) else Color(0xFF313136),
            markerBackground = if (isDark) Color(0xFF26262A) else Color(0xFFF1F1F3)
        )
    }

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        containerColor = if (isDark) Color(0xFF131315) else Color(0xFFFFFFFF),
        contentColor = if (isDark) Color(0xFFF5F5F6) else Color(0xFF0A0A0B),
        shape = RoundedCornerShape(topStart = 28.dp, topEnd = 28.dp),
        dragHandle = {
            BottomSheetDefaults.DragHandle(
                color = if (isDark) Color(0xFF3A3A3F) else Color(0xFFDCDCE0)
            )
        }
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp)
                .padding(bottom = 32.dp)
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(bottom = 12.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = document.title,
                        style = MaterialTheme.typography.titleLarge.copy(
                            fontWeight = FontWeight.Bold,
                            fontSize = 22.sp
                        ),
                        color = if (isDark) Color(0xFFFAFAFB) else Color(0xFF0A0A0B)
                    )
                    Text(
                        text = document.subtitle,
                        style = MaterialTheme.typography.labelMedium,
                        color = if (isDark) Color(0xFF9B9BA1) else Color(0xFF5C5C61)
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
                        tint = if (isDark) Color(0xFF9B9BA1) else Color(0xFF5C5C61)
                    )
                }
            }

            Row(
                modifier = Modifier
                    .clip(RoundedCornerShape(50))
                    .background(colors.markerBackground)
                    .padding(horizontal = 12.dp, vertical = 6.dp)
            ) {
                Text(
                    text = document.lastUpdated,
                    style = MaterialTheme.typography.labelMedium.copy(fontSize = 12.sp),
                    color = colors.body
                )
            }

            Spacer(modifier = Modifier.height(14.dp))

            HorizontalDivider(
                color = if (isDark) Color(0xFF26262A) else Color(0xFFE9E9EB),
                modifier = Modifier.padding(bottom = 16.dp)
            )

            LazyColumn(
                modifier = Modifier.weight(1f, fill = false),
                verticalArrangement = Arrangement.spacedBy(20.dp)
            ) {
                items(document.sections, key = { it.number }) { section ->
                    LegalSectionBlock(section = section, colors = colors)
                }
                item(key = "footer") {
                    Text(
                        text = "Read the full document at ${document.webUrl}",
                        style = MaterialTheme.typography.bodySmall,
                        color = colors.body
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
                    containerColor = if (isDark) Color(0xFFF5F5F6) else Color(0xFF101012),
                    contentColor = if (isDark) Color(0xFF0A0A0B) else Color(0xFFFFFFFF)
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
