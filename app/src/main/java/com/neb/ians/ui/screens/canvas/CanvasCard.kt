package com.neb.ians.ui.screens.canvas

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.animateFloatAsState
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
import androidx.compose.foundation.gestures.detectDragGesturesAfterLongPress
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
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.DragIndicator
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.outlined.AutoAwesome
import androidx.compose.material.icons.outlined.Close
import androidx.compose.material.icons.outlined.ContentCopy
import androidx.compose.material.icons.outlined.CropFree
import androidx.compose.material.icons.outlined.DeleteOutline
import androidx.compose.material.icons.outlined.Hub
import androidx.compose.material.icons.outlined.OpenInFull
import androidx.compose.material.icons.outlined.Palette
import androidx.compose.material3.*
import androidx.compose.material3.HorizontalDivider
import androidx.compose.runtime.*
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.ui.components.MarkdownInlineText
import com.neb.ians.ui.theme.nebFastSpatialSpec
import com.neb.ians.util.rememberTactileFeedback
import com.neb.ians.util.TactileType
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.foundation.verticalScroll

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
    onMeasured: (Float) -> Unit = {},
    modifier: Modifier = Modifier
) {
    val isDark = MaterialTheme.colorScheme.surface.luminance() < 0.5f
    val colors = canvasCardColors(node.color)
    val tactile = rememberTactileFeedback()
    var activeDiagNodeId by remember { mutableStateOf<String?>(null) }
    var followupText by remember { mutableStateOf("") }
    var showMoreMenu by remember { mutableStateOf(false) }
    var branchDirection by remember { mutableStateOf<String?>(null) }
    val composerFocus = remember { FocusRequester() }

    LaunchedEffect(isSelected) {
        if (!isSelected) branchDirection = null
    }

    val handleRadius = 20.dp
    val density = LocalDensity.current.density
    val bodyScroll = rememberScrollState()

    val currentOnDrag by rememberUpdatedState(onDrag)
    val currentOnDragEnd by rememberUpdatedState(onDragEnd)
    val currentOnSelect by rememberUpdatedState(onSelect)

    Box(
        modifier = modifier.offset(-handleRadius, -handleRadius)
    ) {
        // Card Surface
        Box(
            modifier = Modifier
                .padding(handleRadius)
                .width(CanvasCardWidth.dp)
                .onSizeChanged { onMeasured(it.height / density) }
                .shadow(
                    elevation = if (isSelected) 14.dp else 4.dp,
                    shape = RoundedCornerShape(20.dp),
                    spotColor = colors.accent.copy(alpha = 0.25f)
                )
                .clip(RoundedCornerShape(20.dp))
                .background(colors.surface)
                .drawBehind {
                    drawRoundRect(
                        color = colors.accent,
                        topLeft = Offset.Zero,
                        size = Size(4.dp.toPx(), size.height),
                        cornerRadius = CornerRadius(2.dp.toPx(), 2.dp.toPx())
                    )
                }
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
                        currentOnSelect()
                    })
                }
                .pointerInput(node.id) {
                    detectDragGesturesAfterLongPress(
                        onDragStart = {
                            tactile.perform(TactileType.LightTap)
                            currentOnSelect()
                        },
                        onDrag = { change, dragAmount ->
                            change.consume()
                            currentOnDrag(dragAmount.x, dragAmount.y)
                        },
                        onDragEnd = { currentOnDragEnd() },
                        onDragCancel = { currentOnDragEnd() }
                    )
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
                                currentOnSelect()
                            },
                            onDrag = { change, dragAmount ->
                                change.consume()
                                currentOnDrag(dragAmount.x, dragAmount.y)
                            },
                            onDragEnd = { currentOnDragEnd() },
                            onDragCancel = { currentOnDragEnd() }
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
                            Text(
                                text = "Card theme",
                                style = MaterialTheme.typography.labelMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier.padding(start = 14.dp, top = 10.dp, bottom = 6.dp)
                            )
                            CanvasColorTokens.Keys.forEach { key ->
                                DropdownMenuItem(
                                    text = { Text(CanvasColorTokens.label(key)) },
                                    leadingIcon = {
                                        Box(
                                            modifier = Modifier
                                                .size(18.dp)
                                                .clip(RoundedCornerShape(6.dp))
                                                .background(CanvasColorTokens.accent(MaterialTheme.colorScheme, key))
                                        )
                                    },
                                    trailingIcon = {
                                        if (node.color.equals(key, ignoreCase = true)) {
                                            Icon(
                                                imageVector = Icons.Filled.Check,
                                                contentDescription = null,
                                                modifier = Modifier.size(16.dp)
                                            )
                                        }
                                    },
                                    onClick = {
                                        onColorChange(key)
                                        showMoreMenu = false
                                    }
                                )
                            }
                            HorizontalDivider(modifier = Modifier.padding(vertical = 6.dp))
                            DropdownMenuItem(
                                text = { Text("Link to another card") },
                                leadingIcon = {
                                    Icon(
                                        imageVector = Icons.Outlined.Hub,
                                        contentDescription = null,
                                        modifier = Modifier.size(18.dp)
                                    )
                                },
                                onClick = {
                                    showMoreMenu = false
                                    onConnect("link")
                                }
                            )
                        }
                    }
                }
            }

            // Body
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(max = CanvasCardMaxBodyHeight.dp)
                    .verticalScroll(bodyScroll)
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

            // Branch composer: turns this card into the context for a new one
            if (node.status != "generating") {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 12.dp, vertical = 8.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    AnimatedVisibility(visible = branchDirection != null) {
                        Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.spacedBy(6.dp)
                            ) {
                                Icon(
                                    imageVector = Icons.Outlined.AutoAwesome,
                                    contentDescription = null,
                                    tint = colors.accent,
                                    modifier = Modifier.size(13.dp)
                                )
                                Text(
                                    text = "New card ${directionLabel(branchDirection)} from this one",
                                    style = MaterialTheme.typography.labelSmall.copy(fontSize = 10.5.sp),
                                    color = colors.secondaryText,
                                    modifier = Modifier.weight(1f)
                                )
                                IconButton(
                                    onClick = { branchDirection = null },
                                    modifier = Modifier.size(18.dp)
                                ) {
                                    Icon(
                                        imageVector = Icons.Filled.Close,
                                        contentDescription = "Cancel branch",
                                        tint = colors.secondaryText,
                                        modifier = Modifier.size(12.dp)
                                    )
                                }
                            }
                            Row(
                                modifier = Modifier.horizontalScroll(rememberScrollState()),
                                horizontalArrangement = Arrangement.spacedBy(6.dp)
                            ) {
                                BranchPresets.forEach { preset ->
                                    BranchPresetChip(
                                        label = preset.first,
                                        colors = colors,
                                        onClick = {
                                            onBranch(branchDirection ?: "bottom", preset.second)
                                            branchDirection = null
                                            followupText = ""
                                        }
                                    )
                                }
                            }
                        }
                    }
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
                            modifier = Modifier
                                .weight(1f)
                                .focusRequester(composerFocus),
                            singleLine = true,
                            maxLines = 1,
                            textStyle = MaterialTheme.typography.bodySmall.copy(
                                fontSize = 12.sp,
                                color = colors.titleText
                            ),
                            decorationBox = { innerTextField ->
                                if (followupText.isEmpty()) {
                                    Text(
                                        text = if (branchDirection == null) {
                                            "Ask a follow-up..."
                                        } else {
                                            "What should the new card cover?"
                                        },
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
                                    onBranch(branchDirection ?: "bottom", followupText.trim())
                                    followupText = ""
                                    branchDirection = null
                                }
                            },
                            enabled = hasFollowup,
                            modifier = Modifier
                                .size(28.dp)
                                .clip(CircleShape)
                                .background(
                                    if (hasFollowup) colors.accent
                                    else if (isDark) Color(0xFF26262A)
                                    else Color(0xFFF1F1F3)
                                )
                        ) {
                            Icon(
                                imageVector = Icons.Filled.ArrowUpward,
                                contentDescription = "Send",
                                tint = if (hasFollowup) colors.surface else Color(0xFF9B9BA1),
                                modifier = Modifier.size(14.dp)
                            )
                        }
                    }
                }
            }
        }
    }

        if (isSelected || isConnectingSource) {
            listOf(
                "top" to Alignment.TopCenter,
                "bottom" to Alignment.BottomCenter,
                "left" to Alignment.CenterStart,
                "right" to Alignment.CenterEnd
            ).forEach { (dir, alignment) ->
                BranchPort(
                    accent = colors.accent,
                    surfaceColor = colors.surface,
                    isActive = branchDirection == dir,
                    modifier = Modifier
                        .align(alignment)
                        .offset(
                            x = when (dir) {
                                "left" -> 8.dp
                                "right" -> (-8).dp
                                else -> 0.dp
                            },
                            y = when (dir) {
                                "top" -> 8.dp
                                "bottom" -> (-8).dp
                                else -> 0.dp
                            }
                        ),
                    onClick = {
                        onSelect()
                        branchDirection = if (branchDirection == dir) null else dir
                    }
                )
            }
        }
    }

    LaunchedEffect(branchDirection) {
        if (branchDirection != null) {
            runCatching { composerFocus.requestFocus() }
        }
    }
}

