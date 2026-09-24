package com.neb.ians.ui.screens.results

import android.content.Context
import android.content.Intent
import androidx.compose.foundation.BorderStroke
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
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AutoStories
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Download
import androidx.compose.material.icons.filled.Error
import androidx.compose.material.icons.filled.FactCheck
import androidx.compose.material.icons.filled.Print
import androidx.compose.material.icons.filled.ReceiptLong
import androidx.compose.material.icons.filled.School
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Share
import androidx.compose.material.icons.outlined.Badge
import androidx.compose.material.icons.outlined.Cake
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.core.content.FileProvider
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.api.ResultPayload
import com.neb.ians.data.api.ResultSubject
import com.neb.ians.data.results.BulkResultRow
import com.neb.ians.data.results.ResultExam
import com.neb.ians.data.results.ResultExamType
import com.neb.ians.data.results.ResultMode
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.WebTopBar
import kotlinx.coroutines.launch
import java.io.File

private val Batches = listOf("2083", "2082", "2081", "2080")

@Composable
fun ResultCheckerScreen(
    onNavigateBack: () -> Unit,
    viewModel: ResultCheckerViewModel = hiltViewModel()
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    val snackbarHostState = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()
    val context = LocalContext.current

    LaunchedEffect(state.error) {
        state.error?.let { snackbarHostState.showSnackbar(it) }
    }

    Scaffold(
        topBar = {
            WebTopBar(
                showBack = true,
                title = "Result Checker",
                subtitle = "NEB Class 12 and SEE results",
                onBackClick = onNavigateBack
            )
        },
        snackbarHost = { SnackbarHost(snackbarHostState) },
        containerColor = MaterialTheme.colorScheme.surface
    ) { innerPadding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding),
            contentPadding = PaddingValues(start = 16.dp, end = 16.dp, bottom = 120.dp),
            verticalArrangement = Arrangement.spacedBy(18.dp)
        ) {
            item {
                LookupCard(
                    state = state,
                    onExamSelect = viewModel::selectExam,
                    onExamTypeSelect = viewModel::selectExamType,
                    onModeSelect = viewModel::selectMode,
                    onBatchChange = viewModel::updateBatch,
                    onSymbolChange = viewModel::updateSymbol,
                    onDobChange = viewModel::updateDob,
                    onBulkInputChange = viewModel::updateBulkInput,
                    onSubmit = { if (state.mode == ResultMode.Single) viewModel.checkSingle() else viewModel.runBulk() },
                    onCancelBulk = viewModel::cancelBulk
                )
            }
            state.result?.let { lookup ->
                item {
                    ResultCard(
                        payload = lookup.payload,
                        cached = lookup.cached,
                        onShare = { context.shareResultSummary(lookup.payload) },
                        onGradesheet = { viewModel.showGradesheet(true) }
                    )
                }
            }
            if (state.bulkRows.isNotEmpty()) {
                item {
                    BulkResultsCard(
                        rows = state.bulkRows,
                        canExport = !state.isChecking && state.bulkRows.any { it.success },
                        onExport = {
                            val ok = context.exportBulkCsv(state.bulkRows, state.exam, state.batch)
                            scope.launch { snackbarHostState.showSnackbar(if (ok) "CSV export shared" else "Couldn't export CSV") }
                        }
                    )
                }
            }
        }
    }

    if (state.showGradesheet && state.result?.payload != null) {
        GradesheetDialog(
            payload = state.result!!.payload,
            exam = state.exam,
            examType = state.examType,
            batch = state.batch,
            dob = state.dob,
            onDismiss = { viewModel.showGradesheet(false) },
            onShare = { context.shareResultSummary(state.result!!.payload) }
        )
    }
}

