@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.screens.marketplace

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.ArrowDownward
import androidx.compose.material.icons.outlined.ArrowUpward
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material.icons.outlined.VisibilityOff
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiCreatorBlockItem
import com.neb.ians.ui.components.NebAuthField
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.WebCardShape
import com.neb.ians.ui.components.WebPanelShape

/** Where the studio's editors live. Shared with the studio screen. */

/** `BLOCK_LABELS` on the server, for the places a row is drawn before the
 *  schema has arrived. Where the schema is already in hand — the picker and the
 *  editor sheet — its own label wins, so a section renamed on the server is
 *  renamed here without an app release. */
internal fun blockLabel(type: String): String = when (type) {
    "hero" -> "Hero"
    "about" -> "About"
    "stats" -> "Numbers"
    "courses" -> "Courses"
    "resources" -> "Resources"
    "posts" -> "Updates"
    "showcase" -> "Showcase"
    "gallery" -> "Gallery"
    "testimonials" -> "Testimonials"
    "faq" -> "FAQ"
    "schedule" -> "Schedule"
    "links" -> "Links"
    "contact" -> "Contact"
    "cta" -> "Call to action"
    "documents" -> "Documents"
    "pricing" -> "Pricing"
    "video" -> "Video"
    "team" -> "Team"
    "logos" -> "Partners"
    "timeline" -> "Milestones"
    "steps" -> "How it works"
    "quote" -> "Pull quote"
    "banner" -> "Announcement"
    "richtext" -> "Text and image"
    "divider" -> "Divider"
    else -> type.replaceFirstChar { it.uppercase() }
}

@Composable
internal fun StudioCard(content: @Composable ColumnScope.() -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(WebPanelShape)
            .background(MaterialTheme.colorScheme.surfaceContainerLowest)
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp),
        content = content
    )
}

@Composable
internal fun SaveRow(label: String, saving: Boolean, onSave: () -> Unit) {
    NebButton(
        text = label,
        onClick = onSave,
        tone = NebButtonTone.Primary,
        size = NebButtonSize.Standard,
        loading = saving,
        fillWidth = true
    )
}
