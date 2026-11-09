package com.neb.ians.ui.screens.reader

import kotlinx.coroutines.launch
import androidx.compose.ui.platform.LocalContext
import android.app.Activity
import android.content.Context
import android.content.ContextWrapper
import androidx.activity.compose.BackHandler
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.asPaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.navigationBarsIgnoringVisibility
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsIgnoringVisibility
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.ErrorOutline
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.key
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.runtime.snapshotFlow
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.LocalView
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.pixel.PixelSpriteView
import com.neb.ians.ui.pixel.PixelUiSprites
import androidx.compose.foundation.layout.size
import com.neb.ians.ui.components.NebTopBar
import android.content.Intent
import android.net.Uri
import androidx.compose.runtime.mutableStateListOf
import com.neb.ians.ui.components.NebDialog
import com.neb.ians.ui.components.NebDialogAction
import com.neb.ians.ui.screens.reader.pdf.ContentsSheet
import com.neb.ians.ui.screens.reader.pdf.PdfLink
import com.neb.ians.ui.screens.reader.pdf.ReadJump
import com.neb.ians.ui.screens.reader.pdf.ReadSource
import com.neb.ians.ui.screens.reader.pdf.ReaderPill
import com.neb.ians.ui.screens.reader.pdf.ReadingMode
import com.neb.ians.ui.screens.reader.pdf.ReadingSheet
import com.neb.ians.ui.screens.reader.pdf.BookmarksSheet
import com.neb.ians.ui.screens.reader.pdf.FloatingPageBadge
import com.neb.ians.ui.screens.reader.pdf.GoToPageDialog
import com.neb.ians.ui.screens.reader.pdf.PageSource
import com.neb.ians.ui.screens.reader.pdf.PagedReader
import com.neb.ians.ui.screens.reader.pdf.ReaderBarHeight
import com.neb.ians.ui.screens.reader.pdf.ReaderBottomBar
import com.neb.ians.ui.screens.reader.pdf.ReaderOptionsSheet
import com.neb.ians.ui.screens.reader.pdf.ReaderProgressLine
import com.neb.ians.ui.screens.reader.pdf.ReaderTopBar
import com.neb.ians.ui.screens.reader.pdf.ReaderSearchBar
import com.neb.ians.ui.screens.reader.pdf.ReadingLayout
import com.neb.ians.ui.screens.reader.pdf.ScrollReader
import com.neb.ians.ui.screens.reader.pdf.ThumbnailsSheet
import com.neb.ians.ui.screens.reader.pdf.readerLook
import com.neb.ians.ui.screens.reader.pdf.rememberReaderZoomState
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebSpatialSpec
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.distinctUntilChanged

private enum class ReaderSheet { Options, Pages, Bookmarks, GoTo, Contents, Reading }

/** A request to show a page; [id] makes repeated jumps to the same page still count. */
private data class Jump(val page: Int, val id: Int, val frac: Float = 0f, val anchorTop: Boolean = false)