@Composable
private fun ResultHero() {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(top = 10.dp, bottom = 2.dp),
        horizontalAlignment = Alignment.Start
    ) {
        Text(
            text = "Access your exam marksheet instantly.",
            style = MaterialTheme.typography.headlineSmall,
            fontWeight = FontWeight.ExtraBold,
            color = MaterialTheme.colorScheme.onSurface
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = "The app calls the same result-checking endpoint as the NEBians website and keeps the native UI responsive while lookups run.",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            lineHeight = MaterialTheme.typography.bodyMedium.lineHeight
        )
    }
}

@Composable
private fun LookupCard(
    state: ResultCheckerUiState,
    onExamSelect: (ResultExam) -> Unit,
    onExamTypeSelect: (ResultExamType) -> Unit,
    onModeSelect: (ResultMode) -> Unit,
    onBatchChange: (String) -> Unit,
    onSymbolChange: (String) -> Unit,
    onDobChange: (String) -> Unit,
    onBulkInputChange: (String) -> Unit,
    onSubmit: () -> Unit,
    onCancelBulk: () -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(18.dp)) {
            SegmentedPills {
                SelectablePill(
                    label = "12",
                    selected = state.exam == ResultExam.Class12,
                    icon = Icons.Filled.School,
                    onClick = { onExamSelect(ResultExam.Class12) },
                    modifier = Modifier.weight(1f)
                )
                SelectablePill(
                    label = "10",
                    selected = state.exam == ResultExam.Class10,
                    icon = Icons.Filled.AutoStories,
                    onClick = { onExamSelect(ResultExam.Class10) },
                    modifier = Modifier.weight(1f)
                )
            }

            if (state.exam == ResultExam.Class12) {
                SegmentedPills(tonal = true) {
                    SelectablePill(
                        label = "Regular",
                        selected = state.examType == ResultExamType.Regular,
                        onClick = { onExamTypeSelect(ResultExamType.Regular) },
                        modifier = Modifier.weight(1f)
                    )
                    SelectablePill(
                        label = "Re-exam",
                        selected = state.examType == ResultExamType.ReExam,
                        onClick = { onExamTypeSelect(ResultExamType.ReExam) },
                        modifier = Modifier.weight(1f)
                    )
                }
            }

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Batches.forEach { batch ->
                    SmallChip(
                        text = if (batch == "2083") "$batch (Current)" else batch,
                        selected = state.batch == batch,
                        onClick = { onBatchChange(batch) }
                    )
                }
            }

            SegmentedPills(plain = true) {
                SelectablePill(
                    label = "Single Check",
                    selected = state.mode == ResultMode.Single,
                    onClick = { onModeSelect(ResultMode.Single) },
                    modifier = Modifier.weight(1f)
                )
                SelectablePill(
                    label = "Bulk Check",
                    selected = state.mode == ResultMode.Bulk,
                    onClick = { onModeSelect(ResultMode.Bulk) },
                    modifier = Modifier.weight(1f)
                )
            }

            if (state.mode == ResultMode.Single) {
                OutlinedTextField(
                    value = state.symbol,
                    onValueChange = onSymbolChange,
                    label = { Text("Symbol Number") },
                    placeholder = { Text("e.g. 12013825") },
                    leadingIcon = { Icon(Icons.Outlined.Badge, contentDescription = null) },
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Ascii),
                    modifier = Modifier.fillMaxWidth()
                )
                if (state.needsDob) {
                    OutlinedTextField(
                        value = state.dob,
                        onValueChange = { newVal ->
                            onDobChange(formatDobInput(newVal, state.dob))
                        },
                        label = { Text("Date of Birth") },
                        placeholder = { Text("YYYY/MM/DD") },
                        leadingIcon = { Icon(Icons.Outlined.Cake, contentDescription = null) },
                        singleLine = true,
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Ascii),
                        supportingText = { Text("Required for Class 12. Use BS date as printed on your admit card.") },
                        modifier = Modifier.fillMaxWidth()
                    )
                }
            } else {
                OutlinedTextField(
                    value = state.bulkInput,
                    onValueChange = onBulkInputChange,
                    label = { Text("Symbol Numbers") },
                    placeholder = {
                        Text(if (state.needsDob) "12013825,2065/03/15\n12013826,2065/08/09" else "0123456A\n0123457B")
                    },
                    minLines = 5,
                    maxLines = 8,
                    supportingText = {
                        Text(if (state.needsDob) "One student per line: symbol,dob" else "One SEE symbol per line.")
                    },
                    modifier = Modifier.fillMaxWidth()
                )
            }

            if (state.isChecking && state.progressTotal > 0) {
                val progress = state.progressCurrent.toFloat() / state.progressTotal.toFloat().coerceAtLeast(1f)
                LinearProgressIndicator(progress = progress, modifier = Modifier.fillMaxWidth())
                Text(
                    text = "Checking ${state.progressCurrent} of ${state.progressTotal} (${(progress * 100).toInt()}%)",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.align(Alignment.End)
                )
            }

            state.error?.let { error ->
                ErrorInline(message = error)
            }

            Button(
                onClick = onSubmit,
                enabled = state.canSubmit,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(50.dp),
                shape = androidx.compose.foundation.shape.RoundedCornerShape(12.dp)
            ) {
                Icon(Icons.Filled.Search, contentDescription = null, modifier = Modifier.size(19.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text(if (state.isChecking) "Checking..." else if (state.mode == ResultMode.Bulk) "Start Bulk Check" else "Check Result")
            }
            if (state.isChecking && state.mode == ResultMode.Bulk) {
                OutlinedButton(onClick = onCancelBulk, modifier = Modifier.fillMaxWidth(), shape = WebPillShape) {
                    Icon(Icons.Filled.Close, contentDescription = null, modifier = Modifier.size(18.dp))
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Cancel Bulk Check")
                }
            }
        }
    }
}

