package com.neb.ians.ui.screens.institutions

import com.neb.ians.ui.components.NebTopBar
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.runtime.derivedStateOf
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.ChevronRight
import androidx.compose.material3.FilledTonalButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import com.neb.ians.ui.components.NebDialogTextField
import com.neb.ians.ui.components.NebSelectChip
import com.neb.ians.ui.components.SchoolRow
import com.neb.ians.ui.components.SchoolSearchViewModel

private val KINDS = listOf("" to "All", "school" to "Schools", "college" to "Colleges", "university" to "Universities", "institute" to "Institutes")

/** The whole catalogue. Claimed pages come first and the fuller the portfolio the higher it sits. */
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun SchoolsScreen(
    initialKind: String = "",
    onBack: () -> Unit,
    onOpen: (String) -> Unit,
    vm: SchoolSearchViewModel = hiltViewModel()
) {
    val st by vm.state.collectAsState()
    var query by remember { mutableStateOf("") }
    var kind by remember { mutableStateOf(initialKind) }
    var onlyClaimed by remember { mutableStateOf(false) }
    val listState = rememberLazyListState()
    LaunchedEffect(query, kind, onlyClaimed) { vm.search(query, kind, if (onlyClaimed) "1" else "") }
    // Infinite scroll by offset: ask for the next page when the last rows come into view.
    val nearEnd by remember { derivedStateOf { val last = listState.layoutInfo.visibleItemsInfo.lastOrNull()?.index ?: 0; last >= listState.layoutInfo.totalItemsCount - 6 } }
    LaunchedEffect(nearEnd, st.rows.size) { if (nearEnd) vm.loadMore() }
    Column(Modifier.fillMaxSize()) {
        NebTopBar(showBrand = false, title = "Schools and colleges", onBack = onBack)
        Column(Modifier.padding(horizontal = 16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            NebDialogTextField(value = query, onValueChange = { query = it }, placeholder = "Search by name or district", modifier = Modifier.fillMaxWidth())
            FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                NebSelectChip("On NEBians", onlyClaimed, { onlyClaimed = !onlyClaimed })
                KINDS.forEach { (k, l) -> NebSelectChip(l, kind == k, { kind = k }) }
            }
            if (st.total > 0) Text("%,d results".format(st.total), fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        LazyColumn(
            state = listState,
            contentPadding = PaddingValues(16.dp, 8.dp, 16.dp, 40.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            items(st.rows, key = { it.slug }, contentType = { "row" }) { row -> SchoolRow(row) { onOpen(row.slug) } }
            if (st.more) item(key = "more", contentType = "more") {
                Box(Modifier.fillMaxWidth().padding(12.dp), contentAlignment = Alignment.Center) { CircularProgressIndicator(Modifier.size(24.dp), strokeWidth = 2.5.dp) }
            }
        }
    }
}

/** Hosts provide these so deep screens (Pathways, Edit profile) can open schools without plumbing. */
val LocalOpenSchools = androidx.compose.runtime.staticCompositionLocalOf<() -> Unit> { {} }
val LocalOpenInstitution = androidx.compose.runtime.staticCompositionLocalOf<(String) -> Unit> { {} }
val LocalClaimInstitution = androidx.compose.runtime.staticCompositionLocalOf<((String) -> Unit)?> { null }
val LocalManageInstitution = androidx.compose.runtime.staticCompositionLocalOf<(String) -> Unit> { {} }

/** A row at the top of Find a college: the colleges that filled their page, shown first. */
@Composable
fun PwOnNebRow(modifier: Modifier = Modifier) {
    val open = LocalOpenSchools.current
    androidx.compose.material3.Surface(
        onClick = open,
        color = MaterialTheme.colorScheme.tertiaryContainer,
        shape = androidx.compose.foundation.shape.RoundedCornerShape(20.dp),
        modifier = modifier.fillMaxWidth().padding(bottom = 14.dp)
    ) {
        Row(Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
            Column(Modifier.weight(1f)) {
                Text("Colleges on NEBians", fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
            }
            Icon(androidx.compose.material.icons.Icons.Outlined.ChevronRight, null)
        }
    }
}
