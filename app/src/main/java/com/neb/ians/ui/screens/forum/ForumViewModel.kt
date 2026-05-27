package com.neb.ians.ui.screens.forum

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.NEBiansApp
import com.neb.ians.data.local.entity.ForumPostEntity
import com.neb.ians.data.local.entity.ForumReplyEntity
import com.neb.ians.data.repository.ForumRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class ForumViewModel(application: Application) : AndroidViewModel(application) {

    private val db = (application as NEBiansApp).database
    private val repository = ForumRepository(db.forumDao())

    val posts: StateFlow<List<ForumPostEntity>> = repository.getAllPosts()
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    fun toggleThumb(postId: Long) {
        viewModelScope.launch {
            repository.toggleThumbPost(postId)
        }
    }

    fun createPost(title: String, body: String, subject: String, grade: String) {
        viewModelScope.launch {
            repository.insertPost(
                ForumPostEntity(
                    title = title,
                    body = body,
                    authorName = "You",
                    subject = subject,
                    grade = grade,
                )
            )
        }
    }

    fun getRepliesForPost(postId: Long): StateFlow<List<ForumReplyEntity>> {
        return repository.getRepliesForPost(postId)
            .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
    }

    private val _currentPost = MutableStateFlow<ForumPostEntity?>(null)
    val currentPost: StateFlow<ForumPostEntity?> = _currentPost.asStateFlow()

    fun loadPost(postId: Long) {
        viewModelScope.launch {
            _currentPost.value = repository.getPostById(postId)
        }
    }

    fun addReply(postId: Long, body: String, parentReplyId: Long? = null) {
        viewModelScope.launch {
            repository.insertReply(
                ForumReplyEntity(
                    postId = postId,
                    parentReplyId = parentReplyId,
                    body = body,
                    authorName = "You",
                )
            )
            val post = repository.getPostById(postId)
            if (post != null) {
                repository.updatePost(post.copy(replyCount = post.replyCount + 1))
            }
        }
    }

    fun toggleThumbReply(replyId: Long) {
        viewModelScope.launch {
            repository.toggleThumbReply(replyId)
        }
    }
}