@Composable
private fun ResultCard(
    payload: ResultPayload,
    cached: Boolean,
    onShare: () -> Unit,
    onGradesheet: () -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(18.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = "Your Marksheet",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.ExtraBold,
                    modifier = Modifier.weight(1f)
                )
                SmallStatusBadge(if (cached) "Cached" else "Fresh")
            }
            GpaBadge(gpa = payload.gpa, grade = payload.grade)
            StudentDetails(payload = payload)
            SubjectTable(subjects = payload.subjects)
            HorizontalDivider()
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Icon(Icons.Outlined.Info, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(18.dp))
                Text(
                    text = "Powered by ${payload.source.ifBlank { "Nepal Telecom / NEB" }}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                OutlinedButton(onClick = onShare, modifier = Modifier.weight(1f), shape = WebPillShape) {
                    Icon(Icons.Filled.Share, contentDescription = null, modifier = Modifier.size(18.dp))
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("Share")
                }
                Button(onClick = onGradesheet, modifier = Modifier.weight(1f), shape = WebPillShape) {
                    Icon(Icons.Filled.Print, contentDescription = null, modifier = Modifier.size(18.dp))
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("Print")
                }
            }
        }
    }
}

@Composable
private fun BulkResultsCard(rows: List<BulkResultRow>, canExport: Boolean, onExport: () -> Unit) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Bulk Results", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.ExtraBold, modifier = Modifier.weight(1f))
                OutlinedButton(onClick = onExport, enabled = canExport, shape = WebPillShape) {
                    Icon(Icons.Filled.Download, contentDescription = null, modifier = Modifier.size(17.dp))
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("Export CSV")
                }
            }
            HorizontalDivider()
            rows.forEach { row ->
                Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Column(modifier = Modifier.weight(1.35f)) {
                        Text(row.symbol.ifBlank { "—" }, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold)
                        Text(row.status, style = MaterialTheme.typography.labelSmall, color = if (row.error == null) MaterialTheme.colorScheme.onSurfaceVariant else MaterialTheme.colorScheme.error)
                    }
                    Text(row.name, modifier = Modifier.weight(1.6f), maxLines = 1, overflow = TextOverflow.Ellipsis, style = MaterialTheme.typography.bodySmall)
                    Text(row.gpa, modifier = Modifier.weight(0.7f), style = MaterialTheme.typography.bodySmall, fontWeight = FontWeight.Bold)
                    Text(row.grade, modifier = Modifier.weight(0.7f), style = MaterialTheme.typography.bodySmall)
                }
                HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.65f))
            }
        }
    }
}

