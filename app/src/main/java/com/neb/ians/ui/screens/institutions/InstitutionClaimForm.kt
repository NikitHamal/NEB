package com.neb.ians.ui.screens.institutions

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.AttachFile
import androidx.compose.material.icons.outlined.Close
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.data.api.ApiInstDetail
import com.neb.ians.ui.components.NebDialogTextField
import com.neb.ians.ui.components.NebSelectChip
import com.neb.ians.ui.components.nebHorizontalScroll

private val KINDS = listOf("school" to "School", "college" to "College", "university" to "University", "institute" to "Institute")
private val DOC_TYPES = listOf(
    "registration" to "Registration", "pan" to "PAN or VAT", "affiliation" to "Affiliation",
    "authority" to "Authority letter", "id" to "Applicant ID", "other" to "Other"
)

@Composable
private fun Section(title: String, content: @Composable ColumnScope.() -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Text(title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
        content()
    }
}

/** The whole application in one scroll: institution, contact, documents with a type each, then send. */
@Composable
fun ClaimForm(
    detail: ApiInstDetail?,
    st: InstitutionClaimViewModel.State,
    vm: InstitutionClaimViewModel,
    slug: String
) {
    val c = MaterialTheme.colorScheme
    val key = detail?.slug ?: "new"
    var name by rememberSaveable(key) { mutableStateOf(detail?.name.orEmpty()) }
    var kind by rememberSaveable(key) { mutableStateOf(detail?.kind ?: "school") }
    var district by rememberSaveable(key) { mutableStateOf(detail?.district.orEmpty()) }
    var address by rememberSaveable(key) { mutableStateOf(listOf(detail?.place.orEmpty(), detail?.district.orEmpty()).filter { it.isNotBlank() }.distinct().joinToString(", ")) }
    var website by rememberSaveable(key) { mutableStateOf(detail?.website.orEmpty()) }
    var reg by rememberSaveable { mutableStateOf("") }
    var person by rememberSaveable { mutableStateOf("") }
    var role by rememberSaveable { mutableStateOf("") }
    var phone by rememberSaveable { mutableStateOf("") }
    var email by rememberSaveable(st.email) { mutableStateOf(st.email) }
    var message by rememberSaveable { mutableStateOf("") }
    var tried by rememberSaveable { mutableStateOf(false) }
    val pick = rememberLauncherForActivityResult(ActivityResultContracts.OpenMultipleDocuments()) { vm.addDocs(it) }

    val bad = mapOf(
        "name" to (name.trim().length < 3), "address" to (address.trim().length < 3), "reg" to (reg.trim().length < 2),
        "person" to (person.trim().length < 3), "role" to (role.trim().length < 2),
        "phone" to (phone.count { it.isDigit() } < 7), "email" to !android.util.Patterns.EMAIL_ADDRESS.matcher(email.trim()).matches()
    )
    fun err(k: String) = tried && bad[k] == true

    Section("Institution") {
        if (detail == null) NebDialogTextField(name, { name = it }, label = "Institution name", isError = err("name"), modifier = Modifier.fillMaxWidth())
        Row(Modifier.fillMaxWidth().nebHorizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            KINDS.forEach { (k, l) -> NebSelectChip(l, kind == k, { kind = k }) }
        }
        if (detail == null) NebDialogTextField(district, { district = it }, label = "District", modifier = Modifier.fillMaxWidth())
        NebDialogTextField(address, { address = it }, label = "Address", isError = err("address"), modifier = Modifier.fillMaxWidth())
        NebDialogTextField(website, { website = it }, label = "Website", placeholder = "school.edu.np", keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Uri), modifier = Modifier.fillMaxWidth())
        NebDialogTextField(reg, { reg = it }, label = "Registration number", isError = err("reg"), modifier = Modifier.fillMaxWidth())
    }
    Section("Contact person") {
        NebDialogTextField(person, { person = it }, label = "Full name", isError = err("person"), modifier = Modifier.fillMaxWidth())
        NebDialogTextField(role, { role = it }, label = "Role", placeholder = "Principal", isError = err("role"), modifier = Modifier.fillMaxWidth())
        NebDialogTextField(phone, { phone = it }, label = "Phone", isError = err("phone"), keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Phone), modifier = Modifier.fillMaxWidth())
        NebDialogTextField(email, { email = it }, label = "Email", isError = err("email"), keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email), modifier = Modifier.fillMaxWidth())
    }
    Section("Documents") {
        st.docs.forEach { doc ->
            Surface(shape = RoundedCornerShape(20.dp), color = c.surfaceContainerLow) {
                Column(Modifier.fillMaxWidth().padding(start = 14.dp, top = 4.dp, bottom = 10.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(doc.name, Modifier.weight(1f), fontSize = 13.sp, fontWeight = FontWeight.Medium, maxLines = 1, overflow = TextOverflow.Ellipsis)
                        IconButton(onClick = { vm.removeDoc(doc) }) { Icon(Icons.Outlined.Close, "Remove ${doc.name}", Modifier.size(18.dp)) }
                    }
                    Row(Modifier.fillMaxWidth().nebHorizontalScroll(rememberScrollState()).padding(end = 14.dp), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        DOC_TYPES.forEach { (k, l) -> NebSelectChip(l, doc.type == k, { vm.setDocType(doc, k) }) }
                    }
                }
            }
        }
        OutlinedButton(
            onClick = { pick.launch(arrayOf("application/pdf", "image/jpeg", "image/png", "image/webp")) },
            enabled = st.docs.size < 6, shape = RoundedCornerShape(24.dp), border = BorderStroke(1.5.dp, c.outlineVariant),
            modifier = Modifier.fillMaxWidth().heightIn(min = 52.dp)
        ) { Icon(Icons.Outlined.AttachFile, null, Modifier.size(18.dp)); Spacer(Modifier.width(8.dp)); Text(if (st.docs.isEmpty()) "Attach documents" else "Add another", fontSize = 14.sp, maxLines = 1, overflow = TextOverflow.Ellipsis) }
        Text("PDF, JPG, PNG or WebP. Up to 6 files, 8 MB each.", fontSize = 12.sp, color = c.onSurfaceVariant)
    }
    Section("Note to the reviewer") {
        NebDialogTextField(message, { message = it }, placeholder = "Optional", singleLine = false, minLines = 3, modifier = Modifier.fillMaxWidth())
    }
    st.error?.let { Text(it, color = c.error, fontSize = 13.sp) }
    Button(
        onClick = {
            tried = true
            if (bad.values.none { it } && st.docs.isNotEmpty()) {
                vm.send(slug, mapOf(
                    "name" to name.trim(), "kind" to kind, "district" to district.trim(), "address" to address.trim(), "website" to website.trim(),
                    "registration_no" to reg.trim(), "contact_name" to person.trim(), "contact_role" to role.trim(),
                    "contact_phone" to phone.trim(), "contact_email" to email.trim(), "message" to message.trim()
                ))
            } else if (st.docs.isEmpty() && bad.values.none { it }) vm.fail("Attach at least one document")
        },
        enabled = !st.sending, shape = RoundedCornerShape(28.dp), elevation = null,
        modifier = Modifier.fillMaxWidth().height(52.dp)
    ) { Text(if (st.sending) "Sending" else "Send application", fontWeight = FontWeight.SemiBold) }
}
