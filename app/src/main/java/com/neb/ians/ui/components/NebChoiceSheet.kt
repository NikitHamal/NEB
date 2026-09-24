@file:OptIn(
    androidx.compose.material3.ExperimentalMaterial3Api::class,
    androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class,
    androidx.compose.foundation.layout.ExperimentalLayoutApi::class
)

package com.neb.ians.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.KeyboardArrowRight
import androidx.compose.material.icons.rounded.Add
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material.icons.rounded.Search
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
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp

/**
 * One answer on a form, shown as the answer rather than as an empty box.
 *
 * Every picker built on this is the same row: what it is on the left, what you
 * chose underneath it as chips, a chevron at the end. Nothing pretends to be a
 * text field the user can type into.
 */
@Composable
fun NebSelectField(
    label: String,
    values: List<String>,
    placeholder: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    icon: ImageVector? = null,
    isError: Boolean = false,
    errorText: String = "Required"
) {
    val shape = RoundedCornerShape(20.dp)
    val edge = if (isError) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.outlineVariant

    Column(modifier = modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .nebPressable(onClick = onClick)
                .clip(shape)
                .background(MaterialTheme.colorScheme.surfaceContainerLow)
                .border(1.dp, edge, shape)
                .padding(start = 14.dp, end = 12.dp, top = 12.dp, bottom = 12.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            if (icon != null) {
                Box(
                    modifier = Modifier
                        .size(38.dp)
                        .clip(RoundedCornerShape(13.dp))
                        .background(MaterialTheme.colorScheme.surfaceContainerHighest),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = icon,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurface,
                        modifier = Modifier.size(19.dp)
                    )
                }
            }
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = label,
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(modifier = Modifier.height(if (values.isEmpty()) 1.dp else 6.dp))
                if (values.isEmpty()) {
                    Text(
                        text = placeholder,
                        style = MaterialTheme.typography.bodyLarge,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                } else {
                    FlowRow(
                        horizontalArrangement = Arrangement.spacedBy(6.dp),
                        verticalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        values.take(6).forEach { value ->
                            ValuePill(value)
                        }
                        if (values.size > 6) ValuePill("+${values.size - 6}")
                    }
                }
            }
            Icon(
                imageVector = Icons.AutoMirrored.Rounded.KeyboardArrowRight,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.size(20.dp)
            )
        }
        AnimatedVisibility(visible = isError) {
            Text(
                text = errorText,
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.error,
                modifier = Modifier.padding(start = 16.dp, top = 5.dp)
            )
        }
    }
}

@Composable
private fun ValuePill(text: String) {
    Text(
        text = text,
        style = MaterialTheme.typography.labelLarge,
        color = MaterialTheme.colorScheme.onSurface,
        maxLines = 1,
        overflow = TextOverflow.Ellipsis,
        modifier = Modifier
            .clip(RoundedCornerShape(50))
            .background(MaterialTheme.colorScheme.surfaceContainerHighest)
            .padding(horizontal = 10.dp, vertical = 4.dp)
    )
}

/**
 * The list of possible answers, as a sheet full of chips.
 *
 * A sheet rather than a dialog because the thumb is at the bottom of the phone,
 * and chips rather than a checklist because a subject is two words and forty of
 * them fit on one screen that way. Anything not on the list can be typed in.
 */