@Composable
private fun GpaBadge(gpa: String, grade: String) {
    val score = gpa.toFloatOrNull()
    val accent = when {
        score == null -> MaterialTheme.colorScheme.onSurfaceVariant
        score >= 3.2f -> MaterialTheme.colorScheme.onSurface
        score >= 2.0f -> MaterialTheme.colorScheme.onSurfaceVariant
        else -> MaterialTheme.colorScheme.error
    }
    Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.Center) {
        Surface(
            shape = androidx.compose.foundation.shape.RoundedCornerShape(18.dp),
            color = MaterialTheme.colorScheme.surfaceContainer,
            border = BorderStroke(1.dp, accent.copy(alpha = 0.22f)),
            modifier = Modifier.width(196.dp)
        ) {
            Column(modifier = Modifier.padding(vertical = 22.dp, horizontal = 26.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                Text("GPA", style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Text(gpa.ifBlank { "—" }, style = MaterialTheme.typography.displaySmall, fontWeight = FontWeight.ExtraBold, color = accent)
                Surface(shape = WebPillShape, color = accent.copy(alpha = 0.12f)) {
                    Text(
                        text = if (grade.isBlank()) "—" else "Grade: $grade",
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 4.dp),
                        style = MaterialTheme.typography.labelMedium,
                        fontWeight = FontWeight.SemiBold,
                        color = accent
                    )
                }
            }
        }
    }
}

@Composable
private fun StudentDetails(payload: ResultPayload) {
    Surface(
        shape = androidx.compose.foundation.shape.RoundedCornerShape(16.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLow,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            DetailItem("Student Name", payload.studentName.ifBlank { "—" })
            Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                DetailItem("Exam Board", payload.exam.ifBlank { "—" }, Modifier.weight(1f))
                DetailItem("Exam Year (BS)", payload.batch.ifBlank { "—" }, Modifier.weight(1f))
            }
            Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                DetailItem("Symbol Number", payload.symbol.ifBlank { "—" }, Modifier.weight(1f))
                DetailItem("School / College", payload.school.ifBlank { "—" }, Modifier.weight(1f))
            }
        }
    }
}

@Composable
private fun DetailItem(label: String, value: String, modifier: Modifier = Modifier) {
    Column(modifier = modifier) {
        Text(label.uppercase(), style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurfaceVariant)
        Spacer(modifier = Modifier.height(2.dp))
        Text(value, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold, maxLines = 2, overflow = TextOverflow.Ellipsis)
    }
}

@Composable
private fun SubjectTable(subjects: List<ResultSubject>) {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
            Icon(Icons.Filled.ReceiptLong, contentDescription = null, modifier = Modifier.size(18.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant)
            Text("Subject-wise Grades", style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.ExtraBold, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        Surface(shape = androidx.compose.foundation.shape.RoundedCornerShape(12.dp), border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)) {
            Column {
                ResultRowHeader()
                if (subjects.isEmpty()) {
                    Text("No subject-wise details available.", modifier = Modifier.padding(18.dp), color = MaterialTheme.colorScheme.onSurfaceVariant)
                } else {
                    subjects.forEach { subject -> ResultSubjectRow(subject) }
                }
            }
        }
    }
}

@Composable
private fun ResultRowHeader() {
    Row(modifier = Modifier.fillMaxWidth().background(MaterialTheme.colorScheme.surfaceContainerLow).padding(horizontal = 12.dp, vertical = 9.dp)) {
        TableHead("Subject", Modifier.weight(2f))
        TableHead("Credit", Modifier.weight(0.75f))
        TableHead("Grade", Modifier.weight(0.75f))
        TableHead("GP", Modifier.weight(0.65f))
    }
}

