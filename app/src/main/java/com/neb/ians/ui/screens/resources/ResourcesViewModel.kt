package com.neb.ians.ui.screens.resources

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.NEBiansApp
import com.neb.ians.data.local.entity.ResourceEntity
import com.neb.ians.data.repository.ResourceRepository
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.stateIn

class ResourcesViewModel(application: Application) : AndroidViewModel(application) {

    private val db = (application as NEBiansApp).database
    private val repository = ResourceRepository(db.resourceDao(), db.bookmarkDao())

    val selectedSubject = MutableStateFlow("")
    val selectedGrade = MutableStateFlow("")
    val selectedType = MutableStateFlow("")

    @OptIn(ExperimentalCoroutinesApi::class)
    val filteredResources: StateFlow<List<ResourceEntity>> =
        combine(selectedSubject, selectedGrade, selectedType) { subject, grade, type ->
            Triple(subject, grade, type)
        }.flatMapLatest { (subject, grade, type) ->
            repository.getFilteredResources(subject, grade, type)
        }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    fun setSubject(subject: String) {
        selectedSubject.value = subject
    }

    fun setGrade(grade: String) {
        selectedGrade.value = grade
    }

    fun setType(type: String) {
        selectedType.value = type
    }
}
