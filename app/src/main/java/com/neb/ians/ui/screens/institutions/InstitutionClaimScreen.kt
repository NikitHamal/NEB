package com.neb.ians.ui.screens.institutions

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.AttachFile
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.Close
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import com.neb.ians.ui.components.NebDialogTextField
import com.neb.ians.ui.components.NebTopBar

/** Claim an institution without leaving the app: who you are, a document, then the review stages. */
@Composable
fun InstitutionClaimScreen(slug: String, onBack: () -> Unit, onDone: () -> Unit, vm: InstitutionClaimViewModel = hiltViewModel()) {
    val st by vm.state.collectAsState()
    LaunchedEffect(slug) { vm.load(slug) }
    val c = MaterialTheme.colorScheme
    val d = st.detail
    var reg by rememberSaveable { mutableStateOf("") }
    var person by rememberSaveable { mutableStateOf("") }
    var role by rememberSaveable { mutableStateOf("") }
    var phone by rememberSaveable { mutableStateOf("") }
    var email by rememberSaveable { mutableStateOf("") }
    var address by rememberSaveable(d?.slug) { mutableStateOf(listOf(d?.place.orEmpty(), d?.district.orEmpty()).filter { it.isNotBlank() }.distinct().joinToString(", ")) }
    val pick = rememberLauncherForActivityResult(ActivityResultContracts.OpenMultipleDocuments()) { vm.addDocs(it) }
    Column(Modifier.fillMaxSize().background(c.surface)) {
        NebTopBar(title = "Claim institution", showBrand = false, onBack = onBack)
        if (d == null) {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { Text(if (st.loading) "Loading" else "Could not load this page", color = c.onSurfaceVariant) }
            return@Column
        }
        Column(Modifier.weight(1f).verticalScroll(rememberScrollState()).padding(16.dp).imePadding(), verticalArrangement = Arrangement.spacedBy(14.dp)) {
            Surface(shape = RoundedCornerShape(20.dp), color = c.surfaceContainerLow) {
                Column(Modifier.fillMaxWidth().padding(16.dp)) {
                    Text(d.name, fontSize = 15.sp, fontWeight = FontWeight.SemiBold)
                    Text(listOf(d.kindLabel, d.place, d.district).filter { it.isNotBlank() }.distinct().joinToString(" · "), fontSize = 12.sp, color = c.onSurfaceVariant)
                }
            }
            val app = st.application
            if (app != null) {
                val stage = when (app.status) { "approved" -> 3; "needs_info" -> 2; else -> 1 }
                Surface(shape = RoundedCornerShape(24.dp), color = c.surfaceContainerLowest, border = BorderStroke(1.dp, c.outlineVariant)) {
                    Column(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
                        listOf("Application sent", "Documents checked", "Verified").forEachIndexed { i, label ->
                            val done = i < stage
                            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                                Surface(Modifier.size(28.dp), shape = RoundedCornerShape(10.dp), color = if (done) c.primary else c.surfaceContainerHighest) {
                                    Box(contentAlignment = Alignment.Center) { if (done) Icon(Icons.Outlined.Check, null, Modifier.size(16.dp), tint = c.onPrimary) }
                                }
                                Text(label, fontSize = 14.sp, fontWeight = FontWeight.SemiBold, color = if (done) c.onSurface else c.onSurfaceVariant)
                            }
                        }
                        if (app.note.isNotBlank()) Text(app.note, fontSize = 13.sp, color = c.onSurfaceVariant)
                    }
                }
                Button(onClick = onDone, Modifier.fillMaxWidth().height(52.dp), shape = RoundedCornerShape(28.dp), elevation = null) { Text(if (app.status == "approved") "Open my page" else "Done", fontWeight = FontWeight.SemiBold) }
                return@Column
            }
            NebDialogTextField(reg, { reg = it }, label = "Registration number")
            NebDialogTextField(person, { person = it }, label = "Contact person")
            NebDialogTextField(role, { role = it }, label = "Role", placeholder = "Principal")
            NebDialogTextField(phone, { phone = it }, label = "Phone", keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Phone))
            NebDialogTextField(email, { email = it }, label = "Email", keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email))
            NebDialogTextField(address, { address = it }, label = "Address")
            Text("Documents", fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
            st.docs.forEach { doc ->
                Surface(shape = RoundedCornerShape(18.dp), color = c.surfaceContainerLow) {
                    Row(Modifier.fillMaxWidth().padding(start = 14.dp), verticalAlignment = Alignment.CenterVertically) {
                        Text(doc.name, Modifier.weight(1f), fontSize = 13.sp, maxLines = 1)
                        IconButton(onClick = { vm.removeDoc(doc) }) { Icon(Icons.Outlined.Close, "Remove", Modifier.size(18.dp)) }
                    }
                }
            }
            OutlinedButton(
                onClick = { pick.launch(arrayOf("application/pdf", "image/jpeg", "image/png", "image/webp")) },
                Modifier.fillMaxWidth().heightIn(min = 52.dp), shape = RoundedCornerShape(20.dp), border = BorderStroke(1.5.dp, c.outlineVariant),
            ) { Icon(Icons.Outlined.AttachFile, null, Modifier.size(18.dp)); Spacer(Modifier.width(8.dp)); Text("Attach registration certificate or authority letter", fontSize = 13.sp, maxLines = 2) }
            st.error?.let { Text(it, color = c.error, fontSize = 13.sp) }
            Button(
                onClick = {
                    vm.send(slug, mapOf("name" to d.name, "kind" to d.kind, "district" to d.district, "address" to address, "website" to d.website,
                        "registration_no" to reg, "contact_name" to person, "contact_role" to role, "contact_phone" to phone, "contact_email" to email))
                },
                Modifier.fillMaxWidth().height(52.dp), enabled = !st.sending && st.canClaim, shape = RoundedCornerShape(28.dp), elevation = null,
            ) { Text(if (st.sending) "Sending" else "Send application", fontWeight = FontWeight.SemiBold) }
        }
    }
}