@Composable
fun NebChoiceSheet(
    title: String,
    options: List<String>,
    selected: List<String>,
    multiSelect: Boolean,
    onDismiss: () -> Unit,
    onConfirm: (List<String>) -> Unit,
    subtitle: String? = null,
    allowCustom: Boolean = false,
    customPlaceholder: String = "Add your own",
    onAddCustom: (String) -> Unit = {}
) {
    var picked by remember { mutableStateOf(selected) }
    var query by remember { mutableStateOf("") }
    var custom by remember { mutableStateOf("") }

    val visible = remember(options, query, picked) {
        val all = (picked + options).distinct()
        if (query.isBlank()) all else all.filter { it.contains(query.trim(), ignoreCase = true) }
    }

    fun addCustom() {
        val trimmed = custom.trim()
        if (trimmed.isBlank()) return
        custom = ""
        onAddCustom(trimmed)
        if (multiSelect) {
            if (picked.none { it.equals(trimmed, ignoreCase = true) }) picked = picked + trimmed
        } else {
            onConfirm(listOf(trimmed))
        }
    }

    NebModalSheet(
        onDismiss = onDismiss,
        title = title,
        subtitle = subtitle,
        showClose = true
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 22.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            if (options.size >= 10) {
                SheetSearchField(value = query, onValueChange = { query = it })
            }

            FlowRow(
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(max = 300.dp)
                    .verticalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                visible.forEach { option ->
                    val isOn = picked.any { it.equals(option, ignoreCase = true) }
                    NebFilterChip(
                        label = option,
                        selected = isOn,
                        onClick = {
                            picked = when {
                                !multiSelect -> listOf(option)
                                isOn -> picked.filterNot { it.equals(option, ignoreCase = true) }
                                else -> picked + option
                            }
                            if (!multiSelect) onConfirm(listOf(option))
                        }
                    )
                }
                if (visible.isEmpty()) {
                    Text(
                        text = "Nothing matches “${query.trim()}”.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }

            if (allowCustom) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    SheetInlineField(
                        value = custom,
                        onValueChange = { custom = it },
                        placeholder = customPlaceholder,
                        leading = Icons.Rounded.Add,
                        onSubmit = { addCustom() },
                        modifier = Modifier.weight(1f)
                    )
                    NebButton(
                        text = "Add",
                        onClick = { addCustom() },
                        size = NebButtonSize.Small,
                        tone = NebButtonTone.Tonal,
                        enabled = custom.isNotBlank()
                    )
                }
            }

            if (multiSelect) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    NebButton(
                        text = "Clear",
                        onClick = { picked = emptyList() },
                        tone = NebButtonTone.Text,
                        size = NebButtonSize.Small,
                        enabled = picked.isNotEmpty()
                    )
                    Spacer(modifier = Modifier.weight(1f))
                    NebButton(
                        text = if (picked.isEmpty()) "Done" else "Done (${picked.size})",
                        onClick = { onConfirm(picked) },
                        size = NebButtonSize.Small
                    )
                }
            }
        }
    }
}

@Composable
private fun SheetSearchField(value: String, onValueChange: (String) -> Unit) {
    SheetInlineField(
        value = value,
        onValueChange = onValueChange,
        placeholder = "Search",
        leading = Icons.Rounded.Search,
        onSubmit = {},
        trailing = {
            if (value.isNotEmpty()) {
                Box(
                    modifier = Modifier
                        .size(22.dp)
                        .nebPressable(onClick = { onValueChange("") })
                        .clip(RoundedCornerShape(50))
                        .background(MaterialTheme.colorScheme.surfaceContainerHighest),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = Icons.Rounded.Close,
                        contentDescription = "Clear search",
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.size(14.dp)
                    )
                }
            }
        }
    )
}

@Composable
private fun SheetInlineField(
    value: String,
    onValueChange: (String) -> Unit,
    placeholder: String,
    leading: ImageVector,
    onSubmit: () -> Unit,
    modifier: Modifier = Modifier,
    trailing: (@Composable () -> Unit)? = null
) {
    val shape = RoundedCornerShape(50)
    Row(
        modifier = modifier
            .fillMaxWidth()
            .height(48.dp)
            .clip(shape)
            .background(MaterialTheme.colorScheme.surfaceContainerHigh)
            .border(1.dp, MaterialTheme.colorScheme.outlineVariant, shape)
            .padding(horizontal = 14.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Icon(
            imageVector = leading,
            contentDescription = null,
            tint = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.size(18.dp)
        )
        Box(modifier = Modifier.weight(1f), contentAlignment = Alignment.CenterStart) {
            if (value.isEmpty()) {
                Text(
                    text = placeholder,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
            BasicTextField(
                value = value,
                onValueChange = onValueChange,
                singleLine = true,
                textStyle = MaterialTheme.typography.bodyMedium.copy(
                    color = MaterialTheme.colorScheme.onSurface
                ),
                cursorBrush = SolidColor(MaterialTheme.colorScheme.onSurface),
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done),
                modifier = Modifier.fillMaxWidth()
            )
        }
        if (trailing != null) {
            trailing()
        } else if (value.isNotBlank()) {
            Box(
                modifier = Modifier
                    .size(22.dp)
                    .nebPressable(onClick = onSubmit)
                    .clip(RoundedCornerShape(50))
                    .background(MaterialTheme.colorScheme.surfaceContainerHighest),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Rounded.Add,
                    contentDescription = "Add",
                    tint = MaterialTheme.colorScheme.onSurface,
                    modifier = Modifier.size(14.dp)
                )
            }
        }
        Spacer(modifier = Modifier.width(0.dp))
    }
}
