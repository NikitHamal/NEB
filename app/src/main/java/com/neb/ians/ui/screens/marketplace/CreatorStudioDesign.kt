@file:OptIn(
    androidx.compose.material3.ExperimentalMaterial3Api::class,
    androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class
)

package com.neb.ians.ui.screens.marketplace

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.selection.selectable
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiCreatorChoice
import com.neb.ians.data.api.ApiCreatorTemplate
import com.neb.ians.ui.components.NebAuthField
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebFieldHint
import com.neb.ians.ui.components.NebToggleRow

/* The design half of the studio: where a page gets its look.
 *
 * A gallery before a blank canvas. Nobody's first storefront should be
 * twenty-five section names and no idea which of them they need -- a template
 * leaves a creator holding a page they could publish as it stands, and editing
 * down from something is far easier than building up from nothing.
 *
 * Every card paints itself in its own template's colours, because the colour is
 * the thing being chosen and a grey thumbnail of a teal page is worse than no
 * thumbnail at all. */


@Composable
internal fun StudioTemplateGallery(
    uiState: CreatorStudioUiState,
    viewModel: CreatorStudioViewModel
) {
    if (uiState.templates.isEmpty()) return
    StudioCard {
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Text(
                text = "Start from a template",
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.SemiBold,
                modifier = Modifier.weight(1f)
            )
            Text(
                text = "${uiState.templates.size} designs",
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        NebFieldHint("Finished pages. Pick one, then change anything you like.")
        LazyRow(
            horizontalArrangement = Arrangement.spacedBy(10.dp),
            contentPadding = PaddingValues(vertical = 2.dp)
        ) {
            uiState.templates.forEach { template ->
                item(key = template.id) {
                    StudioTemplateCard(template) { viewModel.previewTemplate(template) }
                }
            }
        }
        // What "use this template" means is asked *before* the confirm, not
        // inside it: the answer changes what a creator is risking, so it belongs
        // somewhere they can read it twice.
        StudioSegmented(
            label = "A template replaces",
            options = listOf(
                ApiCreatorChoice("page", "Whole page"),
                ApiCreatorChoice("theme", "Look only"),
                ApiCreatorChoice("sections", "Sections only")
            ),
            selected = uiState.templateMode,
            onSelect = viewModel::chooseTemplateMode,
            hint = when (uiState.templateMode) {
                "theme" -> "Repaints your page. Keeps every word you have written."
                "sections" -> "New sections, in the colours you already chose."
                else -> "Look and sections together. Best when you are starting out."
            }
        )
    }

    uiState.pendingTemplate?.let { template ->
        AlertDialog(
            onDismissRequest = viewModel::dismissTemplate,
            title = { Text("Use ${template.name}?") },
            text = {
                Text(
                    when (uiState.templateMode) {
                        "theme" -> "Your palette, type and spacing become ${template.name}'s. " +
                            "Your sections and everything you have written stay exactly as they are."
                        "sections" -> "Your sections are replaced with ${template.name}'s " +
                            "${template.sectionCount}, keeping your current colours. " +
                            "Anything you have typed into the old sections goes with them."
                        else -> "Your look and your sections both become ${template.name}'s " +
                            "${template.sectionCount} sections. Your name, address, contacts, " +
                            "courses and earnings are untouched."
                    }
                )
            },
            confirmButton = {
                TextButton(
                    onClick = viewModel::applyPendingTemplate,
                    enabled = !uiState.isApplyingTemplate
                ) { Text(if (uiState.isApplyingTemplate) "Applying…" else "Use template") }
            },
            dismissButton = { TextButton(onClick = viewModel::dismissTemplate) { Text("Cancel") } }
        )
    }
}

@Composable
private fun StudioTemplateCard(template: ApiCreatorTemplate, onClick: () -> Unit) {
    Column(
        modifier = Modifier
            .width(196.dp)
            .clip(RoundedCornerShape(16.dp))
            .background(MaterialTheme.colorScheme.surfaceContainerHigh)
            .border(1.dp, MaterialTheme.colorScheme.outlineVariant, RoundedCornerShape(16.dp))
            .selectable(selected = false, role = Role.Button, onClick = onClick)
            .padding(10.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        StudioTemplateThumb(template)
        Text(
            text = template.name,
            style = MaterialTheme.typography.titleSmall,
            fontWeight = FontWeight.SemiBold,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
        Text(
            text = template.summary,
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            maxLines = 2,
            overflow = TextOverflow.Ellipsis
        )
        Text(
            text = "${template.sectionCount} sections · ${template.bestFor}",
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
    }
}

/**
 * A miniature of the page the template makes.
 *
 * The same five shapes as the web's `.mkt-tt-*`: a hero band, an avatar, two
 * lines of type and a three-up shelf, drawn in the template's resolved colours
 * and reading its `hero` and `card` choices. It is not a real render — it is a
 * silhouette — but a silhouette in the right colours tells a creator which of
 * ten templates is the dark editorial one, which is the whole job.
 */
@Composable
private fun StudioTemplateThumb(template: ApiCreatorTemplate) {
    val accent = creatorAccent(template.colors.accent)
    val bg = creatorAccent(template.colors.bg)
    val surface = creatorAccent(template.colors.surface)
    val ink = creatorAccent(template.colors.ink)
    val muted = creatorAccent(template.colors.muted)
    val soft = creatorAccent(template.colors.soft)
    val line = creatorAccent(template.colors.line)
    val corner = when (template.style.radius) {
        "soft" -> 3.dp
        "sharp" -> 0.dp
        else -> 7.dp
    }
    val centred = template.style.hero == "center" || template.style.hero == "banner"

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .height(104.dp)
            .clip(RoundedCornerShape(10.dp))
            .background(bg)
            .border(1.dp, line, RoundedCornerShape(10.dp)),
        verticalArrangement = Arrangement.spacedBy(5.dp)
    ) {
        // The hero band: solid accent for `banner`, a soft wash for `art` and
        // `cover`, nothing at all for `plain`. Same three readings as the page.
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(if (template.style.hero == "plain") 10.dp else 32.dp)
                .background(
                    when (template.style.hero) {
                        "banner" -> accent
                        "plain" -> Color.Transparent
                        "gradient" -> soft
                        else -> soft
                    }
                )
        )
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 9.dp),
            horizontalAlignment = if (centred) Alignment.CenterHorizontally else Alignment.Start,
            verticalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(14.dp)
                    .clip(CircleShape)
                    .background(accent)
            )
            Box(
                modifier = Modifier
                    .width(if (centred) 64.dp else 78.dp)
                    .height(5.dp)
                    .clip(RoundedCornerShape(3.dp))
                    .background(ink)
            )
            Box(
                modifier = Modifier
                    .width(46.dp)
                    .height(4.dp)
                    .clip(RoundedCornerShape(3.dp))
                    .background(muted)
            )
            // The shelf, in the template's own card treatment: `outlined` and
            // `flat` are the two that read differently at this size.
            Row(horizontalArrangement = Arrangement.spacedBy(5.dp), modifier = Modifier.fillMaxWidth()) {
                repeat(3) {
                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .height(22.dp)
                            .clip(RoundedCornerShape(corner))
                            .background(if (template.style.card == "flat") soft else surface)
                            .then(
                                if (template.style.card == "outlined")
                                    Modifier.border(1.dp, line, RoundedCornerShape(corner))
                                else Modifier
                            )
                    )
                }
            }
        }
    }
}


