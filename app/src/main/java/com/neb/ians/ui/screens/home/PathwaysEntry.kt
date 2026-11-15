package com.neb.ians.ui.screens.home

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.ChevronRight
import androidx.compose.material.icons.outlined.School
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

/** One row at the top of Home: the door to Pathways (open to guests). */
@Composable
fun PathwaysEntry(onClick: () -> Unit, modifier: Modifier = Modifier) {
    val c = MaterialTheme.colorScheme
    Surface(
        onClick = onClick,
        modifier = modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
        shape = RoundedCornerShape(24.dp),
        color = c.primaryContainer,
        contentColor = c.onPrimaryContainer,
    ) {
        Row(Modifier.padding(horizontal = 18.dp, vertical = 14.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) {
            Icon(Icons.Outlined.School, null, Modifier.size(28.dp))
            Column(Modifier.weight(1f)) {
                Text("Pathways", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
                Text("What to study after Class 8, SEE, +2 and a bachelor", style = MaterialTheme.typography.bodySmall)
            }
            Icon(Icons.Outlined.ChevronRight, null, Modifier.size(24.dp))
        }
    }
}
