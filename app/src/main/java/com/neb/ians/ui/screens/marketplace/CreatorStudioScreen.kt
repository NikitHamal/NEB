@file:OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)

package com.neb.ians.ui.screens.marketplace

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.outlined.Add
import androidx.compose.material.icons.outlined.ArrowDownward
import androidx.compose.material.icons.outlined.ArrowUpward
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.Payments
import androidx.compose.material.icons.outlined.Publish
import androidx.compose.material.icons.outlined.PauseCircle
import androidx.compose.material.icons.outlined.Storefront
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.api.ApiCreatorCourse
import com.neb.ians.data.api.ApiCreatorPost
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.api.ApiMarketplaceSale
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.NebAuthField
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebChip
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebFieldHint
import com.neb.ians.ui.components.NebLoader
import com.neb.ians.ui.components.NebLoaderSize
import com.neb.ians.ui.components.NebPriceField
import com.neb.ians.ui.components.NebRailTab
import com.neb.ians.ui.components.NebSectionLabel
import com.neb.ians.ui.components.NebTabRail
import com.neb.ians.ui.components.NebToggleRow
import com.neb.ians.ui.components.WebCardShape
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.nebBorderSubtle
import com.neb.ians.util.formatTimeAgo
import kotlinx.coroutines.launch

private val studioTabs = listOf(
    NebRailTab("Page", null),
    NebRailTab("Courses", null),
    NebRailTab("Updates", null),
    NebRailTab("Earnings", null)
)

/**
 * The marketplace studio: the creator's own workbench.
 *
 * Page identity and look, the sections in their order, the offerings they sell
 * and the money those earn — all of it reading and writing the same fields the
 * web studio does, through the same validators.
 */
