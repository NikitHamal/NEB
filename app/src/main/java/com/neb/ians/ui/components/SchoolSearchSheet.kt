package com.neb.ians.ui.components

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.AccountBalance
import androidx.compose.material.icons.outlined.School
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiInstRow
import com.neb.ians.data.api.ApiService
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

/** Search over the whole catalogue (24k schools, colleges, institutes); claimed pages come first. */
@HiltViewModel
class SchoolSearchViewModel @Inject constructor(private val api: ApiService) : ViewModel() {
    data class State(val rows: List<ApiInstRow> = emptyList(), val total: Int = 0, val loading: Boolean = false, val more: Boolean = false)

    private val _state = MutableStateFlow(State())
    val state: StateFlow<State> = _state.asStateFlow()
    private var job: Job? = null
    private var args = Triple("", "", "")
    private val page = 30

    /** First page of a new query. The old rows stay on screen until the new ones arrive, so the list never blinks empty. */
    fun search(query: String, kind: String = "", verified: String = "", limit: Int = page) {
        job?.cancel()
        args = Triple(query.trim(), kind, verified)
        job = viewModelScope.launch {
            delay(220)
            _state.value = _state.value.copy(loading = true)
            val res = runCatching { api.searchInstitutions(q = args.first, kind = args.second, verified = args.third, limit = limit.coerceAtMost(50)) }.getOrNull()
            _state.value = State(res?.items ?: emptyList(), res?.total ?: 0, false)
        }
    }

    /** Next page by offset (the server caps one page at 50, so a growing limit stopped at 50 rows). */
    fun loadMore() {
        val st = _state.value
        if (st.loading || st.more || st.rows.size >= st.total || job?.isActive == true) return
        _state.value = st.copy(more = true)
        job = viewModelScope.launch {
            val res = runCatching { api.searchInstitutions(q = args.first, kind = args.second, verified = args.third, limit = page, offset = st.rows.size) }.getOrNull()
            val have = _state.value.rows.map { it.slug }.toHashSet()
            val add = res?.items?.filter { it.slug !in have } ?: emptyList()
            _state.value = _state.value.copy(rows = _state.value.rows + add, total = res?.total ?: _state.value.total, more = false)
        }
    }
}

@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
@Composable
fun SchoolSearchSheet(
    title: String = "Find your school",
    kind: String = "",
    onPick: (ApiInstRow) -> Unit,
    onDismiss: () -> Unit,
    vm: SchoolSearchViewModel = hiltViewModel()
) {
    val state by vm.state.collectAsState()
    var query by remember { mutableStateOf("") }
    LaunchedEffect(query) { vm.search(query, kind) }
    NebModalSheet(onDismiss = onDismiss, title = title) {
        NebDialogTextField(
            value = query,
            onValueChange = { query = it },
            placeholder = "Search by name or district",
            modifier = Modifier.fillMaxWidth()
        )
        Text(
            text = if (state.total > 0) "${state.total} found" else if (state.loading) "Searching" else "Nothing yet",
            fontSize = 12.sp,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.padding(top = 8.dp, bottom = 4.dp)
        )
        LazyColumn(
            modifier = Modifier.fillMaxWidth().heightIn(max = 420.dp),
            contentPadding = PaddingValues(bottom = 16.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            items(state.rows, key = { it.slug }) { row -> SchoolRow(row) { onPick(row) } }
        }
    }
}

@Composable
fun SchoolRow(row: ApiInstRow, onClick: () -> Unit) {
    Surface(
        color = MaterialTheme.colorScheme.surfaceContainerLow,
        shape = RoundedCornerShape(20.dp),
        tonalElevation = 0.dp,
        shadowElevation = 0.dp,
        modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(20.dp)).clickable(onClick = onClick)
    ) {
        Row(Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically) {
            Surface(
                color = if (row.verified) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.secondaryContainer,
                shape = RoundedCornerShape(14.dp),
                modifier = Modifier.size(42.dp)
            ) {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.Center, verticalAlignment = Alignment.CenterVertically) {
                    Icon(if (row.kind == "school") Icons.Outlined.School else Icons.Outlined.AccountBalance, null, Modifier.size(22.dp))
                }
            }
            Spacer(Modifier.width(12.dp))
            Column(Modifier.weight(1f)) {
                Text(row.name, fontSize = 14.sp, fontWeight = FontWeight.SemiBold, maxLines = 2)
                Text(
                    listOf(row.kindLabel, row.location).filter { it.isNotBlank() }.joinToString(" · "),
                    fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1
                )
            }
            if (row.verified) {
                Surface(color = MaterialTheme.colorScheme.tertiaryContainer, shape = RoundedCornerShape(10.dp)) {
                    Text(
                        if (row.completeness > 0) "${row.completeness}%" else "On NEBians",
                        fontSize = 11.sp, fontWeight = FontWeight.SemiBold,
                        modifier = Modifier.padding(horizontal = 9.dp, vertical = 3.dp)
                    )
                }
            }
        }
    }
}