@Composable
private fun ResultSubjectRow(subject: ResultSubject) {
    Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 10.dp), verticalAlignment = Alignment.CenterVertically) {
        Column(modifier = Modifier.weight(2f)) {
            Text(subject.name.ifBlank { "—" }, style = MaterialTheme.typography.bodySmall, fontWeight = FontWeight.SemiBold)
            if (subject.code.isNotBlank()) Text(subject.code, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        Text(subject.creditHour.ifBlank { "—" }, modifier = Modifier.weight(0.75f), style = MaterialTheme.typography.bodySmall)
        GradeBadge(subject.grade.ifBlank { "—" }, modifier = Modifier.weight(0.75f))
        Text(subject.gradePoint.ifBlank { "—" }, modifier = Modifier.weight(0.65f), style = MaterialTheme.typography.bodySmall)
    }
    HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.6f))
}

@Composable
private fun TableHead(text: String, modifier: Modifier = Modifier) {
    Text(text.uppercase(), modifier = modifier, style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.ExtraBold, color = MaterialTheme.colorScheme.onSurfaceVariant)
}

@Composable
private fun GradeBadge(text: String, modifier: Modifier = Modifier) {
    val color = when (text.uppercase()) {
        "A+", "A" -> MaterialTheme.colorScheme.onSurface
        "B+", "B" -> MaterialTheme.colorScheme.onSurfaceVariant
        "C+", "C" -> MaterialTheme.colorScheme.outline
        else -> MaterialTheme.colorScheme.error
    }
    Box(modifier = modifier) {
        Surface(shape = WebPillShape, color = color.copy(alpha = 0.12f)) {
            Text(text, modifier = Modifier.padding(horizontal = 9.dp, vertical = 3.dp), style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.ExtraBold, color = color)
        }
    }
}

