package com.neb.ians.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Text
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.theme.LocalNebAuthPalette
import com.neb.ians.ui.theme.NebAuthTokens

// ---------------------------------------------------------------------------
// Choosing from a long list is a sheet, never a dialog. A dialog crops the list
// to a box in the middle of the screen and leaves the thumb nowhere useful; a
// sheet starts at the bottom, where the hand already is, and can take a search
// field without the keyboard covering the results.
// ---------------------------------------------------------------------------

/** The chrome every NEB sheet shares: handle, title, gutters, insets. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NebSheetSurface(
    title: String,
    onDismiss: () -> Unit,
    modifier: Modifier = Modifier,
    subtitle: String? = null,
    content: @Composable ColumnScope.() -> Unit
) {
    val palette = LocalNebAuthPalette.current
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = sheetState,
        containerColor = palette.page,
        contentColor = palette.ink,
        scrimColor = palette.artInk.copy(alpha = 0.34f),
        shape = RoundedCornerShape(topStart = 28.dp, topEnd = 28.dp),
        dragHandle = {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 12.dp, bottom = 2.dp),
                contentAlignment = Alignment.Center
            ) {
                Box(
                    modifier = Modifier
                        .width(38.dp)
                        .height(4.dp)
                        .clip(RoundedCornerShape(2.dp))
                        .background(palette.hairlineStrong)
                )
            }
        }
    ) {
        Column(
            modifier = modifier
                .fillMaxWidth()
                .padding(horizontal = NebAuthTokens.PageGutter)
                .imePadding()
                .navigationBarsPadding()
        ) {
            Spacer(modifier = Modifier.height(6.dp))
            Text(text = title, style = NebAuthType.Title, color = palette.ink)
            if (subtitle != null) {
                Spacer(modifier = Modifier.height(4.dp))
                Text(text = subtitle, style = NebAuthType.Caption, color = palette.inkMuted)
            }
            Spacer(modifier = Modifier.height(16.dp))
            content()
            Spacer(modifier = Modifier.height(20.dp))
        }
    }
}

/** One selectable line in a sheet. The mark on the right is the only ornament. */
@Composable
fun NebPickerRow(
    label: String,
    selected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    supporting: String? = null,
    leading: (@Composable () -> Unit)? = null
) {
    val palette = LocalNebAuthPalette.current
    Row(
        modifier = modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(14.dp))
            .nebPressable(onClick = onClick)
            .padding(horizontal = 12.dp, vertical = 13.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        if (leading != null) {
            leading()
            Spacer(modifier = Modifier.width(12.dp))
        }
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = label,
                style = NebAuthType.Body,
                color = if (selected) palette.sapphire else palette.ink
            )
            if (supporting != null) {
                Spacer(modifier = Modifier.height(2.dp))
                Text(text = supporting, style = NebAuthType.Caption, color = palette.inkFaint)
            }
        }
        Spacer(modifier = Modifier.width(10.dp))
        NebSelectionMark(selected = selected, diameter = 22.dp)
    }
}

/**
 * A list of plain strings to pick one of, with an optional filter. Used for
 * gender, class, province, district and anything else with a fixed catalogue.
 */
@Composable
fun NebPickerSheet(
    title: String,
    options: List<String>,
    selected: String?,
    onSelect: (String) -> Unit,
    onDismiss: () -> Unit,
    searchable: Boolean = options.size > 12,
    searchPlaceholder: String = "Search"
) {
    NebSheetSurface(title = title, onDismiss = onDismiss) {
        var query by remember { mutableStateOf("") }
        val shown = remember(query, options) {
            if (query.isBlank()) options else options.filter { it.contains(query.trim(), ignoreCase = true) }
        }

        if (searchable) {
            NebAuthField(
                value = query,
                onValueChange = { query = it },
                label = "",
                placeholder = searchPlaceholder,
                leadingIcon = Icons.Outlined.Search
            )
            Spacer(modifier = Modifier.height(10.dp))
        }

        LazyColumn(modifier = Modifier.fillMaxWidth().heightIn(max = 392.dp)) {
            items(shown, key = { it }) { option ->
                NebPickerRow(
                    label = option,
                    selected = option == selected,
                    onClick = {
                        onSelect(option)
                        onDismiss()
                    }
                )
            }
        }

        if (shown.isEmpty()) {
            Text(
                text = "Nothing matches “${query.trim()}”.",
                style = NebAuthType.Caption,
                color = LocalNebAuthPalette.current.inkFaint,
                modifier = Modifier.padding(horizontal = 12.dp, vertical = 14.dp)
            )
        }
    }
}
