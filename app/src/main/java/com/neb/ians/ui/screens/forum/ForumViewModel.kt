package com.neb.ians.ui.screens.forum

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.model.ForumPost
import com.neb.ians.data.model.Reply
import com.neb.ians.data.repository.ForumRepository
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class ForumViewModel(private val repository: ForumRepository) : ViewModel() {
    val posts = repository.getPosts()
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    fun addPost(title: String, body: String, author: String) {
        viewModelScope.launch {
            repository.insertPost(
                ForumPost(title = title, body = body, author = author)
            )
        }
    }

    fun thumbPost(postId: Long) {
        viewModelScope.launch { repository.thumbPost(postId) }
    }

    fun addReply(postId: Long, body: String, author: String) {
        viewModelScope.launch {
            repository.insertReply(Reply(postId = postId, body = body, author = author))
        }
    }
}
