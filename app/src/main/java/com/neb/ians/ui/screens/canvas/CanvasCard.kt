package com.neb.ians.ui.screens.canvas

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.ArrowUpward
import androidx.compose.material.icons.filled.DragIndicator
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.outlined.Close
import androidx.compose.material.icons.outlined.ContentCopy
import androidx.compose.material.icons.outlined.CropFree
import androidx.compose.material.icons.outlined.DeleteOutline
import androidx.compose.material.icons.outlined.OpenInFull
import androidx.compose.material.icons.outlined.Palette
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.ui.components.MarkdownInlineText
import com.neb.ians.util.rememberTactileFeedback
import com.neb.ians.util.TactileType

@Composable
fun CanvasCardItem(
    node: CanvasNode,
    isSelected: Boolean,
    isConnectingSource: Boolean = false,
    connectingDirection: String? = null,
    onDrag: (dx: Float, dy: Float) -> Unit,
    onDragEnd: () -> Unit,
    onSelect: () -> Unit,
    onExpand: () -> Unit,
    onDuplicate: () -> Unit,
    onDelete: () -> Unit,
    onColorChange: (String) -> Unit,
    onBranch: (direction: String, prompt: String) -> Unit,
    onConnect: (direction: String) -> Unit = {},
    modifier: Modifier = Modifier
) {
    val isDark = MaterialTheme.colorScheme.surface.luminance() < 0.5f
    val colors = CanvasColorTokens.getColors(node.color, isDark)
    val tactile = rememberTactileFeedback()
    var activeDiagNodeId by remember { mutableStateOf<String?>(null) }
    var followupText by remember { mutableStateOf("") }
    var showMoreMenu by remember { mutableStateOf(false) }

    val handleRadius = 20.dp

    Box(
        modifier = modifier.offset(-handleRadius, -handleRadius)
    ) {
        // Card Surface
        Box(
            modifier = Modifier
                .padding(handleRadius)
                .width(340.dp)
                .shadow(
                    elevation = if (isSelected) 14.dp else 4.dp,
                    shape = RoundedCornerShape(20.dp),
                    spotColor = colors.accent.copy(alpha = 0.25f)
                )
                .clip(RoundedCornerShape(20.dp))
                .background(colors.surface)
                .border(
                    BorderStroke(
                        width = if (isSelected) 2.dp else 1.dp,
                        color = if (isSelected) colors.accent else colors.border
                    ),
                    shape = RoundedCornerShape(20.dp)
                )
                .pointerInput(node.id) {
                    detectTapGestures(onTap = {
                        tactile.perform(TactileType.SelectionChange)
                        onSelect()
                    })
                }
        ) {
            Column(modifier = Modifier.fillMaxWidth()) {
                // Header with clear drag handle and controls
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(colors.headerBg)
                    .border(
                        BorderStroke(0.5.dp, colors.border.copy(alpha = 0.6f)),
                        shape = RoundedCornerShape(topStart = 20.dp, topEnd = 20.dp)
                    )
                    .pointerInput(node.id) {
                        detectDragGestures(
                            onDragStart = {
                                tactile.perform(TactileType.LightTap)
                                onSelect()
                            },
                            onDrag = { change, dragAmount ->
                                change.consume()
                                onDrag(dragAmount.x, dragAmount.y)
                            },
                            onDragEnd = onDragEnd,
                            onDragCancel = onDragEnd
                        )
                    }
                    .padding(horizontal = 12.dp, vertical = 10.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Visual drag grip
                Icon(
                    imageVector = Icons.Filled.DragIndicator,
                    contentDescription = "Drag to move card",
                    tint = colors.secondaryText.copy(alpha = 0.8f),
                    modifier = Modifier
                        .size(20.dp)
                        .padding(end = 4.dp)
                )

                Column(modifier = Modifier.weight(1f)) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Text(
                            text = node.title.ifBlank { node.prompt.take(30) },
                            style = MaterialTheme.typography.titleMedium.copy(
                                fontWeight = FontWeight.Bold,
                                fontSize = 14.5.sp
                            ),
                            color = colors.titleText,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier.weight(1f, fill = false)
                        )
                        // Kind Badge
                        Surface(
                            shape = RoundedCornerShape(99.dp),
                            color = colors.tagBg
                        ) {
                            Text(
                                text = node.kind.replaceFirstChar { it.uppercase() },
                                modifier = Modifier.padding(horizontal = 7.dp, vertical = 2.dp),
                                style = MaterialTheme.typography.labelSmall.copy(fontWeight = FontWeight.SemiBold),
                                color = colors.tagText
                            )
                        }
                    }

                    if (node.prompt.isNotBlank() && node.prompt != node.title) {
                        Text(
                            text = node.prompt,
                            style = MaterialTheme.typography.bodySmall.copy(fontSize = 11.5.sp),
                            color = colors.secondaryText,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier.padding(top = 2.dp)
                        )
                    }
                }

                // Header actions matching reference image: Expand + Duplicate + Delete
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(0.dp)
                ) {
                    IconButton(
                        onClick = onExpand,
                        modifier = Modifier.size(28.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.CropFree,
                            contentDescription = "Expand",
                            tint = colors.secondaryText,
                            modifier = Modifier.size(16.dp)
                        )
                    }

                    IconButton(
                        onClick = onDuplicate,
                        modifier = Modifier.size(28.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.ContentCopy,
                            contentDescription = "Duplicate",
                            tint = colors.secondaryText,
                            modifier = Modifier.size(15.dp)
                        )
                    }

                    IconButton(
                        onClick = onDelete,
                        modifier = Modifier.size(28.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.DeleteOutline,
                            contentDescription = "Delete",
                            tint = colors.secondaryText,
                            modifier = Modifier.size(16.dp)
                        )
                    }

                    Box {
                        IconButton(
                            onClick = { showMoreMenu = true },
                            modifier = Modifier.size(26.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Filled.MoreVert,
                                contentDescription = "Card options",
                                tint = colors.secondaryText.copy(alpha = 0.6f),
                                modifier = Modifier.size(15.dp)
                            )
                        }

                        DropdownMenu(
                            expanded = showMoreMenu,
                            onDismissRequest = { showMoreMenu = false }
                        ) {
                            val colorOptions = listOf(
                                "default" to "Default (Neutral)",
                                "blue" to "Blue (Concept)",
                                "green" to "Green (Formula/Example)",
                                "amber" to "Amber (Highlight)",
                                "rose" to "Rose (Warning/Trap)",
                                "purple" to "Purple (Synthesis)",
                                "slate" to "Slate (Reference)"
                            )
                            colorOptions.forEach { (key, label) ->
                                DropdownMenuItem(
                                    text = { Text(label) },
                                    onClick = {
                                        onColorChange(key)
                                        showMoreMenu = false
                                    }
                                )
                            }
                        }
                    }
                }
            }

            // Body
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(14.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                if (node.status == "generating") {
                    GeneratingIndicator(colors.accent)
                } else {
                    if (node.content.summary.isNotBlank()) {
                        MarkdownInlineText(
                            markdown = node.content.summary,
                            style = MaterialTheme.typography.bodyMedium.copy(
                                lineHeight = 21.sp,
                                fontSize = 13.5.sp
                            ),
                            color = colors.titleText
                        )
                    }

                    node.content.sections.forEachIndexed { idx, section ->
                        when (section.type) {
                            "text" -> {
                                section.content?.let { txt ->
                                    MarkdownInlineText(
                                        markdown = txt,
                                        style = MaterialTheme.typography.bodySmall.copy(
                                            lineHeight = 20.sp,
                                            fontSize = 13.sp
                                        ),
                                        color = colors.bodyText
                                    )
                                }
                            }
                            "diagram" -> {
                                DiagramSectionRenderer(
                                    section = section,
                                    activeNodeId = activeDiagNodeId,
                                    onNodeClick = { clickedId ->
                                        activeDiagNodeId = if (activeDiagNodeId == clickedId) null else clickedId
                                    },
                                    colors = colors
                                )
                            }
                            "comparison" -> {
                                ComparisonSectionRenderer(section = section, colors = colors)
                            }
                            "cards" -> {
                                CardsGridRenderer(section = section, colors = colors)
                            }
                            "bullets" -> {
                                BulletsListRenderer(section = section, colors = colors)
                            }
                            "timeline" -> {
                                TimelineSectionRenderer(section = section, colors = colors)
                            }
                        }
                    }
                }
            }

            // In-card follow-up input bar matching reference
            if (node.status != "generating") {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 12.dp, vertical = 8.dp)
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(36.dp)
                            .clip(RoundedCornerShape(99.dp))
                            .background(colors.surface)
                            .border(BorderStroke(1.dp, colors.border.copy(alpha = 0.8f)), RoundedCornerShape(99.dp))
                            .padding(start = 12.dp, end = 3.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        BasicTextField(
                            value = followupText,
                            onValueChange = { followupText = it },
                            modifier = Modifier.weight(1f),
                            singleLine = true,
                            maxLines = 1,
                            textStyle = MaterialTheme.typography.bodySmall.copy(
                                fontSize = 12.sp,
                                color = colors.titleText
                            ),
                            decorationBox = { innerTextField ->
                                if (followupText.isEmpty()) {
                                    Text(
                                        text = "Ask a follow-up...",
                                        style = MaterialTheme.typography.bodySmall.copy(fontSize = 12.sp),
                                        color = colors.secondaryText,
                                        maxLines = 1
                                    )
                                }
                                innerTextField()
                            }
                        )

                        val hasFollowup = followupText.isNotBlank()
                        IconButton(
                            onClick = {
                                if (hasFollowup) {
                                    onBranch("bottom", followupText.trim())
                                    followupText = ""
                                }
                            },
                            enabled = hasFollowup,
                            modifier = Modifier
                                .size(28.dp)
                                .clip(CircleShape)
                                .background(
                                    if (hasFollowup) colors.accent
                                    else if (isDark) Color(0xFF334155)
                                    else Color(0xFFEEF2F6)
                                )
                        ) {
                            Icon(
                                imageVector = Icons.Filled.ArrowUpward,
                                contentDescription = "Send",
                                tint = if (hasFollowup) Color.White else Color(0xFF94A3B8),
                                modifier = Modifier.size(14.dp)
                            )
                        }
                    }
                }
            }
        }
    }

        // Connector Ports on top, bottom, left, right - Visible when card is selected or connecting
        if (isSelected || isConnectingSource) {
            ConnectorPort(
                direction = "top",
                accent = colors.accent,
                surfaceColor = colors.surface,
                isConnectingSource = isConnectingSource && (connectingDirection == "top" || connectingDirection == null),
                modifier = Modifier
                    .align(Alignment.TopCenter)
                    .offset(y = 8.dp),
                onClick = { onConnect("top") }
            )
            ConnectorPort(
                direction = "bottom",
                accent = colors.accent,
                surfaceColor = colors.surface,
                isConnectingSource = isConnectingSource && (connectingDirection == "bottom" || connectingDirection == null),
                modifier = Modifier
                    .align(Alignment.BottomCenter)
                    .offset(y = (-8).dp),
                onClick = { onConnect("bottom") }
            )
            ConnectorPort(
                direction = "left",
                accent = colors.accent,
                surfaceColor = colors.surface,
                isConnectingSource = isConnectingSource && (connectingDirection == "left" || connectingDirection == null),
                modifier = Modifier
                    .align(Alignment.CenterStart)
                    .offset(x = 8.dp),
                onClick = { onConnect("left") }
            )
            ConnectorPort(
                direction = "right",
                accent = colors.accent,
                surfaceColor = colors.surface,
                isConnectingSource = isConnectingSource && (connectingDirection == "right" || connectingDirection == null),
                modifier = Modifier
                    .align(Alignment.CenterEnd)
                    .offset(x = (-8).dp),
                onClick = { onConnect("right") }
            )
        }
    }
}

