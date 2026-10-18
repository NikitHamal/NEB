package com.neb.ians.ui.screens.reader

import kotlinx.coroutines.launch
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.core.content.FileProvider
import android.widget.Toast
import android.content.Intent
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

private enum class ReaderSheet { Options, Pages, Bookmarks, GoTo }

/** A request to show a page; [id] makes repeated jumps to the same page still count. */
private data class Jump(val page: Int, val id: Int, val frac: Float = 0f)

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
    var jumpCount by remember { mutableIntStateOf(0) }
    val goTo: (Int) -> Unit = { page ->
        jump = Jump(page.coerceIn(0, state.pageCount - 1), ++jumpCount)
        sheet = null
    }

    val context = LocalContext.current
    val clipboard = LocalClipboardManager.current
    val scope = rememberCoroutineScope()
    val look = readerLook(state.theme)
    val source = remember(viewModel) { PageSource({ i, w -> viewModel.cachedPage(i, w) }, { i, w -> viewModel.renderPage(i, w) }) }
    val zoom = rememberReaderZoomState()
    val zoomedIn by remember(zoom) { derivedStateOf { zoom.isZoomed } }
    val topInset = WindowInsets.statusBarsIgnoringVisibility.asPaddingValues().calculateTopPadding()
    val bottomInset = WindowInsets.navigationBarsIgnoringVisibility.asPaddingValues().calculateBottomPadding()
    val toggleChrome = { chromeVisible = !chromeVisible }

    ImmersiveWhileHidden(hidden = !chromeVisible)
    KeepScreenOn(state.keepScreenOn)
    BackHandler(enabled = zoomedIn) { zoom.reset() }
    BackHandler(enabled = state.search.open && !zoomedIn) { viewModel.closeSearch() }
    LaunchedEffect(state.search.jump) {
        val hit = state.search.current ?: return@LaunchedEffect
        jump = Jump(hit.page, ++jumpCount, hit.rect.top)
    }

    Box(Modifier.fillMaxSize()) {
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
                            val offset = if (it.frac > 0f) (it.frac * pageHeight - info.viewportSize.height / 3f).toInt().coerceAtLeast(0) else 0
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

        ReaderProgressLine(
            visible = !chromeVisible,
            progress = if (state.pageCount > 1) state.currentPage / (state.pageCount - 1f) else 1f,
            modifier = Modifier.align(Alignment.TopCenter)
        )
        PageBadgeOnChange(chromeVisible, state.currentPage, state.pageCount, Modifier.align(Alignment.BottomCenter))

        ReaderTopBar(
            visible = chromeVisible,
            title = state.title,
            page = state.currentPage,
            pageCount = state.pageCount,
            bookmarked = state.currentPage in state.bookmarks,
            onBack = onBack,
            onToggleBookmark = { viewModel.toggleBookmark() },
            onOptions = { sheet = ReaderSheet.Options },
            modifier = Modifier.align(Alignment.TopCenter),
            onSearch = if (state.canReadText) ({ chromeVisible = true; viewModel.openSearch() }) else null
        )
        ReaderSearchBar(
            search = state.search,
            pageCount = state.pageCount,
            onQuery = viewModel::search,
            onPrev = { viewModel.stepSearch(-1) },
            onNext = { viewModel.stepSearch(1) },
            onClose = viewModel::closeSearch,
            modifier = Modifier.align(Alignment.TopCenter)
        )
        ReaderBottomBar(
            visible = chromeVisible,
            page = state.currentPage,
            pageCount = state.pageCount,
            onGoToPage = { sheet = ReaderSheet.GoTo },
            onSeek = goTo,
            onThumbnails = { sheet = ReaderSheet.Pages },
            onBookmarks = { sheet = ReaderSheet.Bookmarks },
            modifier = Modifier.align(Alignment.BottomCenter)
        )

        ResumeHint(
            page = state.resumePage,
            onStartOver = { goTo(0); viewModel.consumeResume() },
            onDone = viewModel::consumeResume,
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .padding(bottom = bottomInset + ReaderBarHeight + 16.dp)
        )

        val lift by animateDpAsState(
            targetValue = bottomInset + if (chromeVisible) ReaderBarHeight else 0.dp,
            animationSpec = nebSpatialSpec(),
            label = "assistant_lift"
        )
        PdfAssistantOverlay(
            documentTitle = state.title,
            // the spring overshoots; a negative padding throws
            modifier = Modifier.fillMaxSize().padding(bottom = lift.coerceAtLeast(0.dp))
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
            onShare = { sheet = null; shareDocument(context, viewModel.localFile(), state.title) },
            onCopyText = if (state.canReadText) ({
                sheet = null
                scope.launch {
                    val text = viewModel.pageText()
                    if (text == null) Toast.makeText(context, "This page has no selectable text", Toast.LENGTH_SHORT).show()
                    else {
                        clipboard.setText(AnnotatedString(text))
                        Toast.makeText(context, "Page ${state.currentPage + 1} text copied", Toast.LENGTH_SHORT).show()
                    }
                }
            }) else null
        )
        ReaderSheet.Pages -> ThumbnailsSheet(
            aspects = state.pageAspects,
            current = state.currentPage,
            bookmarks = state.bookmarks,
            look = look,
            load = { viewModel.thumbnail(it) },
            onPick = goTo,
            onDismiss = { sheet = null }
        )
        ReaderSheet.Bookmarks -> BookmarksSheet(
            bookmarks = state.bookmarks,
            aspects = state.pageAspects,
            look = look,
            load = { viewModel.thumbnail(it) },
            onPick = goTo,
            onRemove = viewModel::toggleBookmark,
            onDismiss = { sheet = null }
        )
        ReaderSheet.GoTo -> GoToPageDialog(
            pageCount = state.pageCount,
            current = state.currentPage,
            onGo = goTo,
            onDismiss = { sheet = null }
        )
        null -> Unit
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

/** Hands the PDF to another app (share sheet, or open with a different reader). */
private fun shareDocument(context: Context, file: java.io.File?, title: String) {
    if (file == null) { Toast.makeText(context, "The document is not saved on this phone yet", Toast.LENGTH_SHORT).show(); return }
    val uri = runCatching { FileProvider.getUriForFile(context, "${context.packageName}.fileprovider", file) }.getOrNull()
    if (uri == null) { Toast.makeText(context, "This document cannot be shared", Toast.LENGTH_SHORT).show(); return }
    val send = Intent(Intent.ACTION_SEND).apply {
        type = "application/pdf"
        putExtra(Intent.EXTRA_STREAM, uri)
        putExtra(Intent.EXTRA_SUBJECT, title)
        addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
    }
    val view = Intent(Intent.ACTION_VIEW).apply { setDataAndType(uri, "application/pdf"); addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION) }
    val chooser = Intent.createChooser(send, "Share or open $title").apply { putExtra(Intent.EXTRA_INITIAL_INTENTS, arrayOf(view)) }
    runCatching { context.startActivity(chooser) }
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
