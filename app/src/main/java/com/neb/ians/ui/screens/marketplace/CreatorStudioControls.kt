@file:OptIn(
    androidx.compose.material3.ExperimentalMaterial3Api::class,
    androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class,
    androidx.compose.foundation.layout.ExperimentalLayoutApi::class
)

package com.neb.ians.ui.screens.marketplace

import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.selection.selectable
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.BrokenImage
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.Image
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import coil.compose.AsyncImagePainter
import com.neb.ians.data.api.ApiCreatorChoice
import com.neb.ians.data.api.ApiCreatorPaletteChoice
import com.neb.ians.ui.components.NebAuthField
import com.neb.ians.ui.components.NebFieldHint
import com.neb.ians.ui.components.WebCardShape

/* The controls the rebuilt studio is assembled from.
 *
 * Three rules run through all of them, and they are the reason this file exists
 * rather than the controls being inlined where they are used:
 *
 *  1. Every tap target is at least 44dp. A studio is used one-handed, standing
 *     up, and a 24dp icon button is a control you miss.
 *  2. Nothing is hidden behind hover or a long-press alone. Where a gesture is
 *     the fast path there is always a visible control that does the same thing
 *     (WCAG 2.5.1), because a gesture nobody discovers is a feature nobody has.
 *  3. Options come from the server's `editor_schema`, never from a list written
 *     out here. A list written out here is a list that disagrees with the web
 *     studio by the end of the month. */


/**
 * One choice out of a handful, all of them visible.
 *
 * The web's `.mkt-seg`, and chosen over a dropdown for the same reason: with
 * four options a dropdown hides three of them behind a tap and tells the
 * creator nothing about what they are choosing between. It wraps rather than
 * scrolls, so the fourth option is never just off the edge of a phone.
 */