@Composable
private fun ConnectorPort(
    direction: String,
    accent: Color,
    surfaceColor: Color,
    isConnectingSource: Boolean,
    modifier: Modifier = Modifier,
    onClick: () -> Unit
) {
    val tactile = rememberTactileFeedback()
    val transition = rememberInfiniteTransition(label = "pulse")
    val pulseScale by if (isConnectingSource) {
        transition.animateFloat(
            initialValue = 1f,
            targetValue = 1.25f,
            animationSpec = infiniteRepeatable(tween(550, easing = FastOutSlowInEasing), RepeatMode.Reverse),
            label = "pulseScale"
        )
    } else {
        remember { mutableStateOf(1f) }
    }

    Box(
        modifier = modifier
            .size(24.dp)
            .graphicsLayer {
                scaleX = pulseScale
                scaleY = pulseScale
            }
            .shadow(
                elevation = if (isConnectingSource) 4.dp else 2.dp,
                shape = CircleShape
            )
            .clip(CircleShape)
            .background(if (isConnectingSource) accent else surfaceColor)
            .border(
                BorderStroke(
                    width = if (isConnectingSource) 2.dp else 1.5.dp,
                    color = accent
                ),
                CircleShape
            )
            .clickable(onClick = {
                tactile.perform(TactileType.SelectionChange)
                onClick()
            }),
        contentAlignment = Alignment.Center
    ) {
        Icon(
            imageVector = Icons.Filled.Add,
            contentDescription = "Connect card",
            tint = if (isConnectingSource) Color.White else accent,
            modifier = Modifier.size(13.dp)
        )
    }
}

