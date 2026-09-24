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
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

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
    onApply: () -> Unit
) {
    val activeCount = listOfNotNull(selectedSubject, selectedGradeLevel, selectedType).size +
        (if (selectedSort != "relevant") 1 else 0)

    NebModalSheet(
        onDismiss = onDismissRequest,
        title = "Filter",
        subtitle = if (activeCount == 0) {
            "Narrow the library down to what you need"
        } else {
            "$activeCount filter${if (activeCount == 1) "" else "s"} active"
        },
        showClose = true
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
            FilterGroup(
                label = "Subject",
                options = subjects,
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
            OutlinedButton(
                onClick = onClearAll,
                enabled = activeCount > 0,
                shape = RoundedCornerShape(50),
                modifier = Modifier
                    .weight(1f)
                    .heightIn(min = 52.dp)
            ) {
                Text(text = "Clear all", style = MaterialTheme.typography.labelLargeEmphasized)
            }
            Button(
                onClick = onApply,
                shape = RoundedCornerShape(50),
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    contentColor = MaterialTheme.colorScheme.onPrimary
                ),
                modifier = Modifier
                    .weight(1.4f)
                    .heightIn(min = 52.dp)
            ) {
                Text(text = "Show results", style = MaterialTheme.typography.labelLargeEmphasized)
            }
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
