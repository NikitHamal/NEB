package com.neb.ians.ui.screens.profile

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiEntry
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebDialogTextField
import com.neb.ians.ui.components.NebFieldGroupLabel
import com.neb.ians.ui.components.NebModalSheet
import com.neb.ians.ui.components.NebSelectChip

private fun split(v: String): Pair<String, String> =
    v.split("-").let { (it.getOrNull(1)?.trimStart('0') ?: "") to (it.getOrNull(0) ?: "") }

private fun join(m: String, y: String): String {
    val year = y.filter(Char::isDigit).take(4)
    if (year.length != 4) return ""
    val month = m.filter(Char::isDigit).toIntOrNull()?.takeIf { it in 1..12 }
    return if (month != null) "$year-%02d".format(month) else year
}

/** Add or change one portfolio entry. Only the title is required; everything else can come later. */
@Composable
fun PortfolioEntrySheet(
    entry: ApiEntry,
    kindLabel: String,
    saving: Boolean,
    error: String?,
    onSave: (ApiEntry) -> Unit,
    onDelete: (() -> Unit)?,
    onDismiss: () -> Unit
) {
    var title by remember { mutableStateOf(entry.title) }
    var org by remember { mutableStateOf(entry.org) }
    var sm by remember { mutableStateOf(split(entry.start).first) }
    var sy by remember { mutableStateOf(split(entry.start).second) }
    var em by remember { mutableStateOf(split(entry.end).first) }
    var ey by remember { mutableStateOf(split(entry.end).second) }
    var current by remember { mutableStateOf(entry.isCurrent) }
    var desc by remember { mutableStateOf(entry.description) }
    var url by remember { mutableStateOf(entry.url) }
    NebModalSheet(onDismiss = onDismiss, title = (if (entry.id == 0) "Add " else "Edit ") + kindLabel.lowercase().trimEnd('s')) {
        Column(Modifier.verticalScroll(rememberScrollState()), verticalArrangement = Arrangement.spacedBy(14.dp)) {
            NebDialogTextField(title, { title = it.take(150) }, Modifier.fillMaxWidth(), label = "Title")
            NebDialogTextField(org, { org = it.take(150) }, Modifier.fillMaxWidth(), label = "Where")
            NebFieldGroupLabel("From")
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                NebDialogTextField(sm, { sm = it.take(2) }, Modifier.weight(1f), placeholder = "Month")
                NebDialogTextField(sy, { sy = it.take(4) }, Modifier.weight(1f), placeholder = "Year")
            }
            NebSelectChip("Still going", current, { current = !current })
            if (!current) {
                NebFieldGroupLabel("To")
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    NebDialogTextField(em, { em = it.take(2) }, Modifier.weight(1f), placeholder = "Month")
                    NebDialogTextField(ey, { ey = it.take(4) }, Modifier.weight(1f), placeholder = "Year")
                }
            }
            NebDialogTextField(desc, { desc = it.take(600) }, Modifier.fillMaxWidth(), label = "Details", singleLine = false, minLines = 3)
            NebDialogTextField(url, { url = it.take(300) }, Modifier.fillMaxWidth(), label = "Link", placeholder = "https://")
            if (error != null) Text(error, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
                if (onDelete != null) NebButton("Delete", onDelete, tone = NebButtonTone.Danger, enabled = !saving)
                NebButton(
                    "Save",
                    { onSave(entry.copy(title = title, org = org, start = join(sm, sy), end = if (current) "" else join(em, ey),
                        isCurrent = current, description = desc, url = url)) },
                    Modifier.weight(1f), loading = saving, fillWidth = true
                )
            }
        }
    }
}