@Composable
private fun GradesheetDialog(
    payload: ResultPayload,
    exam: ResultExam,
    examType: ResultExamType,
    batch: String,
    dob: String,
    onDismiss: () -> Unit,
    onShare: () -> Unit
) {
    Dialog(onDismissRequest = onDismiss) {
        Card(
            shape = androidx.compose.foundation.shape.RoundedCornerShape(20.dp),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
            modifier = Modifier.fillMaxWidth().heightIn(max = 740.dp)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("Unofficial Gradesheet Preview", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.ExtraBold, modifier = Modifier.weight(1f))
                    IconButton(onClick = onDismiss) { Icon(Icons.Filled.Close, contentDescription = "Close") }
                }
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = onShare, modifier = Modifier.weight(1f), shape = WebPillShape) {
                        Icon(Icons.Filled.Share, contentDescription = null, modifier = Modifier.size(18.dp))
                        Spacer(Modifier.width(6.dp))
                        Text("Share")
                    }
                    OutlinedButton(onClick = onDismiss, modifier = Modifier.weight(1f), shape = WebPillShape) {
                        Text("Done")
                    }
                }
                Spacer(modifier = Modifier.height(12.dp))
                Surface(
                    modifier = Modifier.fillMaxWidth().weight(1f),
                    color = Color(0xFFFAFAFB),
                    shape = androidx.compose.foundation.shape.RoundedCornerShape(6.dp),
                    border = BorderStroke(2.dp, Color(0xFF9B9BA1))
                ) {
                    LazyColumn(contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                        item {
                            Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.fillMaxWidth()) {
                                Icon(Icons.Filled.FactCheck, contentDescription = null, tint = Color(0xFF101012), modifier = Modifier.size(40.dp))
                                Text(
                                    text = if (exam == ResultExam.Class10) "UNOFFICIAL SEE RESULT" else "UNOFFICIAL CLASS 12 RESULT${if (examType == ResultExamType.ReExam) " (RE-EXAM)" else ""}",
                                    style = MaterialTheme.typography.titleMedium,
                                    fontWeight = FontWeight.ExtraBold,
                                    color = Color(0xFF101012)
                                )
                                Text("nebians.consica.com.np", color = Color(0xFF5C5C61), style = MaterialTheme.typography.labelMedium)
                                Surface(border = BorderStroke(1.dp, Color(0xFF101012)), color = Color.Transparent, modifier = Modifier.padding(top = 8.dp)) {
                                    Text("UNOFFICIAL GRADE SHEET", modifier = Modifier.padding(horizontal = 14.dp, vertical = 4.dp), color = Color(0xFF101012), fontWeight = FontWeight.ExtraBold)
                                }
                            }
                        }
                        item {
                            val examName = if (exam == ResultExam.Class10) "SECONDARY EDUCATION EXAMINATION" else "CLASS 12 EXAMINATION${if (examType == ResultExamType.ReExam) " (RE-EXAM)" else ""}"
                            Text(
                                text = "THE GRADE SECURED BY THE STUDENT IN THE $examName HELD IN THE YEAR ${payload.batch.ifBlank { batch }} BS IS GIVEN BELOW.",
                                style = MaterialTheme.typography.labelSmall,
                                color = Color(0xFF26262A),
                                modifier = Modifier.padding(vertical = 4.dp),
                                textAlign = androidx.compose.ui.text.style.TextAlign.Center
                            )
                        }
                        item { GradesheetDetails(payload, batch, dob) }
                        itemsIndexed(payload.subjects) { index, subject ->
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                                Text((index + 1).toString(), modifier = Modifier.weight(0.4f), color = Color(0xFF0A0A0B), style = MaterialTheme.typography.labelSmall)
                                Text(subject.code.ifBlank { "—" }, modifier = Modifier.weight(0.8f), color = Color(0xFF0A0A0B), style = MaterialTheme.typography.labelSmall)
                                Text(subject.name.ifBlank { "—" }, modifier = Modifier.weight(2f), color = Color(0xFF0A0A0B), style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.SemiBold)
                                Text(subject.creditHour.ifBlank { "—" }, modifier = Modifier.weight(0.7f), color = Color(0xFF0A0A0B), style = MaterialTheme.typography.labelSmall)
                                Text(subject.grade.ifBlank { "—" }, modifier = Modifier.weight(0.7f), color = Color(0xFF0A0A0B), style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.Bold)
                                Text(subject.gradePoint.ifBlank { "—" }, modifier = Modifier.weight(0.6f), color = Color(0xFF0A0A0B), style = MaterialTheme.typography.labelSmall)
                            }
                            HorizontalDivider(color = Color(0xFFE9E9EB))
                        }
                        item {
                            Surface(color = Color(0xFFF1F1F3), border = BorderStroke(1.dp, Color(0xFF26262A))) {
                                Row(modifier = Modifier.fillMaxWidth().padding(12.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                                    Text("GPA: ${payload.gpa.ifBlank { "—" }}", color = Color(0xFF101012), fontWeight = FontWeight.ExtraBold)
                                    Text("GRADE: ${payload.grade.ifBlank { "—" }}", color = Color(0xFF101012), fontWeight = FontWeight.ExtraBold)
                                }
                            }
                            Text("Issue Date: ${batch}/04/15 BS", modifier = Modifier.padding(top = 8.dp), color = Color(0xFF5C5C61), style = MaterialTheme.typography.labelSmall)
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun GradesheetDetails(payload: ResultPayload, batch: String, dob: String) {
    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
        Row(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.weight(1.2f)) {
                Text("NAME OF STUDENT", color = Color(0xFF5C5C61), style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.Bold)
                Text(payload.studentName.uppercase().ifBlank { "—" }, color = Color(0xFF0A0A0B), style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.Bold)
            }
            Column(modifier = Modifier.weight(0.8f)) {
                Text("SYMBOL NO", color = Color(0xFF5C5C61), style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.Bold)
                Text(payload.symbol.ifBlank { "—" }, color = Color(0xFF0A0A0B), style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.Bold)
            }
        }
        Row(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.weight(1.2f)) {
                Text("SCHOOL/COLLEGE", color = Color(0xFF5C5C61), style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.Bold)
                Text(payload.school.uppercase().ifBlank { "—" }, color = Color(0xFF0A0A0B), style = MaterialTheme.typography.labelSmall)
            }
            Column(modifier = Modifier.weight(0.8f)) {
                Text("REGISTRATION NO", color = Color(0xFF5C5C61), style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.Bold)
                Text(payload.registrationNumberOrFallback(), color = Color(0xFF0A0A0B), style = MaterialTheme.typography.labelSmall)
            }
        }
        Row(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.weight(1.2f)) {
                Text("DATE OF BIRTH", color = Color(0xFF5C5C61), style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.Bold)
                Text(dob.ifBlank { payload.dob.ifBlank { "—" } }, color = Color(0xFF0A0A0B), style = MaterialTheme.typography.labelSmall)
            }
            Column(modifier = Modifier.weight(0.8f)) {
                Text("EXAM YEAR / BATCH", color = Color(0xFF5C5C61), style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.Bold)
                Text("${payload.batch.ifBlank { batch }} BS", color = Color(0xFF0A0A0B), style = MaterialTheme.typography.labelSmall)
            }
        }
        HorizontalDivider(color = Color(0xFF9B9BA1), thickness = 1.dp, modifier = Modifier.padding(vertical = 6.dp))
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
            Text("S.N.", modifier = Modifier.weight(0.4f), color = Color(0xFF26262A), fontWeight = FontWeight.ExtraBold, style = MaterialTheme.typography.labelSmall)
            Text("CODE", modifier = Modifier.weight(0.8f), color = Color(0xFF26262A), fontWeight = FontWeight.ExtraBold, style = MaterialTheme.typography.labelSmall)
            Text("SUBJECT TITLE", modifier = Modifier.weight(2f), color = Color(0xFF26262A), fontWeight = FontWeight.ExtraBold, style = MaterialTheme.typography.labelSmall)
            Text("CH", modifier = Modifier.weight(0.7f), color = Color(0xFF26262A), fontWeight = FontWeight.ExtraBold, style = MaterialTheme.typography.labelSmall)
            Text("GRADE", modifier = Modifier.weight(0.7f), color = Color(0xFF26262A), fontWeight = FontWeight.ExtraBold, style = MaterialTheme.typography.labelSmall)
            Text("GP", modifier = Modifier.weight(0.6f), color = Color(0xFF26262A), fontWeight = FontWeight.ExtraBold, style = MaterialTheme.typography.labelSmall)
        }
    }
}

