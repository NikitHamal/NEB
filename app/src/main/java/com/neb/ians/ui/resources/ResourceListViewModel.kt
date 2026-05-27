package com.neb.ians.ui.resources

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import com.neb.ians.NEBiansApp
import com.neb.ians.data.model.Grade
import com.neb.ians.data.model.Resource
import com.neb.ians.data.model.ResourceType
import com.neb.ians.data.model.Subject
import com.neb.ians.data.repository.ResourceRepository
import kotlinx.coroutines.launch

class ResourceListViewModel(application: Application) : AndroidViewModel(application) {

    private val repository = ResourceRepository((application as NEBiansApp).database.resourceDao())

    private val _results = MutableLiveData<List<Resource>>(emptyList())
    val results: LiveData<List<Resource>> = _results

    private val _isLoading = MutableLiveData(false)
    val isLoading: LiveData<Boolean> = _isLoading

    private var currentQuery: String = ""
    private var currentSubject: Subject? = null
    private var currentGrade: Grade? = null
    private var currentType: ResourceType? = null

    fun search(query: String) {
        currentQuery = query
        applyFilters()
    }

    fun setSubjectFilter(subject: Subject?) {
        currentSubject = subject
        applyFilters()
    }

    fun setGradeFilter(grade: Grade?) {
        currentGrade = grade
        applyFilters()
    }

    fun setTypeFilter(type: ResourceType?) {
        currentType = type
        applyFilters()
    }

    private fun applyFilters() {
        viewModelScope.launch {
            _isLoading.value = true
            val list = if (currentQuery.isNotBlank()) {
                repository.search(currentQuery)
            } else {
                // Return all when no search query; in a real app, you'd paginate.
                // For this minimal app, return all seeded data.
                repository.getAll()
            }
            val filtered = list.filter {
                (currentSubject == null || it.subject == currentSubject) &&
                (currentGrade == null || it.grade == currentGrade) &&
                (currentType == null || it.type == currentType)
            }
            _results.postValue(filtered)
            _isLoading.value = false
        }
    }
}
