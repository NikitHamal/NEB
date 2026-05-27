package com.neb.ians.ui.forum

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.db.PostEntity
import com.neb.ians.data.db.ThreadEntity
import com.neb.ians.data.repo.ForumRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class ForumViewModel @Inject constructor(
    private val repo: ForumRepository,
) : ViewModel() {
    val threads: StateFlow<List<ThreadEntity>> =
        repo.threads().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())

    fun toggleThumb(id: String) = viewModelScope.launch { repo.toggleThreadThumb(id) }
}

@OptIn(ExperimentalCoroutinesApi::class)
@HiltViewModel
class ThreadViewModel @Inject constructor(
    private val repo: ForumRepository,
) : ViewModel() {

    private val threadIdFlow = MutableStateFlow<String?>(null)

    val thread: StateFlow<ThreadEntity?> = threadIdFlow
        .flatMapLatest { id -> if (id == null) flowOf<ThreadEntity?>(null) else repo.thread(id) }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), null)

    val posts: StateFlow<List<PostEntity>> = threadIdFlow
        .flatMapLatest { id -> if (id == null) flowOf(emptyList()) else repo.posts(id) }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())

    fun load(id: String) { threadIdFlow.value = id }

    fun toggleThreadThumb(id: String) = viewModelScope.launch { repo.toggleThreadThumb(id) }
    fun togglePostThumb(post: PostEntity) = viewModelScope.launch { repo.togglePostThumb(post) }
}

@HiltViewModel
class ReplyViewModel @Inject constructor(
    private val repo: ForumRepository,
) : ViewModel() {
    fun reply(threadId: String, body: String, parentId: String? = null, onDone: () -> Unit) {
        viewModelScope.launch {
            repo.reply(threadId, body.trim(), author = "you", parentId = parentId)
            onDone()
        }
    }

    fun createThread(title: String, body: String, subject: String?, grade: String?, onDone: (String) -> Unit) {
        viewModelScope.launch {
            val id = repo.createThread(title.trim(), body.trim(), author = "you", subject = subject, grade = grade)
            onDone(id)
        }
    }
}