@Composable
internal fun StudioSegmented(
    label: String,
    options: List<ApiCreatorChoice>,
    selected: String,
    onSelect: (String) -> Unit,
    hint: String? = null
) {
    if (options.isEmpty()) return
    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
        StudioFieldLabel(label)
        FlowRow(
            horizontalArrangement = Arrangement.spacedBy(6.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            options.forEach { option ->
                val isOn = option.id == selected
                val background by animateColorAsState(
                    if (isOn) MaterialTheme.colorScheme.secondaryContainer
                    else MaterialTheme.colorScheme.surfaceContainerHigh,
                    label = "segment"
                )
                Row(
                    modifier = Modifier
                        .heightIn(min = 44.dp)
                        .clip(RoundedCornerShape(12.dp))
                        .background(background)
                        .then(
                            if (isOn) Modifier.border(
                                1.5.dp,
                                MaterialTheme.colorScheme.primary,
                                RoundedCornerShape(12.dp)
                            ) else Modifier
                        )
                        .selectable(
                            selected = isOn,
                            role = Role.RadioButton,
                            onClick = { onSelect(option.id) }
                        )
                        .padding(horizontal = 14.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(5.dp)
                ) {
                    if (isOn) {
                        Icon(
                            imageVector = Icons.Outlined.Check,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.primary,
                            modifier = Modifier.size(15.dp)
                        )
                    }
                    Text(
                        text = option.label,
                        style = MaterialTheme.typography.labelLarge,
                        fontWeight = if (isOn) FontWeight.SemiBold else FontWeight.Normal
                    )
                }
            }
        }
        hint?.let { NebFieldHint(it) }
    }
}

/** The same control over plain strings, for the few lists the schema does not
 *  carry (gallery columns, and a section's column count). */
@Composable
internal fun StudioSegmentedValues(
    label: String,
    options: List<Pair<String, String>>,
    selected: String,
    onSelect: (String) -> Unit,
    hint: String? = null
) = StudioSegmented(
    label = label,
    options = options.map { ApiCreatorChoice(id = it.first, label = it.second) },
    selected = selected,
    onSelect = onSelect,
    hint = hint
)

@Composable
internal fun StudioFieldLabel(text: String) {
    Text(
        text = text,
        style = MaterialTheme.typography.labelLarge,
        fontWeight = FontWeight.SemiBold,
        color = MaterialTheme.colorScheme.onSurface
    )
}


/**
 * The palette picker: the colour itself, at a size you can judge.
 *
 * A palette is chosen by eye, so each swatch shows the accent over the tint it
 * comes with rather than a name and a dot. Names stay, because "the teal one"
 * is how a creator will describe it to somebody else.
 */
@Composable
internal fun StudioPaletteRow(
    palettes: List<ApiCreatorPaletteChoice>,
    selected: String,
    onSelect: (String) -> Unit
) {
    if (palettes.isEmpty()) return
    FlowRow(
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        palettes.forEach { entry ->
            val isOn = entry.id == selected
            val accent = creatorAccent(entry.accent)
            Column(
                modifier = Modifier
                    .width(78.dp)
                    .clip(RoundedCornerShape(14.dp))
                    .background(MaterialTheme.colorScheme.surfaceContainerHigh)
                    .then(
                        if (isOn) Modifier.border(2.dp, accent, RoundedCornerShape(14.dp))
                        else Modifier
                    )
                    .selectable(
                        selected = isOn,
                        role = Role.RadioButton,
                        onClick = { onSelect(entry.id) }
                    )
                    .padding(8.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(34.dp)
                        .clip(RoundedCornerShape(9.dp))
                        .background(creatorAccent(entry.soft)),
                    contentAlignment = Alignment.Center
                ) {
                    Box(
                        modifier = Modifier
                            .size(20.dp)
                            .clip(CircleShape)
                            .background(accent)
                    )
                    if (isOn) {
                        Icon(
                            imageVector = Icons.Outlined.Check,
                            contentDescription = null,
                            tint = Color.White,
                            modifier = Modifier.size(14.dp)
                        )
                    }
                }
                Text(
                    text = entry.label,
                    style = MaterialTheme.typography.labelSmall,
                    fontWeight = if (isOn) FontWeight.Bold else FontWeight.Normal,
                    textAlign = TextAlign.Center,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }
    }
}


/** How a picture field draws its preview. */
internal enum class StudioImageShape { Round, Wide, Square }

/**
 * A picture field that shows the picture.
 *
 * The old studio asked for "AVATAR IMAGE URL" and showed nothing, so a creator
 * pasted a link, saved, opened their page and found out. This shows it
 * immediately, at the shape it will actually be used at, and says so plainly
 * when the link does not load — which is nearly always a typo or a host that
 * blocks hotlinking, and both are worth knowing before publishing.
 */
@Composable
internal fun StudioImageField(
    label: String,
    value: String,
    onValueChange: (String) -> Unit,
    shape: StudioImageShape,
    hint: String? = null
) {
    var failed by remember(value) { mutableStateOf(false) }
    val previewShape = when (shape) {
        StudioImageShape.Round -> CircleShape
        StudioImageShape.Wide -> RoundedCornerShape(10.dp)
        StudioImageShape.Square -> RoundedCornerShape(12.dp)
    }
    Row(horizontalArrangement = Arrangement.spacedBy(12.dp), modifier = Modifier.fillMaxWidth()) {
        Box(
            modifier = Modifier
                .then(
                    when (shape) {
                        StudioImageShape.Wide -> Modifier.width(84.dp).height(56.dp)
                        else -> Modifier.size(56.dp)
                    }
                )
                .clip(previewShape)
                .background(
                    if (failed) MaterialTheme.colorScheme.errorContainer
                    else MaterialTheme.colorScheme.surfaceContainerHigh
                ),
            contentAlignment = Alignment.Center
        ) {
            if (value.isNotBlank() && !failed) {
                AsyncImage(
                    model = value,
                    contentDescription = null,
                    contentScale = ContentScale.Crop,
                    onState = { state -> if (state is AsyncImagePainter.State.Error) failed = true },
                    modifier = Modifier.fillMaxSize()
                )
            } else {
                Icon(
                    imageVector = if (failed) Icons.Outlined.BrokenImage else Icons.Outlined.Image,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.size(20.dp)
                )
            }
        }
        Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(4.dp)) {
            NebAuthField(
                value = value,
                onValueChange = onValueChange,
                label = label,
                placeholder = "https://…",
                keyboardType = KeyboardType.Uri
            )
            when {
                failed -> NebFieldHint("That link did not load. Check it, or try a different host.")
                hint != null -> NebFieldHint(hint)
            }
        }
    }
}


/** A small square button, at a size a thumb actually hits. */
@Composable
internal fun StudioIconButton(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    contentDescription: String,
    onClick: () -> Unit,
    enabled: Boolean = true,
    tint: Color? = null
) {
    Box(
        modifier = Modifier
            .size(44.dp)
            .clip(WebCardShape)
            .then(
                if (enabled) Modifier.clickable(onClickLabel = contentDescription, onClick = onClick)
                else Modifier
            ),
        contentAlignment = Alignment.Center
    ) {
        Icon(
            imageVector = icon,
            contentDescription = contentDescription,
            tint = when {
                !enabled -> MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.38f)
                tint != null -> tint
                else -> MaterialTheme.colorScheme.onSurfaceVariant
            },
            modifier = Modifier.size(19.dp)
        )
    }
}
