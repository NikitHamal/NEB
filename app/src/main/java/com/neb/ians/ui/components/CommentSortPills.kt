package com.neb.ians.ui.components

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

/**
 * Single shared sort-pill row for every comment list in the app
 * (forum replies, resource comments, news comments) so sorting looks
 * and behaves identically everywhere.
 *
 * Sort values: "oldest" | "newest" | "top".
 */
@Composable
fun CommentSortPillsRow(
    currentSort: String,
    onSelect: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    Row(modifier = modifier, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        CommentSortPill("Oldest", "oldest", currentSort, onSelect)
        CommentSortPill("Newest", "newest", currentSort, onSelect)
        CommentSortPill("Top", "top", currentSort, onSelect)
    }
}

@Composable
private fun CommentSortPill(
    label: String,
    value: String,
    currentSort: String,
    onSelect: (String) -> Unit
) {
    val selected = currentSort == value
    Surface(
        shape = WebPillShape,
        color = if (selected) MaterialTheme.colorScheme.secondaryContainer
        else MaterialTheme.colorScheme.surfaceContainerLow,
        modifier = Modifier.clip(WebPillShape).clickable { onSelect(value) }
    ) {
        Text(
            text = label,
            modifier = Modifier.padding(horizontal = 14.dp, vertical = 6.dp),
            style = MaterialTheme.typography.labelMedium,
            fontWeight = if (selected) FontWeight.SemiBold else FontWeight.Medium,
            color = if (selected) MaterialTheme.colorScheme.onSecondaryContainer
            else MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}