@Composable
private fun CertificateLine(label: String, value: String) {
    Row(modifier = Modifier.fillMaxWidth()) {
        Text(label.uppercase(), modifier = Modifier.weight(0.85f), color = Color(0xFF5C5C61), style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.Bold)
        Text(value, modifier = Modifier.weight(2f), color = Color(0xFF0A0A0B), style = MaterialTheme.typography.labelSmall, fontFamily = FontFamily.SansSerif)
    }
}

@Composable
private fun SegmentedPills(
    tonal: Boolean = false,
    plain: Boolean = false,
    content: @Composable androidx.compose.foundation.layout.RowScope.() -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(WebPillShape)
            .background(if (plain) Color.Transparent else MaterialTheme.colorScheme.surfaceContainerHigh.copy(alpha = if (tonal) 0.72f else 1f))
            .padding(if (plain) 0.dp else 4.dp),
        horizontalArrangement = Arrangement.spacedBy(4.dp),
        content = content
    )
}

@Composable
private fun SelectablePill(
    label: String,
    selected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    icon: ImageVector? = null
) {
    Surface(
        modifier = modifier.clip(WebPillShape).clickable(onClick = onClick),
        shape = WebPillShape,
        color = if (selected) MaterialTheme.colorScheme.primary else Color.Transparent,
        contentColor = if (selected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.Center
        ) {
            if (icon != null) {
                Icon(icon, contentDescription = null, modifier = Modifier.size(18.dp))
                Spacer(modifier = Modifier.width(6.dp))
            }
            Text(label, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold)
        }
    }
}