private val BranchPresets = listOf(
    "Go deeper" to "Explain this in more depth, building on the card above.",
    "Example" to "Give a worked example based on the card above.",
    "Simplify" to "Explain the card above in the simplest possible terms.",
    "Practice" to "Create practice questions from the card above.",
    "Mistakes" to "List the common mistakes students make with the card above."
)

private fun directionLabel(direction: String?): String = when (direction) {
    "top" -> "above"
    "left" -> "to the left"
    "right" -> "to the right"
    else -> "below"
}

@Composable
private fun BranchPresetChip(
    label: String,
    colors: CanvasCardColorScheme,
    onClick: () -> Unit
) {
    Text(
        text = label,
        style = MaterialTheme.typography.labelSmall.copy(fontSize = 10.5.sp, fontWeight = FontWeight.Medium),
        color = colors.tagText,
        modifier = Modifier
            .clip(RoundedCornerShape(99.dp))
            .background(colors.tagBg)
            .clickable(onClick = onClick)
            .padding(horizontal = 10.dp, vertical = 5.dp)
    )
}

@Composable
private fun BranchPort(
    accent: Color,
    surfaceColor: Color,
    isActive: Boolean,
    modifier: Modifier = Modifier,
    onClick: () -> Unit
) {
    val tactile = rememberTactileFeedback()
    val scale by animateFloatAsState(
        targetValue = if (isActive) 1.18f else 1f,
        animationSpec = nebFastSpatialSpec(),
        label = "branch_port_scale"
    )
    val rotation by animateFloatAsState(
        targetValue = if (isActive) 45f else 0f,
        animationSpec = nebFastSpatialSpec(),
        label = "branch_port_rotation"
    )

    Box(
        modifier = modifier
            .size(26.dp)
            .graphicsLayer {
                scaleX = scale
                scaleY = scale
            }
            .shadow(elevation = if (isActive) 6.dp else 2.dp, shape = CircleShape)
            .clip(CircleShape)
            .background(if (isActive) accent else surfaceColor)
            .border(BorderStroke(if (isActive) 2.dp else 1.5.dp, accent), CircleShape)
            .clickable(onClick = {
                tactile.perform(TactileType.SelectionChange)
                onClick()
            }),
        contentAlignment = Alignment.Center
    ) {
        Icon(
            imageVector = Icons.Filled.Add,
            contentDescription = "New card from this one",
            tint = if (isActive) surfaceColor else accent,
            modifier = Modifier
                .size(14.dp)
                .graphicsLayer { rotationZ = rotation }
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
                                BulletRule(color = colors.accent, topPadding = 6.dp)
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
                                BulletRule(color = colors.accent, topPadding = 6.dp)
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
                BulletRule(color = colors.accent, topPadding = 8.dp)
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

@Composable
private fun BulletRule(color: Color, topPadding: Dp) {
    Box(
        modifier = Modifier
            .padding(top = topPadding)
            .width(7.dp)
            .height(1.5.dp)
            .background(color)
    )
}
