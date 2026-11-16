package com.neb.ians.ui.screens.profile

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiEntry
import com.neb.ians.data.api.ApiEntryBody
import com.neb.ians.data.api.ApiEntrySection
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

/** One profile's portfolio entries. Read for anyone, add / edit / delete for the owner. */
@HiltViewModel
class PortfolioViewModel @Inject constructor(
    private val api: ApiService,
    private val auth: AuthRepository
) : ViewModel() {
    data class State(
        val sections: List<ApiEntrySection> = emptyList(),
        val loaded: Boolean = false,
        val saving: Boolean = false,
        val error: String? = null
    )

    private val _state = MutableStateFlow(State())
    val state: StateFlow<State> = _state.asStateFlow()
    private var username = ""

    fun load(name: String, force: Boolean = false) {
        if (name == username && _state.value.loaded && !force) return
        username = name
        viewModelScope.launch {
            val token = runCatching { auth.getBearerToken() }.getOrNull()
            val res = runCatching { api.userPortfolio(token, name) }.getOrNull()
            _state.update { it.copy(sections = res?.sections ?: it.sections, loaded = true) }
        }
    }

    fun clearError() = _state.update { it.copy(error = null) }

    /** [entry] with id 0 is new. [done] runs on success so the sheet can close. */
    fun save(entry: ApiEntry, done: () -> Unit) {
        if (entry.title.isBlank()) { _state.update { it.copy(error = "A title is required.") }; return }
        viewModelScope.launch {
            _state.update { it.copy(saving = true, error = null) }
            val token = auth.getBearerToken()
            val body = ApiEntryBody(entry.kind, entry.title.trim(), entry.org.trim(), entry.start, entry.end,
                entry.isCurrent, entry.description.trim(), entry.url.trim())
            val res = runCatching {
                if (token == null) null
                else if (entry.id == 0) api.addEntry(token, body) else api.editEntry(token, entry.id, body)
            }
            val saved = res.getOrNull()
            val error = saved?.error ?: if (saved == null) "Could not save. Check your connection." else null
            _state.update { it.copy(saving = false, error = error) }
            if (error == null) { reload(); done() }
        }
    }

    fun delete(id: Int, done: () -> Unit) {
        viewModelScope.launch {
            val token = auth.getBearerToken() ?: return@launch
            _state.update { it.copy(saving = true) }
            runCatching { api.deleteEntry(token, id) }
            _state.update { it.copy(saving = false) }
            reload(); done()
        }
    }

    private suspend fun reload() {
        val token = runCatching { auth.getBearerToken() }.getOrNull()
        runCatching { api.userPortfolio(token, username) }.getOrNull()?.let { r ->
            _state.update { it.copy(sections = r.sections) }
        }
    }
}
