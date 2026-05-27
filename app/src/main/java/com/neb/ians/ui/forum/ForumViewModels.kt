package com.neb.ians.ui.forum

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.ForumRepository
import com.neb.ians.data.local.ForumReplyEntity
import com.neb.ians.data.local.ForumThreadEntity
import com.neb.ians.data.prefs.UserPrefsRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

@HiltViewModel
class ForumListViewModel @Inject constructor(
    private val repo: ForumRepository,
) : ViewModel() {
    val threads: StateFlow<List<ForumThreadEntity>> =
        repo.threads().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())

    fun like(id: Long) = viewModelScope.launch { repo.likeThread(id) }
}

@HiltViewModel
class ThreadViewModel @Inject constructor(
    private val repo: ForumRepository,
    savedStateHandle: SavedStateHandle,
) : ViewModel() {
    private val threadId: Long = savedStateHandle["threadId"] ?: 0L

    val thread: StateFlow<ForumThreadEntity?> =
        repo.thread(threadId).stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), null)
    val replies: StateFlow<List<ForumReplyEntity>> =
        repo.replies(threadId).stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())

    fun likeThread() = viewModelScope.launch { repo.likeThread(threadId) }
    fun likeReply(id: Long) = viewModelScope.launch { repo.likeReply(id) }
}

@HiltViewModel
class ReplyViewModel @Inject constructor(
    private val repo: ForumRepository,
    private val prefs: UserPrefsRepository,
    savedStateHandle: SavedStateHandle,
) : ViewModel() {
    private val threadId: Long = savedStateHandle["threadId"] ?: 0L

    suspend fun submit(body: String): Boolean {
        if (body.isBlank()) return false
        val handle = prefs.flow.first().handle.ifBlank { "Student" }
        repo.postReply(
            ForumReplyEntity(threadId = threadId, body = body.trim(), author = handle)
        )
        return true
    }
}

@HiltViewModel
class NewThreadViewModel @Inject constructor(
    private val repo: ForumRepository,
    private val prefs: UserPrefsRepository,
) : ViewModel() {
    suspend fun submit(title: String, body: String, tags: String): Boolean {
        if (title.isBlank() || body.isBlank()) return false
        val handle = prefs.flow.first().handle.ifBlank { "Student" }
        repo.postThread(
            ForumThreadEntity(
                title = title.trim(),
                body = body.trim(),
                tags = tags.trim(),
                author = handle,
            )
        )
        return true
    }
}
