package com.agentx.app.ui.screens.assistant

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.agentx.app.data.chat.ChatRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

@HiltViewModel
class ConversationsViewModel @Inject constructor(
    private val chatRepository: ChatRepository
) : ViewModel() {

    val conversations = chatRepository.observeConversations()
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    init {
        viewModelScope.launch { chatRepository.ensureLegacyMigrated() }
    }

    suspend fun createNew(): String = chatRepository.createConversation()

    fun rename(id: String, title: String) {
        viewModelScope.launch { chatRepository.renameConversation(id, title) }
    }

    fun delete(id: String) {
        viewModelScope.launch { chatRepository.deleteConversation(id) }
    }

    fun clear(id: String) {
        viewModelScope.launch { chatRepository.clearConversation(id) }
    }
}