@Composable
fun PdfViewerScreen(
    onNavigateBack: () -> Unit,
    viewModel: PdfViewerViewModel = hiltViewModel()
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    val ready = state.isLocalFileReady && state.pageCount > 0 && state.error == null

    Box(Modifier.fillMaxSize().background(MaterialTheme.colorScheme.surface)) {
        if (ready) {
            PdfReader(state, viewModel, onNavigateBack)
        } else {
            Column(Modifier.fillMaxSize()) {
                NebTopBar(
                    showBrand = false,
                    title = state.title.ifBlank { "Document" },
                    titleFontWeight = FontWeight.Normal,
                    onBack = onNavigateBack
                )
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    when {
                        state.isDownloading -> DownloadState(state.downloadProgress)
                        state.error != null -> ErrorState(state.error ?: "Unable to open document", viewModel::retry)
                        else -> PixelSpriteView(sprite = PixelUiSprites.bookLoader, modifier = Modifier.size(width = 128.dp, height = 88.dp))
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun PdfReader(state: PdfViewerUiState, viewModel: PdfViewerViewModel, onBack: () -> Unit) {
    var chromeVisible by rememberSaveable { mutableStateOf(true) }
    var sheet by remember { mutableStateOf<ReaderSheet?>(null) }
    var jump by remember { mutableStateOf<Jump?>(null) }
    var readJump by remember { mutableStateOf<ReadJump?>(null) }
    var jumpCount by remember { mutableIntStateOf(0) }
    var pendingUri by remember { mutableStateOf<String?>(null) }
    var returnTo by remember { mutableStateOf<Int?>(null) }
    var hiddenNotice by remember { mutableStateOf<String?>(null) }
    val context = LocalContext.current
    val goTo: (Int, Float, Boolean) -> Unit = { page, frac, anchor ->
        val target = page.coerceIn(0, state.pageCount - 1)
        if (state.readingMode) readJump = ReadJump(target, ++jumpCount)
        else jump = Jump(target, ++jumpCount, frac, anchor)
        sheet = null
    }
    val goToPage: (Int) -> Unit = { goTo(it, 0f, false) }
    val openOriginal: (Int) -> Unit = { page ->
        viewModel.onPageVisible(page.coerceIn(0, state.pageCount - 1))
        viewModel.setReadingMode(false)
        sheet = null
    }

    val look = readerLook(state.theme)
    val onLink: (PdfLink) -> Unit = { link ->
        if (link.page >= 0) {
            returnTo = state.currentPage
            goTo(link.page, link.y, true)
        } else {
            pendingUri = link.uri
        }
    }
    val currentOnLink by rememberUpdatedState(onLink)
    val source = remember(viewModel) {
        PageSource(
            { i, w -> viewModel.cachedPage(i, w) },
            { i, w -> viewModel.renderPage(i, w) },
            { i -> viewModel.links(i) },
            { i -> viewModel.cachedLinks(i) },
            { link -> currentOnLink(link) }
        )
    }
    val readSource = remember(viewModel) {
        ReadSource(
            cached = { viewModel.cachedReflow(it) },
            load = { viewModel.reflow(it) },
            cachedCrop = { p, r, w -> viewModel.cachedCrop(p, r, w) },
            loadCrop = { p, r, w -> viewModel.crop(p, r, w) },
            bodyPoints = { viewModel.bodyPoints() }
        )
    }
    val zoom = rememberReaderZoomState()
    val zoomedIn by remember(zoom) { derivedStateOf { zoom.isZoomed } }
    val topInset = WindowInsets.statusBarsIgnoringVisibility.asPaddingValues().calculateTopPadding()
    val bottomInset = WindowInsets.navigationBarsIgnoringVisibility.asPaddingValues().calculateBottomPadding()
    val toggleChrome = { chromeVisible = !chromeVisible }

    ImmersiveWhileHidden(hidden = !chromeVisible || (state.readingMode && state.reading.zen))
    ReadingBrightness(if (state.readingMode) state.reading.brightness else -1f)
    KeepScreenOn(state.keepScreenOn)
    BackHandler(enabled = zoomedIn) { zoom.reset() }
    BackHandler(enabled = state.search.open && !zoomedIn) { viewModel.closeSearch() }
    BackHandler(enabled = state.readSearch.open && state.readingMode) { viewModel.closeReadSearch() }
    LaunchedEffect(state.search.jump) {
        val hit = state.search.current ?: return@LaunchedEffect
        goTo(hit.page, hit.rect.top, false)
    }

    Box(Modifier.fillMaxSize()) {
        if (state.readingMode) {
            ReadingMode(
                title = state.title,
                pageCount = state.pageCount,
                startPage = state.currentPage,
                jump = readJump,
                settings = state.reading,
                theme = state.theme,
                look = look,
                outline = state.outline,
                bookmarked = state.currentPage in state.bookmarks,
                source = readSource,
                chromeVisible = chromeVisible,
                assistantHidden = state.assistantHidden,
                search = state.readSearch,
                onSearchOpen = viewModel::openReadSearch,
                onSearchQuery = viewModel::readSearch,
                onSearchStep = viewModel::stepReadSearch,
                onSearchClose = viewModel::closeReadSearch,
                onChromeToggle = toggleChrome,
                onPage = viewModel::onPageVisible,
                onBack = onBack,
                onToggleBookmark = { viewModel.toggleBookmark() },
                onContents = { sheet = ReaderSheet.Contents },
                onTypography = { sheet = ReaderSheet.Reading },
                onOriginal = openOriginal,
                onJumpPage = goToPage,
                onZen = { viewModel.updateReading { it.copy(zen = !it.zen) }; chromeVisible = state.reading.zen },
                onToggleAssistant = {
                    viewModel.setAssistantHidden(!state.assistantHidden)
                }
            )
        } else {
        // Each layout keeps its own scroll state; switching starts the new one on the current page.
        key(state.layout) {
            when (state.layout) {
                ReadingLayout.Scroll -> {
                    val listState = rememberLazyListState(initialFirstVisibleItemIndex = state.currentPage)
                    LaunchedEffect(listState) {
                        snapshotFlow {
                            val info = listState.layoutInfo
                            val middle = (info.viewportStartOffset + info.viewportEndOffset) / 2
                            info.visibleItemsInfo.firstOrNull { it.offset + it.size >= middle }?.index
                                ?: listState.firstVisibleItemIndex
                        }.distinctUntilChanged().collect(viewModel::onPageVisible)
                    }
                    LaunchedEffect(jump) {
                        jump?.let {
                            zoom.reset()
                            // land a search hit a third of the way down the screen, not at the page top
                            val info = listState.layoutInfo
                            val pageHeight = info.viewportSize.width * state.pageAspects.getOrElse(it.page) { 1.414f }
                            val offset = when {
                                it.anchorTop -> (it.frac * pageHeight - 24f).toInt().coerceAtLeast(0)
                                it.frac > 0f -> (it.frac * pageHeight - info.viewportSize.height / 3f).toInt().coerceAtLeast(0)
                                else -> 0
                            }
                            listState.scrollToItem(it.page, offset)
                            jump = null
                        }
                    }
                    ScrollReader(
                        aspects = state.pageAspects,
                        listState = listState,
                        zoom = zoom,
                        look = look,
                        source = source,
                        contentPadding = PaddingValues(
                            top = topInset + ReaderBarHeight + 10.dp,
                            bottom = bottomInset + ReaderBarHeight + 10.dp
                        ),
                        onTap = toggleChrome,
                        search = state.search
                    )
                }
                ReadingLayout.Pages -> {
                    val pagerState = rememberPagerState(initialPage = state.currentPage) { state.pageCount }
                    LaunchedEffect(pagerState) {
                        snapshotFlow { pagerState.currentPage }.collect(viewModel::onPageVisible)
                    }
                    LaunchedEffect(jump) {
                        jump?.let { pagerState.scrollToPage(it.page); jump = null }
                    }
                    PagedReader(
                        aspects = state.pageAspects,
                        pagerState = pagerState,
                        zoom = zoom,
                        look = look,
                        source = source,
                        verticalInset = maxOf(topInset, bottomInset) + ReaderBarHeight + 8.dp,
                        onTap = toggleChrome,
                        search = state.search
                    )
                }
            }
        }

        }

        if (!state.readingMode) ReaderProgressLine(
            visible = !chromeVisible,
            progress = if (state.pageCount > 1) state.currentPage / (state.pageCount - 1f) else 1f,
            modifier = Modifier.align(Alignment.TopCenter)
        )
        if (!state.readingMode) PageBadgeOnChange(chromeVisible, state.currentPage, state.pageCount, Modifier.align(Alignment.BottomCenter))

        if (!state.readingMode) ReaderTopBar(
            visible = chromeVisible,
            title = state.title,
            page = state.currentPage,
            pageCount = state.pageCount,
            bookmarked = state.currentPage in state.bookmarks,
            onBack = onBack,
            onToggleBookmark = { viewModel.toggleBookmark() },
            onOptions = { sheet = ReaderSheet.Options },
            modifier = Modifier.align(Alignment.TopCenter),
            // devices without the platform text API search in reading mode, which reads the text itself
            onSearch = {
                chromeVisible = true
                if (state.canReadText) viewModel.openSearch()
                else { viewModel.setReadingMode(true); viewModel.openReadSearch() }
            },
            onReadingMode = { viewModel.setReadingMode(true) },
            onContents = { sheet = ReaderSheet.Contents },
            assistantHidden = state.assistantHidden,
            onToggleAssistant = { viewModel.setAssistantHidden(!state.assistantHidden); if (!state.assistantHidden) hiddenNotice = "Neby AI is hidden. Bring it back from the menu." }
        )
        if (!state.readingMode) ReaderSearchBar(
            search = state.search,
            pageCount = state.pageCount,
            onQuery = viewModel::search,
            onPrev = { viewModel.stepSearch(-1) },
            onNext = { viewModel.stepSearch(1) },
            onClose = viewModel::closeSearch,
            modifier = Modifier.align(Alignment.TopCenter)
        )
        if (!state.readingMode) ReaderBottomBar(
            visible = chromeVisible,
            page = state.currentPage,
            pageCount = state.pageCount,
            onGoToPage = { sheet = ReaderSheet.GoTo },
            onSeek = goToPage,
            onThumbnails = { sheet = ReaderSheet.Pages },
            onBookmarks = { sheet = ReaderSheet.Bookmarks },
            modifier = Modifier.align(Alignment.BottomCenter)
        )

        ResumeHint(
            page = state.resumePage,
            onStartOver = { goToPage(0); viewModel.consumeResume() },
            onDone = viewModel::consumeResume,
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .padding(bottom = bottomInset + ReaderBarHeight + 16.dp)
        )

        ReaderPill(
            message = returnTo?.let { "Went to another page" },
            action = returnTo?.let { "Back to page ${it + 1}" },
            onAction = { returnTo?.let { page -> goToPage(page) }; returnTo = null },
            onDone = { returnTo = null },
            modifier = Modifier.align(Alignment.BottomCenter).padding(bottom = bottomInset + ReaderBarHeight + 16.dp),
            holdMs = 6500
        )
        ReaderPill(
            message = hiddenNotice,
            action = "Undo",
            onAction = { viewModel.setAssistantHidden(false); hiddenNotice = null },
            onDone = { hiddenNotice = null },
            modifier = Modifier.align(Alignment.BottomCenter).padding(bottom = bottomInset + ReaderBarHeight + 16.dp)
        )

        val lift by animateDpAsState(
            targetValue = bottomInset + if (chromeVisible) ReaderBarHeight else 0.dp,
            animationSpec = nebSpatialSpec(),
            label = "assistant_lift"
        )
        PdfAssistantOverlay(
            documentTitle = state.title,
            // the spring overshoots; a negative padding throws
            modifier = Modifier.fillMaxSize().padding(bottom = lift.coerceAtLeast(0.dp)),
            fabHidden = state.assistantHidden,
            fabX = state.assistantX,
            fabY = state.assistantY,
            onFabMoved = viewModel::moveAssistant,
            onFabDismissed = {
                viewModel.setAssistantHidden(true)
                hiddenNotice = "Neby AI is hidden. Bring it back from the menu."
            }
        )
    }

    when (sheet) {
        ReaderSheet.Options -> ReaderOptionsSheet(
            theme = state.theme,
            layout = state.layout,
            keepScreenOn = state.keepScreenOn,
            onTheme = viewModel::setTheme,
            onLayout = viewModel::setLayout,
            onKeepScreenOn = viewModel::setKeepScreenOn,
            onDismiss = { sheet = null },
            assistantHidden = state.assistantHidden,
            onAssistantHidden = viewModel::setAssistantHidden
        )
        ReaderSheet.Contents -> ContentsSheet(
            items = state.outline,
            currentPage = state.currentPage,
            onPick = { item -> goTo(item.page, item.y, true) },
            onDismiss = { sheet = null }
        )
        ReaderSheet.Reading -> ReadingSheet(
            settings = state.reading,
            theme = state.theme,
            assistantHidden = state.assistantHidden,
            onSettings = viewModel::updateReading,
            onTheme = viewModel::setTheme,
            onAssistantHidden = viewModel::setAssistantHidden,
            onDismiss = { sheet = null }
        )
        ReaderSheet.Pages -> ThumbnailsSheet(
            aspects = state.pageAspects,
            current = state.currentPage,
            bookmarks = state.bookmarks,
            look = look,
            load = { viewModel.thumbnail(it) },
            onPick = goToPage,
            onDismiss = { sheet = null }
        )
        ReaderSheet.Bookmarks -> BookmarksSheet(
            bookmarks = state.bookmarks,
            aspects = state.pageAspects,
            look = look,
            load = { viewModel.thumbnail(it) },
            onPick = goToPage,
            onRemove = viewModel::toggleBookmark,
            onDismiss = { sheet = null }
        )
        ReaderSheet.GoTo -> GoToPageDialog(
            pageCount = state.pageCount,
            current = state.currentPage,
            onGo = goToPage,
            onDismiss = { sheet = null }
        )
        null -> Unit
    }

    pendingUri?.let { uri ->
        NebDialog(
            onDismissRequest = { pendingUri = null },
            title = "Open this link?",
            supportingText = uri,
            confirm = NebDialogAction("Open", onClick = {
                runCatching { context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(uri)).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)) }
                pendingUri = null
            }),
            dismiss = NebDialogAction("Cancel", onClick = { pendingUri = null })
        )
    }
}

/** Reading mode can set the screen's brightness; the system's own comes back when it is left. */
@Composable
private fun ReadingBrightness(value: Float) {
    val view = LocalView.current
    DisposableEffect(view, value) {
        val window = view.context.findActivity()?.window
        if (window != null && value >= 0f) {
            val attrs = window.attributes
            attrs.screenBrightness = value.coerceIn(0.02f, 1f)
            window.attributes = attrs
        }
        onDispose {
            if (window != null) {
                val attrs = window.attributes
                attrs.screenBrightness = android.view.WindowManager.LayoutParams.BRIGHTNESS_OVERRIDE_NONE
                window.attributes = attrs
            }
        }
    }
}

/** Shows the page number for a moment when the page changes while the bars are hidden. */
@Composable
private fun PageBadgeOnChange(chromeVisible: Boolean, page: Int, pageCount: Int, modifier: Modifier) {
    var shown by remember { mutableStateOf(false) }
    var lastPage by remember { mutableIntStateOf(page) }
    LaunchedEffect(page, chromeVisible) {
        if (chromeVisible) {
            shown = false
        } else if (page != lastPage) {
            shown = true
            delay(1200)
            shown = false
        }
        lastPage = page
    }
    FloatingPageBadge(visible = shown && !chromeVisible, page = page, pageCount = pageCount, modifier = modifier)
}

/** "Continuing from page 14", with a way back to the start. Leaves by itself after a few seconds. */
@Composable
private fun ResumeHint(page: Int?, onStartOver: () -> Unit, onDone: () -> Unit, modifier: Modifier) {
    var visible by remember { mutableStateOf(false) }
    LaunchedEffect(page) {
        if (page != null) {
            visible = true
            delay(4500)
            visible = false
            delay(400)
            onDone()
        }
    }
    AnimatedVisibility(
        visible = visible && page != null,
        modifier = modifier,
        enter = slideInVertically(nebSpatialSpec()) { it / 2 } + fadeIn(nebEffectsSpec()),
        exit = slideOutVertically(nebSpatialSpec()) { it / 2 } + fadeOut(nebEffectsSpec())
    ) {
        Row(
            Modifier
                .widthIn(max = 420.dp)
                .padding(horizontal = 16.dp)
                .clip(RoundedCornerShape(18.dp))
                .background(MaterialTheme.colorScheme.inverseSurface)
                .padding(start = 18.dp, end = 6.dp, top = 6.dp, bottom = 6.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                "Continuing from page ${(page ?: 0) + 1}",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.inverseOnSurface,
                modifier = Modifier.weight(1f, fill = false).padding(end = 8.dp)
            )
            NebButton(
                text = "Start over",
                onClick = { visible = false; onStartOver() },
                tone = NebButtonTone.Text,
                size = NebButtonSize.Compact
            )
        }
    }
}

/** Hides the system bars while reading in focus mode, and always restores them on exit. */
@Composable
private fun ImmersiveWhileHidden(hidden: Boolean) {
    val view = LocalView.current
    val controller = remember(view) {
        view.context.findActivity()?.window?.let { WindowCompat.getInsetsController(it, view) }
    }
    LaunchedEffect(hidden, controller) {
        controller ?: return@LaunchedEffect
        if (hidden) {
            controller.systemBarsBehavior = WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
            controller.hide(WindowInsetsCompat.Type.systemBars())
        } else {
            controller.show(WindowInsetsCompat.Type.systemBars())
        }
    }
    DisposableEffect(controller) {
        onDispose { controller?.show(WindowInsetsCompat.Type.systemBars()) }
    }
}

@Composable
private fun KeepScreenOn(enabled: Boolean) {
    val view = LocalView.current
    DisposableEffect(view, enabled) {
        view.keepScreenOn = enabled
        onDispose { view.keepScreenOn = false }
    }
}

private tailrec fun Context.findActivity(): Activity? = when (this) {
    is Activity -> this
    is ContextWrapper -> baseContext.findActivity()
    else -> null
}

@Composable
private fun DownloadState(progress: Int) {
    Column(
        Modifier.padding(32.dp).widthIn(max = 360.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        PixelSpriteView(sprite = PixelUiSprites.bookLoader, modifier = Modifier.size(width = 128.dp, height = 88.dp))
        Text("Saving for offline reading", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
        LinearProgressIndicator(
            progress = { progress.coerceIn(0, 100) / 100f },
            color = MaterialTheme.colorScheme.onSurface,
            trackColor = MaterialTheme.colorScheme.surfaceContainerHighest,
            modifier = Modifier.fillMaxWidth()
        )
        Text(
            "$progress%. It opens instantly next time, even without internet.",
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            textAlign = TextAlign.Center
        )
    }
}

@Composable
private fun ErrorState(message: String, onRetry: () -> Unit) {
    Column(
        Modifier.padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        Icon(Icons.Outlined.ErrorOutline, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant)
        Text(message, style = MaterialTheme.typography.bodyLarge, textAlign = TextAlign.Center, color = MaterialTheme.colorScheme.onSurfaceVariant)
        NebButton(text = "Try again", onClick = onRetry)
    }
}