/**
 * The Look card, built entirely from `editor_schema.theme`.
 *
 * Nine choices, every option visible. The previous version of this card offered
 * three of them behind scrolling chip rows, which is how a creator ends up
 * believing the app cannot do what the web can.
 */
@Composable
internal fun StudioLookCard(
    uiState: CreatorStudioUiState,
    viewModel: CreatorStudioViewModel
) {
    val theme = uiState.schema.theme
    StudioCard {
        Text(
            text = "Look",
            style = MaterialTheme.typography.titleSmall,
            fontWeight = FontWeight.SemiBold
        )
        NebFieldHint("Save, then open your page to see it. Everything here is reversible.")

        StudioFieldLabel("Palette")
        StudioPaletteRow(
            palettes = theme.palettes,
            selected = uiState.palette,
            onSelect = viewModel::updatePalette
        )

        StudioSegmented(
            label = "Page colours",
            options = theme.schemes,
            selected = uiState.scheme,
            onSelect = viewModel::updateScheme,
            hint = "A dark page stays dark for every visitor, whatever their own app theme says."
        )
        StudioSegmented(
            label = "Top of the page",
            options = theme.heroes,
            selected = uiState.heroStyle,
            onSelect = viewModel::updateHeroStyle
        )
        StudioSegmented(
            label = "Type",
            options = theme.fonts,
            selected = uiState.font,
            onSelect = viewModel::updateFont
        )
        StudioSegmented(
            label = "Texture",
            options = theme.patterns,
            selected = uiState.pattern,
            onSelect = viewModel::updatePattern
        )
        StudioSegmented(
            label = "Sections",
            options = theme.cards,
            selected = uiState.cardStyle,
            onSelect = viewModel::updateCardStyle
        )
        StudioSegmented(
            label = "Corners",
            options = theme.radii,
            selected = uiState.radius,
            onSelect = viewModel::updateRadius
        )
        StudioSegmented(
            label = "Spacing",
            options = theme.densities,
            selected = uiState.density,
            onSelect = viewModel::updateDensity
        )
        StudioSegmented(
            label = "Page width",
            options = theme.widths,
            selected = uiState.pageWidth,
            onSelect = viewModel::updatePageWidth
        )
        StudioSegmented(
            label = "Layout",
            options = uiState.schema.layouts,
            selected = uiState.layout,
            onSelect = viewModel::updateLayout
        )
        StudioSegmentedValues(
            label = "Gallery columns",
            options = listOf("2" to "2", "3" to "3", "4" to "4"),
            selected = uiState.galleryColumns.toString(),
            onSelect = { value -> viewModel.updateGalleryColumns(value.toIntOrNull() ?: 3) }
        )

        // The accent follows the palette until a creator overrides it, which is
        // what almost everybody wants. This field is here for the one who has a
        // brand colour, and the reset is here so overriding it is not a one-way
        // door.
        StudioFieldLabel("Accent colour")
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp), verticalAlignment = Alignment.CenterVertically) {
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .clip(CircleShape)
                    .background(creatorAccent(uiState.accentHex))
                    .border(1.dp, MaterialTheme.colorScheme.outlineVariant, CircleShape)
            )
            Box(modifier = Modifier.weight(1f)) {
                NebAuthField(
                    value = uiState.accentHex,
                    onValueChange = viewModel::updateAccent,
                    label = "Hex"
                )
            }
        }
        NebButton(
            text = "Use the palette's colour",
            onClick = viewModel::resetAccentToPalette,
            tone = NebButtonTone.Text,
            size = NebButtonSize.Small
        )

        NebToggleRow(
            title = "Lead with your numbers",
            subtitle = "Offerings, views and followers, under your name",
            checked = uiState.showStats,
            onCheckedChange = viewModel::updateShowStats
        )
        NebToggleRow(
            title = "Publish your contact details",
            subtitle = "Your email, phone and socials in the contact section",
            checked = uiState.showContact,
            onCheckedChange = viewModel::updateShowContact
        )
        NebToggleRow(
            title = "Show your verified badge",
            subtitle = "Only appears once we have verified you",
            checked = uiState.showVerified,
            onCheckedChange = viewModel::updateShowVerified
        )
        SaveRow(label = "Save look", saving = uiState.isSavingPage, onSave = viewModel::savePage)
    }
}
