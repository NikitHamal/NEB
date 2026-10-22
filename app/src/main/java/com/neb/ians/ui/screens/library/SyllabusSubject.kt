package com.neb.ians.ui.screens.library

import androidx.activity.compose.BackHandler
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.automirrored.outlined.ArrowForward
import androidx.compose.material.icons.automirrored.outlined.MenuBook
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.ExpandMore
import androidx.compose.material.icons.outlined.Replay
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiSyllabusBank
import com.neb.ians.data.api.ApiSyllabusDoc
import com.neb.ians.data.api.ApiSyllabusUnit
import com.neb.ians.data.repository.StudyMark
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebFilterChip
import com.neb.ians.ui.components.NebIconButton
import com.neb.ians.ui.components.NebLoader
import com.neb.ians.ui.components.NebLoaderSize
import com.neb.ians.ui.components.NebRailTab
import com.neb.ians.ui.components.NebTabRail
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.theme.nebFastSpatialSpec
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebSpatialSpec

private typealias OpenDoc = (grade: String, subject: String, kind: String, no: Int) -> Unit

@Composable
internal fun SyllabusSubject(state: SyllabusUiState, viewModel: SyllabusViewModel, onOpenDoc: OpenDoc) {
    BackHandler(onBack = viewModel::closeSubject)
    val doc = state.doc
    Column(Modifier.fillMaxSize()) {
        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(start = 6.dp, end = 8.dp, top = 4.dp)) {
            NebIconButton(icon = Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "Back to subjects", onClick = viewModel::closeSubject)
            Column(Modifier.weight(1f).padding(start = 4.dp)) {
                Text(doc?.name ?: "Syllabus", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                Text(doc?.gradeLabel ?: "Class ${state.openGrade.orEmpty()}", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
        when {
            doc == null && state.isDocLoading -> Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                NebLoader(size = NebLoaderSize.Standard)
            }
            doc == null -> ErrorCard(
                message = state.docError ?: "This syllabus could not be loaded.",
                onRetry = viewModel::retryDoc,
                modifier = Modifier.padding(16.dp)
            )
            else -> SubjectBody(state, doc, viewModel, onOpenDoc)
        }
    }
}

@Composable
private fun SubjectBody(state: SyllabusUiState, doc: ApiSyllabusDoc, viewModel: SyllabusViewModel, onOpenDoc: OpenDoc) {
    val listState = rememberLazyListState()
    val open: (ApiSyllabusUnit) -> Unit = { u ->
        if (u.hasChapter) onOpenDoc(doc.grade, doc.subject, "unit", u.no) else viewModel.toggleUnit(u.no)
    }
    val terms = state.filter.trim().lowercase().split(" ").filter { it.isNotBlank() }
    val units = doc.units.filter { u ->
        val m = state.mark(doc.grade, doc.subject, u.no)
        val done = m?.isDone == true
        (state.area == null || u.area == state.area) &&
            when (state.show) {
                SyllabusShow.All -> true
                SyllabusShow.ToStudy -> !done
                SyllabusShow.Done -> done
            } &&
            terms.all { t -> u.title.lowercase().contains(t) || u.topics.any { it.lowercase().contains(t) } }
    }
    LaunchedEffect(state.focusUnit, doc) {
        val focus = state.focusUnit ?: return@LaunchedEffect
        val target = doc.units.firstOrNull { it.no == focus }
        viewModel.consumeFocus()
        if (target != null && target.hasChapter) onOpenDoc(doc.grade, doc.subject, "unit", focus)
    }
    val tabs = buildList {
        add(SyllabusTab.Chapters to NebRailTab("Chapters"))
        if (doc.banks.isNotEmpty() || doc.guide != null) add(SyllabusTab.Bank to NebRailTab("Question bank", count = doc.banks.size))
        add(SyllabusTab.Exam to NebRailTab("Exam"))
    }
    val tab = tabs.firstOrNull { it.first == state.tab }?.first ?: SyllabusTab.Chapters

    LazyColumn(
        state = listState,
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 8.dp, bottom = 110.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        item(key = "head") { SubjectHeader(doc, state.chaptersDone(doc.grade, doc.subject)) }
        item(key = "next") { NextCards(state, doc, onOpen = open, onBank = { viewModel.setTab(SyllabusTab.Bank) }) }
        item(key = "tabs") {
            NebTabRail(
                tabs = tabs.map { it.second },
                selectedIndex = tabs.indexOfFirst { it.first == tab }.coerceAtLeast(0),
                onSelect = { viewModel.setTab(tabs[it].first) },
                contentPadding = PaddingValues(horizontal = 0.dp, vertical = 6.dp)
            )
        }
        when (tab) {
            SyllabusTab.Chapters -> {
                item(key = "tools") {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        SyllabusSearchField(state.filter, viewModel::setFilter, placeholder = "Find a chapter or topic")
                        Row(Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                            NebFilterChip(label = "All", selected = state.show == SyllabusShow.All, onClick = { viewModel.setShow(SyllabusShow.All) })
                            NebFilterChip(label = "To read", selected = state.show == SyllabusShow.ToStudy, onClick = { viewModel.setShow(SyllabusShow.ToStudy) })
                            NebFilterChip(label = "Done", selected = state.show == SyllabusShow.Done, onClick = { viewModel.setShow(SyllabusShow.Done) })
                            if (doc.areas.size > 1) {
                                Spacer(Modifier.width(6.dp))
                                NebFilterChip(label = "Every part", selected = state.area == null, onClick = { viewModel.setArea(null) })
                                doc.areas.forEach { a -> NebFilterChip(label = a, selected = state.area == a, onClick = { viewModel.setArea(a) }) }
                            }
                        }
                    }
                }
                if (units.isEmpty()) {
                    item(key = "empty") { NebEmptyState(icon = Icons.Outlined.Check, title = "Nothing here", subtitle = "No chapter matches these filters.", art = null) }
                }
                var lastArea: String? = null
                units.forEach { u ->
                    if (doc.areas.size > 1 && u.area != lastArea) {
                        lastArea = u.area
                        item(key = "a_${u.no}") {
                            Text(u.area.uppercase(), style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.padding(top = 8.dp, start = 4.dp))
                        }
                    }
                    item(key = "u_${u.no}") {
                        ChapterRow(
                            unit = u,
                            mark = state.mark(doc.grade, doc.subject, u.no),
                            expanded = u.no in state.expanded,
                            onOpen = { open(u) },
                            onExpand = { viewModel.toggleUnit(u.no) }
                        )
                    }
                }
            }
            SyllabusTab.Bank -> {
                items(doc.banks, key = { "b_${it.no}" }) { b ->
                    BankCard(b, state.marks["${doc.grade}/${doc.subject}/bank${b.no}"]) { onOpenDoc(doc.grade, doc.subject, "bank", b.no) }
                }
                doc.guide?.let { g ->
                    item(key = "guide") {
                        BankCard(ApiSyllabusBank(no = 0, kind = "guide", title = g, label = "Exam guide", blurb = "The paper's pattern, how marks become grades and a time plan"), state.marks["${doc.grade}/${doc.subject}/guide"]) {
                            onOpenDoc(doc.grade, doc.subject, "guide", 0)
                        }
                    }
                }
            }
            SyllabusTab.Exam -> item(key = "exam") { ExamPanel(doc) }
        }
    }
}

@Composable
private fun SubjectHeader(doc: ApiSyllabusDoc, done: Int) {
    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(top = 4.dp)) {
        Box(
            contentAlignment = Alignment.Center,
            modifier = Modifier.size(52.dp).clip(RoundedCornerShape(16.dp)).background(MaterialTheme.colorScheme.onSurface)
        ) {
            Icon(syllabusIcon(doc.icon), contentDescription = null, tint = MaterialTheme.colorScheme.surface, modifier = Modifier.size(26.dp))
        }
        Spacer(Modifier.width(14.dp))
        Column(Modifier.weight(1f)) {
            Text(doc.name, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            Text(
                listOf(doc.nameNe, doc.code.takeIf { it.isNotBlank() }?.let { "Code $it" }).filterNotNull().joinToString(" · "),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }
    }
    Spacer(Modifier.height(12.dp))
    val reading = doc.units.sumOf { it.readMin }
    Text(
        listOfNotNull(
            "${doc.unitCount} chapters",
            doc.hours?.let { "$it teaching hours" },
            reading.takeIf { it > 0 }?.let { "about ${(it + 30) / 60} h of reading" },
            doc.banks.size.takeIf { it > 0 }?.let { "$it question sets" }
        ).joinToString(" · "),
        style = MaterialTheme.typography.labelMedium,
        color = MaterialTheme.colorScheme.onSurfaceVariant
    )
    Spacer(Modifier.height(10.dp))
    Row(verticalAlignment = Alignment.CenterVertically) {
        Text("$done of ${doc.unitCount} done", style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold)
        Spacer(Modifier.width(12.dp))
        SyllabusBar(fraction(done, doc.unitCount), modifier = Modifier.weight(1f))
    }
}

/** What to do next: carry on with the open chapter, else the first not done; and the chapter
 *  whose self-check went worst, when one went badly. */
@Composable
private fun NextCards(state: SyllabusUiState, doc: ApiSyllabusDoc, onOpen: (ApiSyllabusUnit) -> Unit, onBank: () -> Unit) {
    val readable = doc.units.filter { it.hasChapter }
    if (readable.isEmpty()) return
    val marks = readable.associateWith { state.mark(doc.grade, doc.subject, it.no) }
    val inProgress = marks.filter { (_, m) -> m != null && m.isStarted }.maxByOrNull { it.value?.openedAt ?: 0L }?.key
    val first = readable.firstOrNull { marks[it]?.isDone != true }
    val weak = marks.filter { (_, m) -> m != null && m.isWeak }.minByOrNull { (_, m) -> m!!.right.toFloat() / m.tried }?.key
    val main = inProgress ?: first
    val anyStarted = marks.values.any { it != null }
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        if (main != null) {
            val m = marks[main]
            NextCard(
                kicker = when { inProgress != null -> "Continue"; anyStarted -> "Up next"; else -> "Start here" },
                title = "Unit ${main.no}: ${main.title}",
                meta = if (m != null && m.isStarted) "${m.read}% read · about ${maxOf(1, (main.readMin * (100 - m.read)) / 100)} min left" else "${main.readMin} min read",
                strong = true,
                icon = Icons.AutoMirrored.Outlined.ArrowForward,
                onClick = { onOpen(main) }
            )
        } else if (doc.banks.isNotEmpty()) {
            NextCard(kicker = "All chapters done", title = "Test yourself with the question bank", meta = "Model sets in the board's pattern, with keys", strong = true, icon = Icons.AutoMirrored.Outlined.ArrowForward, onClick = onBank)
        }
        if (weak != null && weak != main) {
            val m = marks[weak]!!
            NextCard(kicker = "Worth revising", title = "Unit ${weak.no}: ${weak.title}", meta = "${m.right} of ${m.tried} self-check questions right", strong = false, icon = Icons.Outlined.Replay, onClick = { onOpen(weak) })
        }
    }
}

@Composable
private fun NextCard(kicker: String, title: String, meta: String, strong: Boolean, icon: androidx.compose.ui.graphics.vector.ImageVector, onClick: () -> Unit) {
    Surface(
        shape = WebPanelShape,
        color = if (strong) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.surfaceContainerLow,
        border = if (strong) null else BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        modifier = Modifier.fillMaxWidth().nebPressable(scale = 0.99f, onClick = onClick)
    ) {
        val ink = if (strong) MaterialTheme.colorScheme.surface else MaterialTheme.colorScheme.onSurface
        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(horizontal = 16.dp, vertical = 14.dp)) {
            Column(Modifier.weight(1f)) {
                Text(kicker.uppercase(), style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.SemiBold, color = ink.copy(alpha = 0.7f))
                Text(title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, color = ink, maxLines = 2, overflow = TextOverflow.Ellipsis)
                Text(meta, style = MaterialTheme.typography.bodySmall, color = ink.copy(alpha = 0.7f))
            }
            Spacer(Modifier.width(10.dp))
            Icon(icon, contentDescription = null, tint = ink)
        }
    }
}

