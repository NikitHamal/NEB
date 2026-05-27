package com.neb.ians.ui.main

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.asLiveData
import androidx.lifecycle.viewModelScope
import com.neb.ians.NEBiansApp
import com.neb.ians.data.model.Resource
import com.neb.ians.data.repository.ResourceRepository
import kotlinx.coroutines.launch

class MainViewModel(application: Application) : AndroidViewModel(application) {

    private val repository = ResourceRepository((application as NEBiansApp).database.resourceDao())

    val resources: LiveData<List<Resource>> = repository.allResourcesFlow.asLiveData()

    private val _isLoading = MutableLiveData(false)
    val isLoading: LiveData<Boolean> = _isLoading

    init {
        viewModelScope.launch {
            _isLoading.value = true
            repository.seedData()
            _isLoading.value = false
        }
    }
}
