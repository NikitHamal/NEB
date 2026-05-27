package com.neb.ians.ui.screens.forum

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.model.ForumPost
import com.neb.ians.data.model.Reply
import com.neb.ians.data.repository.ForumRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class ForumAnswerViewModel(
    private val postId: Long,
    private val forumRepository: ForumRepository
) : ViewModel() {
    private val _post = MutableStateFlow<ForumPost?>(null)
    val post: StateFlow<ForumPost?> = _post

    val replies: StateFlow<List<Reply>> = forumRepository.getReplies(postId)
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    fun load() {
        viewModelScope.launch {
            _post.value = forumRepository.getPostById(postId)
        }
    }

    fun thumbReply(replyId: Long) {
        viewModelScope.launch { forumRepository.thumbReply(replyId) }
    }
}