@Composable
private fun ChapterRow(unit: ApiSyllabusUnit, mark: StudyMark?, expanded: Boolean, onOpen: () -> Unit, onExpand: () -> Unit) {
    val done = mark?.isDone == true
    val chevron by animateFloatAsState(if (expanded) 180f else 0f, animationSpec = nebFastSpatialSpec(), label = "chevron")
    Surface(
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column {
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().nebPressable(scale = 0.99f, onClick = onOpen).padding(start = 14.dp, top = 12.dp, bottom = 12.dp, end = 4.dp)) {
                Box(
                    contentAlignment = Alignment.Center,
                    modifier = Modifier.size(36.dp).clip(RoundedCornerShape(11.dp))
                        .background(if (done) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.surfaceContainerHigh)
                ) {
                    if (done) Icon(Icons.Outlined.Check, contentDescription = "Done", tint = MaterialTheme.colorScheme.surface, modifier = Modifier.size(18.dp))
                    else Text(unit.no.toString(), style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.Bold)
                }
                Spacer(Modifier.width(12.dp))
                Column(Modifier.weight(1f)) {
                    Text(unit.title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
                    Text(
                        listOfNotNull(
                            unit.hours?.let { "$it hrs" },
                            if (unit.hasChapter) "${unit.readMin} min read" else "notes coming",
                            mark?.takeIf { it.tried > 0 }?.let { "${it.right}/${it.tried} right" },
                            mark?.takeIf { it.isStarted }?.let { "${it.read}%" }
                        ).joinToString(" · "),
                        style = MaterialTheme.typography.bodySmall,
                        color = if (mark?.isWeak == true) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    if (mark != null && mark.isStarted) {
                        Spacer(Modifier.height(6.dp))
                        SyllabusBar(mark.read / 100f, modifier = Modifier.fillMaxWidth(0.6f))
                    }
                }
                Box(Modifier.size(44.dp).clip(RoundedCornerShape(22.dp)).nebPressable(onClick = onExpand), contentAlignment = Alignment.Center) {
                    Icon(Icons.Outlined.ExpandMore, contentDescription = if (expanded) "Hide topics" else "What it covers", tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.rotate(chevron))
                }
            }
            AnimatedVisibility(
                visible = expanded,
                enter = expandVertically(animationSpec = nebSpatialSpec()) + fadeIn(animationSpec = nebEffectsSpec()),
                exit = shrinkVertically(animationSpec = nebSpatialSpec()) + fadeOut(animationSpec = nebEffectsSpec())
            ) {
                Column(Modifier.padding(start = 62.dp, end = 16.dp, bottom = 14.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    if (unit.topics.isNotEmpty()) {
                        Text("The syllabus asks for", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        unit.topics.forEach { Text("–  $it", style = MaterialTheme.typography.bodyMedium) }
                    }
                    if (unit.summary.isNotEmpty()) {
                        Spacer(Modifier.height(4.dp))
                        Text("Key points", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        unit.summary.take(4).forEach { Text(it, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant) }
                    }
                    if (unit.hasChapter) {
                        Spacer(Modifier.height(4.dp))
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.clip(RoundedCornerShape(999.dp)).background(MaterialTheme.colorScheme.onSurface).nebPressable(onClick = onOpen).padding(horizontal = 16.dp, vertical = 9.dp)
                        ) {
                            Icon(Icons.AutoMirrored.Outlined.MenuBook, contentDescription = null, tint = MaterialTheme.colorScheme.surface, modifier = Modifier.size(18.dp))
                            Spacer(Modifier.width(8.dp))
                            Text("Read the chapter", style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.surface)
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun BankCard(bank: ApiSyllabusBank, mark: StudyMark?, onClick: () -> Unit) {
    Surface(
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLow,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        modifier = Modifier.fillMaxWidth().nebPressable(scale = 0.99f, onClick = onClick)
    ) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(3.dp)) {
            Text(bank.label.uppercase(), style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.onSurfaceVariant)
            Text(bank.title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
            Text(
                listOfNotNull(bank.blurb.takeIf { it.isNotBlank() }, bank.readMin.takeIf { it > 0 }?.let { "$it min" }, mark?.takeIf { it.tried > 0 }?.let { "${it.right}/${it.tried} right" }).joinToString(" · "),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            if (mark != null && (mark.isStarted || mark.isDone)) {
                Spacer(Modifier.height(6.dp))
                SyllabusBar(if (mark.isDone) 1f else mark.read / 100f)
            }
        }
    }
}

/** "3hr, FM 75 written (+25 internal) | Group A MCQ 11x1=11 | ..." as a heading and rows. */
private fun examRows(exam: String): Pair<String, List<List<String>>> {
    val parts = exam.split("|").map { it.trim() }.filter { it.isNotEmpty() }
    if (parts.isEmpty()) return "" to emptyList()
    val re = Regex("""^(.*?)\s*(\d+)\s*[x×]\s*(\d+)\s*=\s*(\d+)\s*$""")
    return parts.first() to parts.drop(1).map { p ->
        re.find(p)?.groupValues?.let { listOf(it[1].trim(' ', ':', '-'), "${it[2]} × ${it[3]}", it[4]) } ?: listOf(p, "", "")
    }
}

@Composable
private fun ExamPanel(doc: ApiSyllabusDoc) {
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        if (doc.exam.isNotBlank()) {
            val (head, rows) = examRows(doc.exam)
            Surface(shape = WebPanelShape, color = MaterialTheme.colorScheme.surfaceContainerLow, border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant), modifier = Modifier.fillMaxWidth()) {
                Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("The paper", style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
                    Text(head, style = MaterialTheme.typography.bodyMedium)
                    rows.forEach { r ->
                        Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                            Text(r[0], style = MaterialTheme.typography.bodyMedium, modifier = Modifier.weight(1f))
                            Text(r[1], style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.padding(horizontal = 10.dp))
                            Text(r[2], style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }
        }
        val byArea = doc.units.filter { (it.hours ?: 0) > 0 }.groupBy { it.area.ifBlank { "Units" } }
            .mapValues { (_, us) -> us.sumOf { it.hours ?: 0 } }.toList().sortedByDescending { it.second }
        val total = byArea.sumOf { it.second }
        if (total > 0) {
            Surface(shape = WebPanelShape, color = MaterialTheme.colorScheme.surfaceContainerLow, border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant), modifier = Modifier.fillMaxWidth()) {
                Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text("Where the hours go", style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
                    Text("Teaching hours are the board's guide to how much of the paper each part carries.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    byArea.forEach { (area, hours) ->
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(area, style = MaterialTheme.typography.bodyMedium, modifier = Modifier.weight(1f), maxLines = 1, overflow = TextOverflow.Ellipsis)
                            Box(Modifier.weight(1f).height(8.dp).clip(RoundedCornerShape(4.dp)).background(MaterialTheme.colorScheme.surfaceContainerHighest)) {
                                Box(Modifier.fillMaxWidth(hours.toFloat() / total).fillMaxHeight().clip(RoundedCornerShape(4.dp)).background(MaterialTheme.colorScheme.onSurface))
                            }
                            Text("$hours h", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.width(44.dp).padding(start = 8.dp))
                        }
                    }
                }
            }
        }
    }
}