@Composable
fun CreatorStudioScreen(
    onNavigateBack: () -> Unit,
    onViewPage: (String) -> Unit,
    viewModel: CreatorStudioViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val scope = rememberCoroutineScope()
    var isRefreshing by remember { mutableStateOf(false) }
    var tab by remember { mutableStateOf(0) }

    LaunchedEffect(Unit) { viewModel.load() }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text("Studio", fontWeight = FontWeight.SemiBold)
                        Text(
                            text = uiState.page?.displayName ?: "Your marketplace page",
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    if (uiState.page?.published == true) {
                        IconButton(onClick = { uiState.page?.slug?.let(onViewPage) }) {
                            Icon(Icons.Outlined.Visibility, contentDescription = "View page")
                        }
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { padding ->
        when {
            uiState.isLoading && uiState.page == null ->
                Box(
                    modifier = Modifier.fillMaxSize().padding(padding),
                    contentAlignment = Alignment.Center
                ) { NebLoader() }

            uiState.notEligible ->
                Box(modifier = Modifier.fillMaxSize().padding(padding)) {
                    NebEmptyState(
                        icon = Icons.Outlined.Storefront,
                        title = "Marketplace pages are for teachers, institutes and admins",
                        subtitle = "Set your role in profile settings. Teachers and institutes get a page, a studio and payouts."
                    )
                }

            uiState.error != null && uiState.page == null ->
                Box(modifier = Modifier.fillMaxSize().padding(padding)) {
                    ErrorCard(
                        message = uiState.error ?: "Something went wrong",
                        onRetry = viewModel::load,
                        modifier = Modifier.padding(16.dp)
                    )
                }

            else -> Column(modifier = Modifier.fillMaxSize().padding(padding)) {
                NebTabRail(
                    tabs = studioTabs,
                    selectedIndex = tab,
                    onSelect = { tab = it },
                    modifier = Modifier.fillMaxWidth()
                )

                PullToRefreshBox(
                    isRefreshing = isRefreshing,
                    onRefresh = {
                        scope.launch {
                            isRefreshing = true
                            viewModel.load()
                            isRefreshing = false
                        }
                    },
                    modifier = Modifier.fillMaxSize()
                ) {
                    StudioTabContent(
                        tab = tab,
                        uiState = uiState,
                        viewModel = viewModel,
                        onOpenPage = onViewPage
                    )
                }
            }
        }
    }
}

@Composable
private fun StudioTabContent(
    tab: Int,
    uiState: CreatorStudioUiState,
    viewModel: CreatorStudioViewModel,
    onOpenPage: (String) -> Unit
) {
    val page = uiState.page
    if (page == null) {
        NebEmptyState(
            icon = Icons.Outlined.Storefront,
            title = "Nothing to edit yet",
            subtitle = "Pull down to try again."
        )
        return
    }

    LazyColumn(
        contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 12.dp, bottom = 120.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
        modifier = Modifier.fillMaxSize()
    ) {
        uiState.transientMessage?.let { message ->
            item(key = "message") {
                Surface(
                    shape = WebCardShape,
                    color = if (uiState.messageIsError) {
                        MaterialTheme.colorScheme.errorContainer
                    } else {
                        MaterialTheme.colorScheme.surfaceContainerHigh
                    }
                ) {
                    Text(
                        text = message,
                        style = MaterialTheme.typography.bodySmall,
                        modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp)
                    )
                }
            }
        }

        when (tab) {
            0 -> studioPageTab(uiState, viewModel, onOpenPage)
            1 -> studioCoursesTab(uiState, viewModel)
            2 -> studioUpdatesTab(uiState, viewModel)
            else -> studioEarningsTab(uiState, viewModel)
        }
    }
}

private fun androidx.compose.foundation.lazy.LazyListScope.studioPageTab(
    uiState: CreatorStudioUiState,
    viewModel: CreatorStudioViewModel,
    onOpenPage: (String) -> Unit
) {
    val page = uiState.page ?: return

    item(key = "publish") {
        StudioCard {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                Column(modifier = Modifier.weight(1f)) {
                    Text("Visibility", style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
                    Text(
                        text = if (page.published) "Live at /marketplace/${page.slug}/" else "Draft — only you can see it",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                NebButton(
                    text = if (page.published) "Unpublish" else "Publish",
                    onClick = { viewModel.setPublished(!page.published) },
                    icon = if (page.published) Icons.Outlined.PauseCircle else Icons.Outlined.Publish,
                    tone = if (page.published) NebButtonTone.Tonal else NebButtonTone.Primary,
                    size = NebButtonSize.Small
                )
            }
            if (page.published) {
                NebButton(
                    text = "Open my page",
                    onClick = { onOpenPage(page.slug) },
                    icon = Icons.Outlined.Visibility,
                    tone = NebButtonTone.Text,
                    size = NebButtonSize.Small
                )
            }
        }
    }

    item(key = "identity") {
        StudioCard {
            NebSectionLabel("Identity")
            NebAuthField(
                value = uiState.displayName,
                onValueChange = viewModel::updateDisplayName,
                label = "Page name"
            )
            NebAuthField(
                value = uiState.tagline,
                onValueChange = viewModel::updateTagline,
                label = "One line about you",
                helper = "Shown on your card and at the top of your page."
            )
            NebAuthField(
                value = uiState.about,
                onValueChange = viewModel::updateAbout,
                label = "About",
                singleLine = false,
                minHeight = 108.dp
            )
            NebAuthField(
                value = uiState.slug,
                onValueChange = viewModel::updateSlug,
                label = "Page address",
                helper = "nebians.consica.com.np/marketplace/${uiState.slug.ifBlank { "your-name" }}/"
            )
            NebAuthField(
                value = uiState.subjects,
                onValueChange = viewModel::updateSubjects,
                label = "Subjects",
                helper = "Comma separated. These are what marketplace search matches."
            )
            NebAuthField(
                value = uiState.location,
                onValueChange = viewModel::updateLocation,
                label = "Location"
            )
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
                Box(modifier = Modifier.weight(1f)) {
                    NebAuthField(
                        value = uiState.contactEmail,
                        onValueChange = viewModel::updateContactEmail,
                        label = "Contact email",
                        keyboardType = KeyboardType.Email
                    )
                }
                Box(modifier = Modifier.weight(1f)) {
                    NebAuthField(
                        value = uiState.contactPhone,
                        onValueChange = viewModel::updateContactPhone,
                        label = "Contact phone",
                        keyboardType = KeyboardType.Phone
                    )
                }
            }
            NebAuthField(
                value = uiState.avatarUrl,
                onValueChange = viewModel::updateAvatarUrl,
                label = "Avatar image URL",
                keyboardType = KeyboardType.Uri
            )
            NebAuthField(
                value = uiState.coverUrl,
                onValueChange = viewModel::updateCoverUrl,
                label = "Cover image URL",
                keyboardType = KeyboardType.Uri
            )
            NebToggleRow(
                title = "Accepting new students",
                subtitle = "Shows a small badge on your page",
                checked = uiState.acceptingStudents,
                onCheckedChange = viewModel::updateAccepting
            )
            SaveRow(label = "Save page", saving = uiState.isSavingPage, onSave = viewModel::savePage)
        }
    }

    item(key = "look") {
        StudioCard {
            NebSectionLabel("Look")
            NebFieldHint("Your accent is used on your avatar, your name and your price chips — never on the app's own chrome.")
            Row(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                modifier = Modifier.horizontalScroll(rememberScrollState())
            ) {
                listOf("#004BD4", "#0F766E", "#B45309", "#9D174D", "#4C1D95", "#166534").forEach { hex ->
                    val selected = uiState.accentHex.equals(hex, ignoreCase = true)
                    Surface(
                        shape = CircleShape,
                        color = creatorAccent(hex),
                        modifier = Modifier
                            .size(34.dp)
                            .clip(CircleShape)
                            .clickable { viewModel.updateAccent(hex) },
                        border = if (selected) {
                            androidx.compose.foundation.BorderStroke(
                                3.dp,
                                MaterialTheme.colorScheme.onSurface
                            )
                        } else null
                    ) {}
                }
            }
            NebAuthField(
                value = uiState.accentHex,
                onValueChange = viewModel::updateAccent,
                label = "Accent hex"
            )
            NebSectionLabel("Layout")
            Row(
                horizontalArrangement = Arrangement.spacedBy(6.dp),
                modifier = Modifier.horizontalScroll(rememberScrollState())
            ) {
                listOf("editorial", "spotlight", "grid", "classic").forEach { layout ->
                    NebChip(
                        label = layout.replaceFirstChar { it.uppercase() },
                        selected = uiState.layout == layout,
                        onClick = { viewModel.updateLayout(layout) }
                    )
                }
            }
            Row(
                horizontalArrangement = Arrangement.spacedBy(6.dp),
                modifier = Modifier.horizontalScroll(rememberScrollState())
            ) {
                listOf("art" to "Banner art", "cover" to "Cover", "plain" to "Plain").forEach { (value, label) ->
                    NebChip(
                        label = label,
                        selected = uiState.heroStyle == value,
                        onClick = { viewModel.updateHeroStyle(value) }
                    )
                }
            }
            Row(
                horizontalArrangement = Arrangement.spacedBy(6.dp),
                modifier = Modifier.horizontalScroll(rememberScrollState())
            ) {
                listOf("soft", "round", "sharp").forEach { radius ->
                    NebChip(
                        label = radius.replaceFirstChar { it.uppercase() },
                        selected = uiState.radius == radius,
                        onClick = { viewModel.updateRadius(radius) }
                    )
                }
            }
            SaveRow(label = "Save look", saving = uiState.isSavingPage, onSave = viewModel::savePage)
        }
    }

    item(key = "blocks") {
        StudioCard {
            NebSectionLabel("Sections")
            NebFieldHint("Your page is these sections in this order. Add, reorder or remove them freely — that is the whole layout.")
            uiState.blocks.forEachIndexed { index, block ->
                BlockRow(
                    index = index,
                    block = block,
                    canMoveUp = index > 0,
                    canMoveDown = index < uiState.blocks.lastIndex,
                    onMoveUp = { viewModel.moveBlock(index, -1) },
                    onMoveDown = { viewModel.moveBlock(index, 1) },
                    onRemove = { viewModel.removeBlock(index) },
                    onToggle = { viewModel.toggleBlock(index) },
                    onOpenEditor = { viewModel.openBlockEditor(index) }
                )
            }
            Spacer(Modifier.height(4.dp))
            NebFieldHint("Add a section")
            Row(
                horizontalArrangement = Arrangement.spacedBy(6.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState())
            ) {
                listOf("hero", "about", "courses", "resources", "posts").forEach { type ->
                    NebChip(
                        label = blockLabel(type),
                        selected = false,
                        onClick = { viewModel.addBlock(type) }
                    )
                }
            }
            Row(
                horizontalArrangement = Arrangement.spacedBy(6.dp),
                modifier = Modifier.horizontalScroll(rememberScrollState())
            ) {
                listOf("showcase", "gallery", "testimonials", "faq", "schedule", "links", "contact", "cta").forEach { type ->
                    NebChip(
                        label = blockLabel(type),
                        selected = false,
                        onClick = { viewModel.addBlock(type) }
                    )
                }
            }
            SaveRow(label = "Save sections", saving = uiState.isSavingPage, onSave = viewModel::savePage)
        }
    }

    uiState.editingBlock?.let { (index, block) ->
        item(key = "block_editor_$index") {
            StudioCard {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = "Editing ${blockLabel(block.type)}",
                        style = MaterialTheme.typography.titleSmall,
                        fontWeight = FontWeight.SemiBold,
                        modifier = Modifier.weight(1f)
                    )
                    IconButton(onClick = viewModel::closeBlockEditor) {
                        Icon(Icons.Outlined.Delete, contentDescription = "Close editor")
                    }
                }
                NebAuthField(
                    value = block.title,
                    onValueChange = { viewModel.updateBlockTitle(index, it) },
                    label = "Heading"
                )
                NebAuthField(
                    value = block.subtitle,
                    onValueChange = { viewModel.updateBlockSubtitle(index, it) },
                    label = "Subheading"
                )
                if (block.type == "about" || block.type == "contact") {
                    NebAuthField(
                        value = block.body,
                        onValueChange = { viewModel.updateBlockBody(index, it) },
                        label = "Text",
                        singleLine = false,
                        minHeight = 108.dp
                    )
                }
                if (block.type == "hero" || block.type == "cta") {
                    NebAuthField(
                        value = block.ctaLabel,
                        onValueChange = { viewModel.updateBlockCtaLabel(index, it) },
                        label = "Button label"
                    )
                    NebAuthField(
                        value = block.ctaUrl,
                        onValueChange = { viewModel.updateBlockCtaUrl(index, it) },
                        label = "Button link",
                        keyboardType = KeyboardType.Uri
                    )
                }
                if (block.type in listOf("showcase", "testimonials", "faq", "schedule", "links")) {
                    NebFieldHint(
                        "This section has ${block.items.size} item${if (block.items.size == 1) "" else "s"}. " +
                            "Add or edit items from the studio on the web for long lists; " +
                            "the app keeps the first few in step."
                    )
                    Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        NebButton(
                            text = "Add item",
                            onClick = { viewModel.addBlockItem(index) },
                            icon = Icons.Outlined.Add,
                            tone = NebButtonTone.Tonal,
                            size = NebButtonSize.Small
                        )
                        if (block.items.isNotEmpty()) {
                            NebButton(
                                text = "Remove last",
                                onClick = { viewModel.removeLastBlockItem(index) },
                                tone = NebButtonTone.Text,
                                size = NebButtonSize.Small
                            )
                        }
                    }
                    block.items.forEachIndexed { itemIndex, item ->
                        BlockItemEditor(
                            index = index,
                            itemIndex = itemIndex,
                            blockType = block.type,
                            item = item,
                            viewModel = viewModel
                        )
                    }
                }
                SaveRow(label = "Save section", saving = uiState.isSavingPage, onSave = viewModel::savePage)
            }
        }
    }
}
