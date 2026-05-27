package com.neb.ians.ui.screens.forum

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.Button
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.neb.ians.data.SampleData

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CreatePostScreen(
    onBack: () -> Unit,
    onPostCreated: () -> Unit,
    viewModel: ForumViewModel = viewModel(),
) {
    var title by rememberSaveable { mutableStateOf("") }
    var body by rememberSaveable { mutableStateOf("") }
    var selectedSubject by rememberSaveable { mutableStateOf("") }
    var selectedGrade by rememberSaveable { mutableStateOf("") }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("New Question") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Filled.Close, "Close")
                    }
                },
                actions = {
                    Button(
                        onClick = {
                            if (title.isNotBlank() && body.isNotBlank()) {
                                viewModel.createPost(title, body, selectedSubject, selectedGrade)
                                onPostCreated()
                            }
                        },
                        enabled = title.isNotBlank() && body.isNotBlank(),
                    ) {
                        Text("Post")
                    }
                },
            )
        },
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(16.dp),
        ) {
            OutlinedTextField(
                value = title,
                onValueChange = { title = it },
                label = { Text("Title") },
                placeholder = { Text("What's your question?") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
            )

            Spacer(Modifier.height(12.dp))

            OutlinedTextField(
                value = body,
                onValueChange = { body = it },
                label = { Text("Details") },
                placeholder = { Text("Provide more context...") },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(160.dp),
                maxLines = 8,
            )

            Spacer(Modifier.height(16.dp))

            Text(
                "Subject (optional)",
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            LazyRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                contentPadding = PaddingValues(vertical = 4.dp),
            ) {
                items(SampleData.subjects) { subject ->
                    FilterChip(
                        selected = selectedSubject == subject,
                        onClick = {
                            selectedSubject = if (selectedSubject == subject) "" else subject
                        },
                        label = { Text(subject) },
                    )
                }
            }

            Spacer(Modifier.height(8.dp))

            Text(
                "Grade (optional)",
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            LazyRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                contentPadding = PaddingValues(vertical = 4.dp),
            ) {
                items(SampleData.grades) { grade ->
                    FilterChip(
                        selected = selectedGrade == grade,
                        onClick = {
                            selectedGrade = if (selectedGrade == grade) "" else grade
                        },
                        label = { Text(grade) },
                    )
                }
            }
        }
    }
}
