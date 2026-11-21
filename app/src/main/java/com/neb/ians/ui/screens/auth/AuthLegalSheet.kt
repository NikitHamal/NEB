package com.neb.ians.ui.screens.auth

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Close
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.ui.screens.legal.LegalDocSwitcher
import com.neb.ians.ui.screens.legal.LegalSectionBlock
import com.neb.ians.ui.screens.legal.LegalTextColors
import com.neb.ians.ui.screens.legal.NebLegal
import com.neb.ians.ui.theme.nebFloatColor
import com.neb.ians.ui.theme.nebFloatLine
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
    var activeKey by remember(sheetType) {
        mutableStateOf(
            if (sheetType == LegalSheetType.TERMS) NebLegal.TERMS else NebLegal.PRIVACY
        )
    }
    val document = remember(activeKey) {
        NebLegal.documentFor(activeKey)
    }
    val scheme = MaterialTheme.colorScheme
    val colors = remember(isDark, scheme) {
        LegalTextColors(
            heading = scheme.onSurface,
            body = scheme.onSurfaceVariant,
            marker = scheme.onSecondaryContainer,
            markerBackground = scheme.secondaryContainer
        )
    }

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        containerColor = nebFloatColor(),
        contentColor = scheme.onSurface,
        shape = RoundedCornerShape(topStart = 28.dp, topEnd = 28.dp),
        dragHandle = {
            BottomSheetDefaults.DragHandle(
                color = nebFloatLine()
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
                        color = scheme.onSurface
                    )
                    Text(
                        text = document.subtitle,
                        style = MaterialTheme.typography.labelMedium,
                        color = scheme.onSurfaceVariant
                    )
                }

                IconButton(
                    onClick = {
                        tactile.perform(TactileType.LightTap)
                        onDismiss()
                    }
                ) {
                    Icon(
                        imageVector = Icons.Outlined.Close,
                        contentDescription = "Close",
                        tint = scheme.onSurfaceVariant
                    )
                }
            }

            Row(
                modifier = Modifier
                    .clip(RoundedCornerShape(20.dp))
                    .background(scheme.surfaceContainerHigh)
                    .padding(horizontal = 12.dp, vertical = 6.dp)
            ) {
                Text(
                    text = document.lastUpdated,
                    style = MaterialTheme.typography.labelMedium.copy(fontSize = 12.sp),
                    color = scheme.onSurfaceVariant
                )
            }

            Spacer(modifier = Modifier.height(12.dp))

            LegalDocSwitcher(
                activeKey = activeKey,
                onSelectKey = { nextKey ->
                    if (nextKey != activeKey) {
                        activeKey = nextKey
                    }
                }
            )

            Spacer(modifier = Modifier.height(14.dp))

            HorizontalDivider(
                color = nebFloatLine(),
                modifier = Modifier.padding(bottom = 16.dp)
            )

            LazyColumn(
                modifier = Modifier.weight(1f, fill = false),
                verticalArrangement = Arrangement.spacedBy(20.dp)
            ) {
                items(document.sections, key = { "${document.key}_${it.number}" }, contentType = { "legal_section" }) { section ->
                    LegalSectionBlock(section = section, colors = colors)
                }
                item(key = "footer", contentType = "footer") {
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
                    containerColor = scheme.primary,
                    contentColor = scheme.onPrimary
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