@Composable
private fun SmallChip(text: String, selected: Boolean, onClick: () -> Unit) {
    Surface(
        shape = WebPillShape,
        color = if (selected) MaterialTheme.colorScheme.primary.copy(alpha = 0.12f) else MaterialTheme.colorScheme.surfaceContainerLow,
        border = BorderStroke(1.dp, if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outlineVariant),
        modifier = Modifier.clip(WebPillShape).clickable(onClick = onClick)
    ) {
        Text(
            text = text,
            modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp),
            style = MaterialTheme.typography.labelMedium,
            fontWeight = FontWeight.SemiBold,
            color = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
private fun SmallStatusBadge(text: String) {
    Surface(shape = WebPillShape, color = MaterialTheme.colorScheme.primary.copy(alpha = 0.10f)) {
        Text(text.uppercase(), modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp), style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.ExtraBold)
    }
}

@Composable
private fun ErrorInline(message: String) {
    Surface(
        shape = androidx.compose.foundation.shape.RoundedCornerShape(12.dp),
        color = MaterialTheme.colorScheme.errorContainer,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.error.copy(alpha = 0.2f))
    ) {
        Row(modifier = Modifier.fillMaxWidth().padding(12.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Icon(Icons.Filled.Error, contentDescription = null, tint = MaterialTheme.colorScheme.onErrorContainer)
            Text(message, color = MaterialTheme.colorScheme.onErrorContainer, style = MaterialTheme.typography.bodySmall)
        }
    }
}

private fun Context.shareResultSummary(payload: ResultPayload) {
    val text = buildString {
        appendLine("NEBians Result")
        appendLine("Name: ${payload.studentName.ifBlank { "—" }}")
        appendLine("Symbol: ${payload.symbol.ifBlank { "—" }}")
        appendLine("GPA: ${payload.gpa.ifBlank { "—" }}")
        appendLine("Grade: ${payload.grade.ifBlank { "—" }}")
        appendLine("Checked via https://nebians.consica.com.np/results/check/")
    }
    val intent = Intent(Intent.ACTION_SEND).apply {
        type = "text/plain"
        putExtra(Intent.EXTRA_TEXT, text)
        putExtra(Intent.EXTRA_SUBJECT, "NEBians Result")
    }
    startActivity(Intent.createChooser(intent, "Share Result"))
}

private fun Context.exportBulkCsv(rows: List<BulkResultRow>, exam: ResultExam, batch: String): Boolean {
    return runCatching {
        val csv = buildString {
            appendLine("Symbol Number,Student Name,GPA,Grade,Status")
            rows.forEach { row ->
                appendCsv(row.symbol); append(',')
                appendCsv(row.name); append(',')
                appendCsv(row.gpa); append(',')
                appendCsv(row.grade); append(',')
                appendCsv(row.error ?: row.status); append('\n')
            }
        }
        val dir = File(cacheDir, "exports").apply { mkdirs() }
        val file = File(dir, "Result_Export_${exam.name}_$batch.csv")
        file.writeText(csv)
        val uri = FileProvider.getUriForFile(this, "$packageName.fileprovider", file)
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "text/csv"
            putExtra(Intent.EXTRA_STREAM, uri)
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        }
        startActivity(Intent.createChooser(intent, "Export CSV"))
        true
    }.getOrDefault(false)
}

private fun StringBuilder.appendCsv(value: String) {
    append('"')
    append(value.replace("\"", "\"\""))
    append('"')
}

private fun formatDobInput(input: String, previous: String): String {
    val clean = input.filter { it.isDigit() || it == '/' }
    if (clean.length < previous.length) {
        return clean
    }
    val digits = clean.filter { it.isDigit() }
    val sb = StringBuilder()
    for (i in digits.indices) {
        sb.append(digits[i])
        if (i == 3) {
            sb.append('/')
        } else if (i == 5) {
            sb.append('/')
        }
    }
    return sb.toString().take(10)
}