@Composable
private fun GeneratingIndicator(accent: Color) {
    val transition = rememberInfiniteTransition(label = "pulse")
    val alpha1 by transition.animateFloat(
        initialValue = 0.3f, targetValue = 1f,
        animationSpec = infiniteRepeatable(tween(700, easing = FastOutSlowInEasing), RepeatMode.Reverse),
        label = "a1"
    )
    val alpha2 by transition.animateFloat(
        initialValue = 0.3f, targetValue = 1f,
        animationSpec = infiniteRepeatable(tween(700, 200, easing = FastOutSlowInEasing), RepeatMode.Reverse),
        label = "a2"
    )
    val alpha3 by transition.animateFloat(
        initialValue = 0.3f, targetValue = 1f,
        animationSpec = infiniteRepeatable(tween(700, 400, easing = FastOutSlowInEasing), RepeatMode.Reverse),
        label = "a3"
    )

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 12.dp),
        horizontalArrangement = Arrangement.Center,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
            Box(Modifier.size(8.dp).clip(CircleShape).background(accent.copy(alpha = alpha1)))
            Box(Modifier.size(8.dp).clip(CircleShape).background(accent.copy(alpha = alpha2)))
            Box(Modifier.size(8.dp).clip(CircleShape).background(accent.copy(alpha = alpha3)))
        }
        Spacer(Modifier.width(10.dp))
        Text(
            text = "Neby is creating visual concept...",
            style = MaterialTheme.typography.bodySmall.copy(fontWeight = FontWeight.Medium),
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
private fun DiagramSectionRenderer(
    section: CanvasSection,
    activeNodeId: String?,
    onNodeClick: (String) -> Unit,
    colors: CanvasCardColorScheme
) {
    val tactile = rememberTactileFeedback()
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(14.dp))
            .background(colors.innerCardBg)
            .border(BorderStroke(1.dp, colors.innerCardBorder), RoundedCornerShape(14.dp))
            .padding(10.dp)
    ) {
        section.title?.let { t ->
            Text(
                text = t.uppercase(),
                style = MaterialTheme.typography.labelSmall.copy(
                    fontWeight = FontWeight.Bold,
                    letterSpacing = 1.sp
                ),
                color = colors.accent,
                modifier = Modifier.padding(bottom = 8.dp)
            )
        }

        val dNodes = section.nodes ?: emptyList()
        if (dNodes.size <= 2) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                dNodes.forEach { dn ->
                    val isActive = dn.id == activeNodeId
                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .clip(RoundedCornerShape(10.dp))
                            .background(if (isActive) colors.accent.copy(alpha = 0.15f) else colors.surface)
                            .border(
                                BorderStroke(if (isActive) 1.5.dp else 1.dp, if (isActive) colors.accent else colors.border),
                                RoundedCornerShape(10.dp)
                            )
                            .clickable {
                                tactile.perform(TactileType.LightTap)
                                onNodeClick(dn.id)
                            }
                            .padding(8.dp)
                    ) {
                        Column {
                            Text(
                                text = dn.label,
                                style = MaterialTheme.typography.bodySmall.copy(fontWeight = FontWeight.Bold, fontSize = 11.5.sp),
                                color = if (isActive) colors.accent else colors.titleText,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                            if (dn.desc.isNotBlank()) {
                                Text(
                                    text = dn.desc,
                                    style = MaterialTheme.typography.labelSmall.copy(fontSize = 10.sp),
                                    color = colors.secondaryText,
                                    maxLines = 2,
                                    overflow = TextOverflow.Ellipsis
                                )
                            }
                        }
                    }
                }
            }
        } else {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(6.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                dNodes.forEachIndexed { idx, dn ->
                    val isActive = dn.id == activeNodeId
                    Box(
                        modifier = Modifier
                            .widthIn(min = 100.dp, max = 135.dp)
                            .clip(RoundedCornerShape(10.dp))
                            .background(if (isActive) colors.accent.copy(alpha = 0.15f) else colors.surface)
                            .border(
                                BorderStroke(if (isActive) 1.5.dp else 1.dp, if (isActive) colors.accent else colors.border),
                                RoundedCornerShape(10.dp)
                            )
                            .clickable {
                                tactile.perform(TactileType.LightTap)
                                onNodeClick(dn.id)
                            }
                            .padding(8.dp)
                    ) {
                        Column {
                            Text(
                                text = dn.label,
                                style = MaterialTheme.typography.bodySmall.copy(fontWeight = FontWeight.Bold, fontSize = 11.5.sp),
                                color = if (isActive) colors.accent else colors.titleText,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                            if (dn.desc.isNotBlank()) {
                                Text(
                                    text = dn.desc,
                                    style = MaterialTheme.typography.labelSmall.copy(fontSize = 10.sp),
                                    color = colors.secondaryText,
                                    maxLines = 2,
                                    overflow = TextOverflow.Ellipsis
                                )
                            }
                        }
                    }

                    if (idx < dNodes.size - 1) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowForward,
                            contentDescription = null,
                            tint = colors.accent.copy(alpha = 0.6f),
                            modifier = Modifier.size(13.dp)
                        )
                    }
                }
            }
        }

        // Active node detail banner
        AnimatedVisibility(
            visible = activeNodeId != null,
            enter = fadeIn() + expandVertically(),
            exit = fadeOut() + shrinkVertically()
        ) {
            val activeItem = dNodes.find { it.id == activeNodeId }
            if (activeItem != null) {
                Surface(
                    shape = RoundedCornerShape(8.dp),
                    color = colors.accent.copy(alpha = 0.12f),
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 8.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(8.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "${activeItem.label}: ${activeItem.desc}. Tap again to collapse.",
                            style = MaterialTheme.typography.bodySmall.copy(fontSize = 11.5.sp),
                            color = colors.titleText,
                            modifier = Modifier.weight(1f)
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun ComparisonSectionRenderer(section: CanvasSection, colors: CanvasCardColorScheme) {
    val headers = section.headers ?: listOf("Aspect", "A", "B")
    val rows = section.rows ?: emptyList()

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .border(BorderStroke(1.dp, colors.border), RoundedCornerShape(12.dp))
    ) {
        section.title?.let { t ->
            Text(
                text = t,
                style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.Bold),
                color = colors.titleText,
                modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp)
            )
        }

        // Header
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .background(colors.headerBg)
                .padding(horizontal = 8.dp, vertical = 6.dp)
        ) {
            headers.forEach { h ->
                Text(
                    text = h,
                    style = MaterialTheme.typography.labelSmall.copy(fontWeight = FontWeight.Bold, fontSize = 10.5.sp),
                    color = colors.titleText,
                    modifier = Modifier.weight(1f)
                )
            }
        }

        // Rows
        rows.forEachIndexed { idx, row ->
            HorizontalDivider(color = colors.border.copy(alpha = 0.4f))
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(if (idx % 2 == 1) colors.innerCardBg else colors.surface)
                    .padding(horizontal = 8.dp, vertical = 6.dp)
            ) {
                row.forEachIndexed { colIdx, cell ->
                    Text(
                        text = cell,
                        style = MaterialTheme.typography.bodySmall.copy(
                            fontSize = 11.5.sp,
                            fontWeight = if (colIdx == 0) FontWeight.SemiBold else FontWeight.Normal
                        ),
                        color = colors.bodyText,
                        modifier = Modifier.weight(1f)
                    )
                }
            }
        }
    }
}

