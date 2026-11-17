package com.neb.ians.ui.screens.institutions

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import com.neb.ians.ui.components.NebTopBar

/** Claim an institution without leaving the app: the form, the documents, then the review stages. [slug] is "new" for one that is not listed. */
@Composable
fun InstitutionClaimScreen(slug: String, onBack: () -> Unit, onDone: () -> Unit, vm: InstitutionClaimViewModel = hiltViewModel()) {
    val st by vm.state.collectAsState()
    LaunchedEffect(slug) { vm.load(slug) }
    val c = MaterialTheme.colorScheme
    val d = st.detail
    val unlisted = slug == InstitutionClaimViewModel.NEW
    Column(Modifier.fillMaxSize().background(c.surface)) {
        NebTopBar(title = if (unlisted) "Add your institution" else "Claim institution", showBrand = false, onBack = onBack)
        if (!unlisted && d == null) {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { Text(if (st.loading) "Loading" else "Could not load this page", color = c.onSurfaceVariant) }
            return@Column
        }
        Column(Modifier.weight(1f).verticalScroll(rememberScrollState()).padding(16.dp).imePadding(), verticalArrangement = Arrangement.spacedBy(20.dp)) {
            if (d != null) Surface(shape = RoundedCornerShape(20.dp), color = c.surfaceContainerLow) {
                Column(Modifier.fillMaxWidth().padding(16.dp)) {
                    Text(d.name, fontSize = 15.sp, fontWeight = FontWeight.SemiBold)
                    Text(listOf(d.kindLabel, d.place, d.district).filter { it.isNotBlank() }.distinct().joinToString(" \u00b7 "), fontSize = 12.sp, color = c.onSurfaceVariant)
                }
            }
            val app = st.application
            when {
                app != null -> ClaimStatus(app, onDone)
                !st.signedIn -> Gate("Sign in to send an application.", "Sign in with the institution account you will manage the page from.")
                !st.canClaim -> Gate("This is a ${st.role.ifBlank { "member" }} account.", "Only institution accounts can claim a page. Sign out and create an institution account to continue.")
                d != null && d.verified && !d.claimable -> Gate("This page is already claimed.", "")
                else -> ClaimForm(d, st, vm, slug)
            }
        }
    }
}

@Composable
private fun Gate(title: String, body: String) {
    val c = MaterialTheme.colorScheme
    Surface(shape = RoundedCornerShape(24.dp), color = c.surfaceContainerLowest, border = BorderStroke(1.dp, c.outlineVariant)) {
        Column(Modifier.fillMaxWidth().padding(18.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            Text(title, fontSize = 15.sp, fontWeight = FontWeight.SemiBold)
            if (body.isNotBlank()) Text(body, fontSize = 13.sp, color = c.onSurfaceVariant)
        }
    }
}

@Composable
private fun ClaimStatus(app: com.neb.ians.data.api.ApiInstApplication, onDone: () -> Unit) {
    val c = MaterialTheme.colorScheme
    val stage = when (app.status) { "approved" -> 3; "needs_info" -> 2; else -> 1 }
    Surface(shape = RoundedCornerShape(24.dp), color = c.surfaceContainerLowest, border = BorderStroke(1.dp, c.outlineVariant)) {
        Column(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
            Text(app.name, fontSize = 15.sp, fontWeight = FontWeight.SemiBold)
            listOf("Application sent", "Documents checked", "Verified").forEachIndexed { i, label ->
                val done = i < stage
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    Surface(Modifier.size(28.dp), shape = RoundedCornerShape(10.dp), color = if (done) c.primary else c.surfaceContainerHighest) {
                        Box(contentAlignment = Alignment.Center) { if (done) Icon(Icons.Outlined.Check, null, Modifier.size(16.dp), tint = c.onPrimary) }
                    }
                    Text(label, fontSize = 14.sp, fontWeight = FontWeight.SemiBold, color = if (done) c.onSurface else c.onSurfaceVariant)
                }
            }
            if (app.status == "needs_info") Text("The reviewer needs more from you", fontSize = 13.sp, fontWeight = FontWeight.Medium, color = c.tertiary)
            if (app.note.isNotBlank()) Text(app.note, fontSize = 13.sp, color = c.onSurfaceVariant)
        }
    }
    Button(onClick = onDone, Modifier.fillMaxWidth().height(52.dp), shape = RoundedCornerShape(28.dp), elevation = null) {
        Text(if (app.status == "approved") "Open my page" else "Done", fontWeight = FontWeight.SemiBold)
    }
}
