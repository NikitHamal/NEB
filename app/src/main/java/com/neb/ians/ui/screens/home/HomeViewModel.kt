package com.neb.ians.ui.screens.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.model.ContentItem
import com.neb.ians.data.repository.ContentRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class HomeViewModel(private val repository: ContentRepository) : ViewModel() {
    val recentItems: StateFlow<List<ContentItem>> = repository.getAll()
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    fun seedDataIfEmpty() {
        viewModelScope.launch {
            if (recentItems.value.isEmpty()) {
                _isLoading.value = true
                repository.insertAll(sampleContent)
                _isLoading.value = false
            }
        }
    }
}

val sampleContent = listOf(
    ContentItem(
        title = "NEB Physics Grade 11 Textbook",
        description = "Complete physics textbook for Grade 11 NEB curriculum.",
        subject = "Physics",
        grade = "Grade 11",
        type = "Textbook",
        fileUrl = "https://example.com/physics11.pdf",
        thumbnailUrl = null
    ),
    ContentItem(
        title = "Chemistry Notes - Grade 12",
        description = "Handwritten and typed notes covering all chapters.",
        subject = "Chemistry",
        grade = "Grade 12",
        type = "Notes",
        fileUrl = "https://example.com/chem12_notes.pdf",
        thumbnailUrl = null
    ),
    ContentItem(
        title = "Mathematics Past Papers 2080",
        description = "Collection of previous year mathematics question papers.",
        subject = "Mathematics",
        grade = "Grade 12",
        type = "Past Papers",
        fileUrl = "https://example.com/math_past_2080.pdf",
        thumbnailUrl = null
    ),
    ContentItem(
        title = "Biology Grade 11 Solutions",
        description = "Chapter-wise solutions for NEB Biology.",
        subject = "Biology",
        grade = "Grade 11",
        type = "Solutions",
        fileUrl = "https://example.com/bio11_solutions.pdf",
        thumbnailUrl = null
    ),
    ContentItem(
        title = "English Grammar Notes",
        description = "Comprehensive grammar notes for NEB English.",
        subject = "English",
        grade = "Grade 11",
        type = "Notes",
        fileUrl = "https://example.com/english_grammar.pdf",
        thumbnailUrl = null
    ),
    ContentItem(
        title = "Nepali Byakaran Grade 12",
        description = "Complete Nepali grammar reference for Grade 12.",
        subject = "Nepali",
        grade = "Grade 12",
        type = "Textbook",
        fileUrl = "https://example.com/nepali12.pdf",
        thumbnailUrl = null
    ),
    ContentItem(
        title = "Computer Science Practical Guide",
        description = "Practical programming exercises and solutions.",
        subject = "Computer Science",
        grade = "Grade 11",
        type = "Notes",
        fileUrl = "https://example.com/cs_practical.pdf",
        thumbnailUrl = null
    ),
    ContentItem(
        title = "Physics Past Papers 2080",
        description = "NEB Physics board exam papers with marking schemes.",
        subject = "Physics",
        grade = "Grade 12",
        type = "Past Papers",
        fileUrl = "https://example.com/physics_past_2080.pdf",
        thumbnailUrl = null
    )
)
