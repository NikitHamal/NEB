package com.neb.ians.ui.screens.library

import androidx.activity.compose.BackHandler
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
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
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.Assignment
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.ExpandMore
import androidx.compose.material.icons.outlined.Lightbulb
import androidx.compose.material.icons.outlined.RestartAlt
import androidx.compose.material.icons.outlined.Schedule
import androidx.compose.material.icons.outlined.UnfoldLess
import androidx.compose.material.icons.outlined.UnfoldMore
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
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
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiSyllabusDoc
import com.neb.ians.data.api.ApiSyllabusUnit
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.NebDialog
import com.neb.ians.ui.components.NebDialogAction
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebFilterChip
import com.neb.ians.ui.components.NebIconButton
import com.neb.ians.ui.components.NebLoader
import com.neb.ians.ui.components.NebLoaderSize
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebFastSpatialSpec
import com.neb.ians.ui.theme.nebSpatialSpec
import kotlinx.coroutines.launch

private const val HEADER_ITEMS = 3

@Composable
internal fun SyllabusSubject(state: SyllabusUiState, viewModel: SyllabusViewModel) {
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
            else -> SubjectBody(state, doc, viewModel)
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun SubjectBody(state: SyllabusUiState, doc: ApiSyllabusDoc, viewModel: SyllabusViewModel) {
    val key = "${doc.grade}/${doc.subject}"
    val done = state.done[key].orEmpty()
    val listState = rememberLazyListState()
    val scope = rememberCoroutineScope()
    var confirmReset by remember { mutableStateOf(false) }
    val terms = state.filter.trim().lowercase().split(" ").filter { it.isNotBlank() }
    val units = doc.units.filter { unit ->
        val areaOk = state.area == null || unit.area == state.area
        areaOk && visibleTopics(unit, done, state.show, terms).isNotEmpty()
    }

    LaunchedEffect(state.focusUnit, doc) {
        val focus = state.focusUnit ?: return@LaunchedEffect
        val index = units.indexOfFirst { it.no == focus }
        if (index >= 0) listState.animateScrollToItem(HEADER_ITEMS + index)
        viewModel.consumeFocus()
    }

    if (confirmReset) {
        NebDialog(
            onDismissRequest = { confirmReset = false },
            title = "Clear your ticks?",
            supportingText = "Every topic in ${doc.name} goes back to unticked.",
            confirm = NebDialogAction(label = "Clear", destructive = true, onClick = {
                viewModel.resetSubject(key)
                confirmReset = false
            }),
            dismiss = NebDialogAction(label = "Keep", onClick = { confirmReset = false })
        )
    }

    LazyColumn(
        state = listState,
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 8.dp, bottom = 110.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        item(key = "head") { SubjectHeader(doc, done.size) }
        item(key = "overview") {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                if (doc.exam.isNotBlank()) {
                    InfoPanel(icon = Icons.Outlined.Assignment, title = "Exam pattern") {
                        Text(doc.exam, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
                val totalHours = doc.units.sumOf { it.hours ?: 0 }
                if (totalHours > 0) {
                    InfoPanel(icon = Icons.Outlined.Schedule, title = "Where the hours go") {
                        WeightBar(doc.units, totalHours, done) { no ->
                            if (no !in state.expanded) viewModel.toggleUnit(no)
                            val index = units.indexOfFirst { it.no == no }
                            if (index >= 0) scope.launch { listState.animateScrollToItem(HEADER_ITEMS + index) }
                        }
                        Spacer(Modifier.height(8.dp))
                        doc.units.filter { it.hours != null }.sortedByDescending { it.hours }.take(3).forEach { u ->
                            Row(Modifier.fillMaxWidth().padding(vertical = 2.dp)) {
                                Text("Unit ${u.no} · ${u.title}", style = MaterialTheme.typography.bodySmall, modifier = Modifier.weight(1f), maxLines = 1, overflow = TextOverflow.Ellipsis)
                                Text("${u.hours} hrs", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                        }
                    }
                }
            }
        }
        item(key = "tools") {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                SyllabusSearchField(state.filter, viewModel::setFilter, placeholder = "Filter topics in ${doc.name}")
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                    Row(Modifier.weight(1f).horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        NebFilterChip(label = "All", selected = state.show == SyllabusShow.All, onClick = { viewModel.setShow(SyllabusShow.All) })
                        NebFilterChip(label = "To study", selected = state.show == SyllabusShow.ToStudy, onClick = { viewModel.setShow(SyllabusShow.ToStudy) })
                        NebFilterChip(label = "Done", selected = state.show == SyllabusShow.Done, onClick = { viewModel.setShow(SyllabusShow.Done) })
                    }
                    val allOpen = units.isNotEmpty() && units.all { it.no in state.expanded }
                    NebIconButton(
                        icon = if (allOpen) Icons.Outlined.UnfoldLess else Icons.Outlined.UnfoldMore,
                        contentDescription = if (allOpen) "Collapse every unit" else "Expand every unit",
                        onClick = { viewModel.expandAll(!allOpen) }
                    )
                    NebIconButton(icon = Icons.Outlined.RestartAlt, contentDescription = "Clear my ticks", onClick = { confirmReset = true })
                }
                if (doc.areas.size > 1) {
                    Row(Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        NebFilterChip(label = "Every part", selected = state.area == null, onClick = { viewModel.setArea(null) })
                        doc.areas.forEach { area ->
                            NebFilterChip(label = area, selected = state.area == area, onClick = { viewModel.setArea(area) })
                        }
                    }
                }
            }
        }
        if (units.isEmpty()) {
            item(key = "empty") {
                NebEmptyState(icon = Icons.Outlined.Check, title = "Nothing here", subtitle = "No topic matches these filters.", art = null)
            }
        }
        itemsIndexed(units, key = { _, u -> "u_${u.no}" }) { _, unit ->
            UnitCard(
                unit = unit,
                showArea = doc.areas.size > 1,
                expanded = unit.no in state.expanded || terms.isNotEmpty(),
                done = done,
                topics = visibleTopics(unit, done, state.show, terms),
                onToggle = { viewModel.toggleUnit(unit.no) },
                onTopic = { id -> viewModel.toggleTopic(key, id) },
                onAll = { all -> viewModel.setUnitDone(key, unit.no, unit.topics.size, all) }
            )
        }
    }
}

private fun visibleTopics(unit: ApiSyllabusUnit, done: Set<String>, show: SyllabusShow, terms: List<String>): List<Pair<Int, String>> {
    val titleHit = terms.isNotEmpty() && terms.all { unit.title.lowercase().contains(it) }
    return unit.topics.mapIndexed { i, t -> i to t }.filter { (i, t) ->
        val checked = "${unit.no}.$i" in done
        val showOk = when (show) {
            SyllabusShow.All -> true
            SyllabusShow.ToStudy -> !checked
            SyllabusShow.Done -> checked
        }
        showOk && (terms.isEmpty() || titleHit || terms.all { t.lowercase().contains(it) })
    }
}

@Composable
private fun SubjectHeader(doc: ApiSyllabusDoc, done: Int) {
    Surface(
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLow,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(Modifier.padding(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(
                    contentAlignment = Alignment.Center,
                    modifier = Modifier.size(52.dp).clip(RoundedCornerShape(16.dp)).background(MaterialTheme.colorScheme.onSurface)
                ) {
                    Icon(syllabusIcon(doc.icon), contentDescription = null, tint = MaterialTheme.colorScheme.surface, modifier = Modifier.size(26.dp))
                }
                Spacer(Modifier.width(14.dp))
                Column(Modifier.weight(1f)) {
                    Text(
                        text = listOf(doc.gradeLabel, doc.gradeLabelNe).filter { it.isNotBlank() }.joinToString(" · "),
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Text(doc.name, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                    Text(doc.nameNe, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
            Spacer(Modifier.height(14.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                StatTile("Units", doc.unitCount.toString(), Modifier.weight(1f))
                StatTile("Topics", doc.topicCount.toString(), Modifier.weight(1f))
                doc.hours?.let { StatTile("Hours", it.toString(), Modifier.weight(1f)) }
                StatTile("Done", "${(fraction(done, doc.topicCount) * 100).toInt()}%", Modifier.weight(1f))
            }
            Spacer(Modifier.height(12.dp))
            SyllabusBar(fraction(done, doc.topicCount))
        }
    }
}

@Composable
private fun StatTile(label: String, value: String, modifier: Modifier) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = modifier
            .clip(RoundedCornerShape(14.dp))
            .border(1.dp, MaterialTheme.colorScheme.outlineVariant, RoundedCornerShape(14.dp))
            .padding(vertical = 8.dp)
    ) {
        Text(label, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        Text(value, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
    }
}

@Composable
private fun InfoPanel(icon: androidx.compose.ui.graphics.vector.ImageVector, title: String, content: @Composable () -> Unit) {
    Surface(
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(Modifier.padding(14.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(icon, contentDescription = null, modifier = Modifier.size(18.dp))
                Spacer(Modifier.width(8.dp))
                Text(title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
            }
            Spacer(Modifier.height(8.dp))
            content()
        }
    }
}

@Composable
private fun WeightBar(units: List<ApiSyllabusUnit>, total: Int, done: Set<String>, onUnit: (Int) -> Unit) {
    Row(Modifier.fillMaxWidth().height(30.dp), horizontalArrangement = Arrangement.spacedBy(2.dp)) {
        units.filter { (it.hours ?: 0) > 0 }.forEachIndexed { i, u ->
            val complete = u.topics.isNotEmpty() && u.topics.indices.all { "${u.no}.$it" in done }
            val color = when {
                complete -> MaterialTheme.colorScheme.onSurface
                i % 2 == 0 -> MaterialTheme.colorScheme.surfaceContainerHighest
                else -> MaterialTheme.colorScheme.outlineVariant
            }
            Box(
                contentAlignment = Alignment.Center,
                modifier = Modifier
                    .weight((u.hours ?: 0).toFloat() / total)
                    .fillMaxSize()
                    .clip(RoundedCornerShape(5.dp))
                    .background(color)
                    .nebPressable(onClick = { onUnit(u.no) })
            ) {
                if ((u.hours ?: 0).toFloat() / total > 0.035f) {
                    Text(
                        u.no.toString(),
                        style = MaterialTheme.typography.labelSmall,
                        color = if (complete) MaterialTheme.colorScheme.surface else MaterialTheme.colorScheme.onSurface,
                        maxLines = 1
                    )
                }
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun UnitCard(
    unit: ApiSyllabusUnit,
    showArea: Boolean,
    expanded: Boolean,
    done: Set<String>,
    topics: List<Pair<Int, String>>,
    onToggle: () -> Unit,
    onTopic: (String) -> Unit,
    onAll: (Boolean) -> Unit
) {
    val count = unit.topics.indices.count { "${unit.no}.$it" in done }
    val complete = unit.topics.isNotEmpty() && count == unit.topics.size
    val chevron by animateFloatAsState(if (expanded) 180f else 0f, animationSpec = nebFastSpatialSpec(), label = "chevron")
    val badge by animateColorAsState(
        if (complete) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.surfaceContainerHigh,
        animationSpec = nebEffectsSpec(),
        label = "badge"
    )
    Surface(
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, if (expanded) MaterialTheme.colorScheme.outline else MaterialTheme.colorScheme.outlineVariant),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.fillMaxWidth().nebPressable(scale = 0.99f, onClick = onToggle).padding(14.dp)
            ) {
                Box(
                    contentAlignment = Alignment.Center,
                    modifier = Modifier.size(38.dp).clip(RoundedCornerShape(12.dp)).background(badge)
                ) {
                    Text(
                        unit.no.toString(),
                        style = MaterialTheme.typography.titleSmall,
                        fontWeight = FontWeight.Bold,
                        color = if (complete) MaterialTheme.colorScheme.surface else MaterialTheme.colorScheme.onSurface
                    )
                }
                Spacer(Modifier.width(12.dp))
                Column(Modifier.weight(1f)) {
                    Text(unit.title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
                    Spacer(Modifier.height(4.dp))
                    FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                        if (showArea && unit.area.isNotBlank()) Tag(unit.area)
                        unit.hours?.let { Tag("$it hrs") }
                        Tag("$count/${unit.topics.size}")
                    }
                }
                Icon(
                    Icons.Outlined.ExpandMore,
                    contentDescription = if (expanded) "Collapse" else "Expand",
                    tint = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.rotate(chevron)
                )
            }
            AnimatedVisibility(
                visible = expanded,
                enter = expandVertically(animationSpec = nebSpatialSpec()) + fadeIn(animationSpec = nebEffectsSpec()),
                exit = shrinkVertically(animationSpec = nebSpatialSpec()) + fadeOut(animationSpec = nebEffectsSpec())
            ) {
                Column(Modifier.padding(start = 14.dp, end = 14.dp, bottom = 14.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text("Topics", style = MaterialTheme.typography.labelLarge, modifier = Modifier.weight(1f))
                        Text(
                            text = if (complete) "Clear unit" else "Mark all done",
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.SemiBold,
                            modifier = Modifier.clip(RoundedCornerShape(10.dp)).nebPressable(onClick = { onAll(!complete) }).padding(horizontal = 8.dp, vertical = 6.dp)
                        )
                    }
                    Column {
                        topics.forEach { (i, text) ->
                            val id = "${unit.no}.$i"
                            TopicRow(text = text, checked = id in done, onClick = { onTopic(id) })
                        }
                    }
                    if (unit.summary.isNotEmpty()) {
                        Column(
                            Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(14.dp))
                                .background(MaterialTheme.colorScheme.surfaceContainer)
                                .padding(12.dp),
                            verticalArrangement = Arrangement.spacedBy(6.dp)
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Outlined.Lightbulb, contentDescription = null, modifier = Modifier.size(18.dp))
                                Spacer(Modifier.width(6.dp))
                                Text("Key points", style = MaterialTheme.typography.labelLarge)
                            }
                            unit.summary.forEach { point ->
                                Text(point, style = MaterialTheme.typography.bodyMedium)
                            }
                        }
                    }
                    if (unit.terms.isNotEmpty()) {
                        Text("Key terms", style = MaterialTheme.typography.labelLarge)
                        FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                            unit.terms.forEach { Tag(it) }
                        }
                    }
                    if (unit.sections.isNotEmpty() && unit.sections.size != unit.topics.size) {
                        Text("What the study book covers", style = MaterialTheme.typography.labelLarge)
                        Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
                            unit.sections.forEach { s ->
                                Row {
                                    Text(s.no, style = MaterialTheme.typography.bodySmall, fontWeight = FontWeight.Bold, modifier = Modifier.width(40.dp))
                                    Text(s.title, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun TopicRow(text: String, checked: Boolean, onClick: () -> Unit) {
    val box by animateColorAsState(
        if (checked) MaterialTheme.colorScheme.onSurface else Color.Transparent,
        animationSpec = nebEffectsSpec(),
        label = "check"
    )
    Row(
        verticalAlignment = Alignment.Top,
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .nebPressable(scale = 0.99f, onClick = onClick)
            .padding(horizontal = 6.dp, vertical = 8.dp)
    ) {
        Box(
            contentAlignment = Alignment.Center,
            modifier = Modifier
                .padding(top = 1.dp)
                .size(20.dp)
                .clip(RoundedCornerShape(6.dp))
                .background(box)
                .border(2.dp, if (checked) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.outline, RoundedCornerShape(6.dp))
        ) {
            if (checked) Icon(Icons.Outlined.Check, contentDescription = null, tint = MaterialTheme.colorScheme.surface, modifier = Modifier.size(14.dp))
        }
        Spacer(Modifier.width(12.dp))
        Text(
            text = text,
            style = MaterialTheme.typography.bodyMedium,
            color = if (checked) MaterialTheme.colorScheme.onSurfaceVariant else MaterialTheme.colorScheme.onSurface,
            modifier = Modifier.weight(1f)
        )
    }
}

@Composable
private fun Tag(text: String) {
    Text(
        text = text,
        style = MaterialTheme.typography.labelSmall,
        color = MaterialTheme.colorScheme.onSurfaceVariant,
        modifier = Modifier
            .clip(RoundedCornerShape(8.dp))
            .background(MaterialTheme.colorScheme.surfaceContainerHigh)
            .padding(horizontal = 8.dp, vertical = 3.dp)
    )
}
