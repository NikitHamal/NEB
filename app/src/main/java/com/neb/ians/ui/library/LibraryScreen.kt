package com.neb.ians.ui.library

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material.icons.rounded.Search
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.neb.ians.data.model.Grade
import com.neb.ians.data.model.ResourceType
import com.neb.ians.data.model.Subject
import com.neb.ians.ui.common.EmptyState
import com.neb.ians.ui.common.FilterChipRow
import com.neb.ians.ui.common.NebSearchField
import com.neb.ians.ui.common.SectionHeader

@Composable
fun LibraryScreen(
    onOpenResource: (Long) -> Unit,
    vm: LibraryViewModel = hiltViewModel(),
) {
    val filters by vm.filters.collectAsState()
    val items by vm.results.collectAsState()

    Column(Modifier.fillMaxSize()) {
        Text(
            "Library",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.padding(start = 20.dp, end = 20.dp, top = 16.dp),
        )
        Spacer(Modifier.height(8.dp))
        NebSearchField(
            value = filters.query,
            onChange = vm::setQuery,
            modifier = Modifier.padding(horizontal = 20.dp),
            leading = Icons.Rounded.Search,
            trailing = {
                if (filters.query.isNotEmpty()) {
                    IconButton(onClick = { vm.setQuery("") }) {
                        Icon(Icons.Rounded.Close, contentDescription = "Clear")
                    }
                }
            },
        )
        Spacer(Modifier.height(12.dp))

        SectionHeader("Subject")
        FilterChipRow(
            options = Subject.entries,
            selected = filters.subject,
            label = { it.display },
            onSelect = vm::setSubject,
        )
        Spacer(Modifier.height(6.dp))

        SectionHeader("Grade")
        FilterChipRow(
            options = Grade.entries,
            selected = filters.grade,
            label = { it.display },
            onSelect = vm::setGrade,
        )
        Spacer(Modifier.height(6.dp))

        SectionHeader("Type")
        FilterChipRow(
            options = ResourceType.entries,
            selected = filters.type,
            label = { it.display },
            onSelect = vm::setType,
        )

        Spacer(Modifier.height(8.dp))

        if (items.isEmpty()) {
            EmptyState(
                title = "No matches",
                body = "Try adjusting your filters or the search text.",
            )
        } else {
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(horizontal = 20.dp, vertical = 8.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp),
            ) {
                items(items, key = { it.id }) { r ->
                    ResourceCard(
                        resource = r,
                        onClick = { onOpenResource(r.id) },
                        onToggleFavorite = { vm.toggleFavorite(r) },
                    )
                }
            }
        }
    }
}