@Composable
private fun CardsGridRenderer(section: CanvasSection, colors: CanvasCardColorScheme) {
    val items = section.cardItems ?: emptyList()
    Column(modifier = Modifier.fillMaxWidth()) {
        section.title?.let { t ->
            Text(
                text = t,
                style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.Bold),
                color = colors.titleText,
                modifier = Modifier.padding(bottom = 6.dp)
            )
        }
        if (items.size <= 2) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items.forEach { card ->
                    Column(
                        modifier = Modifier
                            .weight(1f)
                            .clip(RoundedCornerShape(10.dp))
                            .background(colors.innerCardBg)
                            .border(BorderStroke(1.dp, colors.innerCardBorder), RoundedCornerShape(10.dp))
                            .padding(8.dp)
                    ) {
                        Text(
                            text = card.title,
                            style = MaterialTheme.typography.bodySmall.copy(fontWeight = FontWeight.Bold, fontSize = 12.sp),
                            color = colors.titleText
                        )
                        if (card.subtitle.isNotBlank()) {
                            Text(
                                text = card.subtitle,
                                style = MaterialTheme.typography.labelSmall.copy(fontSize = 10.5.sp),
                                color = colors.secondaryText
                            )
                        }
                        card.bullets.forEach { b ->
                            Row(
                                modifier = Modifier.padding(top = 4.dp),
                                horizontalArrangement = Arrangement.spacedBy(4.dp)
                            ) {
                                Text("•", color = colors.accent, style = MaterialTheme.typography.labelSmall)
                                Text(
                                    text = b,
                                    style = MaterialTheme.typography.labelSmall.copy(fontSize = 10.5.sp),
                                    color = colors.bodyText
                                )
                            }
                        }
                    }
                }
            }
        } else {
            Column(
                modifier = Modifier.fillMaxWidth(),
                verticalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                items.forEach { card ->
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(10.dp))
                            .background(colors.innerCardBg)
                            .border(BorderStroke(1.dp, colors.innerCardBorder), RoundedCornerShape(10.dp))
                            .padding(8.dp)
                    ) {
                        Text(
                            text = card.title,
                            style = MaterialTheme.typography.bodySmall.copy(fontWeight = FontWeight.Bold, fontSize = 12.sp),
                            color = colors.titleText
                        )
                        if (card.subtitle.isNotBlank()) {
                            Text(
                                text = card.subtitle,
                                style = MaterialTheme.typography.labelSmall.copy(fontSize = 10.5.sp),
                                color = colors.secondaryText
                            )
                        }
                        card.bullets.forEach { b ->
                            Row(
                                modifier = Modifier.padding(top = 4.dp),
                                horizontalArrangement = Arrangement.spacedBy(4.dp)
                            ) {
                                Text("•", color = colors.accent, style = MaterialTheme.typography.labelSmall)
                                Text(
                                    text = b,
                                    style = MaterialTheme.typography.labelSmall.copy(fontSize = 10.5.sp),
                                    color = colors.bodyText
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun BulletsListRenderer(section: CanvasSection, colors: CanvasCardColorScheme) {
    val items = section.bulletItems ?: emptyList()
    Column(modifier = Modifier.fillMaxWidth()) {
        section.title?.let { t ->
            Text(
                text = t,
                style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.Bold),
                color = colors.titleText,
                modifier = Modifier.padding(bottom = 4.dp)
            )
        }
        items.forEach { b ->
            Row(
                modifier = Modifier.padding(vertical = 2.dp),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                Text("•", color = colors.accent, fontWeight = FontWeight.Bold)
                Text(
                    text = b,
                    style = MaterialTheme.typography.bodySmall.copy(fontSize = 12.5.sp),
                    color = colors.bodyText
                )
            }
        }
    }
}

@Composable
private fun TimelineSectionRenderer(section: CanvasSection, colors: CanvasCardColorScheme) {
    val items = section.timelineItems ?: emptyList()
    Column(modifier = Modifier.fillMaxWidth()) {
        section.title?.let { t ->
            Text(
                text = t,
                style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.Bold),
                color = colors.titleText,
                modifier = Modifier.padding(bottom = 6.dp)
            )
        }
        items.forEach { tl ->
            Row(
                modifier = Modifier.padding(vertical = 3.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Box(
                    modifier = Modifier
                        .size(20.dp)
                        .clip(CircleShape)
                        .background(colors.accent.copy(alpha = 0.15f)),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = "${tl.number}",
                        style = MaterialTheme.typography.labelSmall.copy(fontWeight = FontWeight.Bold),
                        color = colors.accent
                    )
                }
                Column {
                    Text(
                        text = tl.title,
                        style = MaterialTheme.typography.bodySmall.copy(fontWeight = FontWeight.Bold, fontSize = 12.sp),
                        color = colors.titleText
                    )
                    if (tl.subtitle.isNotBlank()) {
                        Text(
                            text = tl.subtitle,
                            style = MaterialTheme.typography.labelSmall.copy(fontSize = 10.5.sp),
                            color = colors.secondaryText
                        )
                    }
                }
            }
        }
    }
}
