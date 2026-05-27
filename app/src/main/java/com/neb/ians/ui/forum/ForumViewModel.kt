package com.neb.ians.ui.forum

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.asLiveData
import androidx.lifecycle.viewModelScope
import com.neb.ians.NEBiansApp
import com.neb.ians.data.model.ForumReply
import com.neb.ians.data.model.ForumThread
import com.neb.ians.data.repository.ForumRepository
import kotlinx.coroutines.launch

class ForumViewModel(application: Application) : AndroidViewModel(application) {

    private val repository = ForumRepository(
        (application as NEBiansApp).database.forumThreadDao(),
        application.database.forumReplyDao()
    )

    val threads: LiveData<List<ForumThread>> = repository.allThreads

    private val _replies = MutableLiveData<List<ForumReply>>(emptyList())
    val replies: LiveData<List<ForumReply>> = _replies

    private val _isLoading = MutableLiveData(false)
    val isLoading: LiveData<Boolean> = _isLoading

    init {
        viewModelScope.launch {
            _isLoading.value = true
            repository.seedSampleThreads()
            _isLoading.value = false
        }
    }

    fun createThread(title: String, body: String) {
        viewModelScope.launch {
            repository.createThread(title, body)
        }
    }

    fun loadReplies(threadId: String) {
        viewModelScope.launch {
            _replies.value = repository.getReplies(threadId)
        }
    }

    fun addReply(threadId: String, body: String) {
        viewModelScope.launch {
            repository.addReply(threadId, body)
            loadReplies(threadId)
        }
    }

    fun likeThread(id: String) {
        viewModelScope.launch {
            repository.likeThread(id)
        }
    }

    fun likeReply(id: String) {
        viewModelScope.launch {
            repository.likeReply(id)
        }
    }
}
