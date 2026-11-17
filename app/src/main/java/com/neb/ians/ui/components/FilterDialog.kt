@file:OptIn(
    androidx.compose.material3.ExperimentalMaterial3Api::class,
    androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class
)

package com.neb.ians.ui.components

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone

private data class SortOption(val key: String, val label: String)

private val SORT_OPTIONS = listOf(
    SortOption("relevant", "Most Relevant"),
    SortOption("trending", "Trending"),
    SortOption("newest", "Newest"),
    SortOption("liked", "Most Liked"),
    SortOption("oldest", "Oldest")
)

@Composable
fun FilterDialog(
    onDismissRequest: () -> Unit,
    selectedSort: String = "relevant",
    onSortSelected: (String) -> Unit = {},
    selectedSubject: String?,
    selectedGradeLevel: String?,
    selectedType: String?,
    subjects: List<String>,
    gradeLevels: List<String>,
    types: List<String>,
    onSubjectSelected: (String?) -> Unit,
    onGradeLevelSelected: (String?) -> Unit,
    onTypeSelected: (String?) -> Unit,
    onClearAll: () -> Unit,
    onApply: () -> Unit,
    resultCount: Int? = null
) {
    val activeCount = listOfNotNull(selectedSubject, selectedGradeLevel, selectedType).size +
        (if (selectedSort != "relevant") 1 else 0)

    NebModalSheet(
        onDismiss = onDismissRequest,
        title = "Filter",
        subtitle = if (activeCount == 0) null else "$activeCount active",
        showClose = true,
        fullBleed = true // bleed: content pads itself or draws edge to edge rows
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .heightIn(max = 460.dp)
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 22.dp),
            verticalArrangement = Arrangement.spacedBy(22.dp)
        ) {
            FilterGroup(
                label = "Sort by",
                options = SORT_OPTIONS.map { it.label },
                selected = SORT_OPTIONS.firstOrNull { it.key == selectedSort }?.label,
                onSelect = { label ->
                    SORT_OPTIONS.firstOrNull { it.label == label }?.let { onSortSelected(it.key) }
                },
                clearable = false
            )
            var subjectQuery by remember { mutableStateOf("") }
            // Selected first, then the rest; a search box once the list is long enough to scan slowly.
            val shownSubjects = remember(subjects, selectedSubject, subjectQuery) {
                subjects.filter { subjectQuery.isBlank() || it.contains(subjectQuery.trim(), ignoreCase = true) }
                    .sortedByDescending { it == selectedSubject }
            }
            if (subjects.size > 8) {
                NebDialogTextField(
                    value = subjectQuery,
                    onValueChange = { subjectQuery = it },
                    placeholder = "Search subjects",
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(modifier = Modifier.height(0.dp))
            }
            FilterGroup(
                label = "Subject",
                options = shownSubjects,
                selected = selectedSubject,
                onSelect = onSubjectSelected
            )
            FilterGroup(
                label = "Grade / Level",
                options = gradeLevels,
                selected = selectedGradeLevel,
                onSelect = onGradeLevelSelected
            )
            FilterGroup(
                label = "Type",
                options = types,
                selected = selectedType,
                onSelect = onTypeSelected
            )
        }

        Spacer(modifier = Modifier.height(20.dp))

        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 22.dp),
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            NebButton(
                text = "Clear all",
                onClick = onClearAll,
                enabled = activeCount > 0,
                tone = NebButtonTone.Outlined,
                size = NebButtonSize.Hero,
                modifier = Modifier.weight(1f)
            )
            NebButton(
                text = when (resultCount) {
                    null -> "Show results"
                    0 -> "No results"
                    1 -> "Show 1 result"
                    else -> "Show $resultCount results"
                },
                onClick = onApply,
                size = NebButtonSize.Hero,
                modifier = Modifier.weight(1.4f)
            )
        }
    }
}

@Composable
private fun FilterGroup(
    label: String,
    options: List<String>,
    selected: String?,
    onSelect: (String?) -> Unit,
    clearable: Boolean = true
) {
    if (options.isEmpty()) return
    Column(modifier = Modifier.fillMaxWidth()) {
        NebSectionLabel(text = label)
        Spacer(modifier = Modifier.height(12.dp))
        NebChipGroup(
            options = options,
            selected = selected,
            onSelect = onSelect,
            toggleable = clearable
        )
    }
}
