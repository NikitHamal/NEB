package com.neb.ians.ui.screens.institutions

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiInstDetail
import com.neb.ians.data.api.ApiInstSchema
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.async
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.booleanOrNull
import kotlinx.serialization.json.contentOrNull
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import kotlinx.serialization.json.longOrNull
import javax.inject.Inject

/** One institution page: read it, and, for its verified owner, change any field at any time. */
@HiltViewModel
class InstitutionViewModel @Inject constructor(
    private val api: ApiService,
    private val auth: AuthRepository
) : ViewModel() {
    data class State(
        val detail: ApiInstDetail? = null,
        val schema: ApiInstSchema = ApiInstSchema(),
        val loading: Boolean = true,
        val saving: Boolean = false,
        val error: String? = null,
        val saved: Boolean = false
    )

    private val _state = MutableStateFlow(State())
    val state: StateFlow<State> = _state.asStateFlow()

    private companion object {
        val detailCache = java.util.concurrent.ConcurrentHashMap<String, ApiInstDetail>()
        @Volatile var schemaCache: ApiInstSchema? = null
    }

    /**
     * Shows what is already known the moment the screen opens (the last copy of this page, the
     * schema from any earlier visit), then refreshes. The schema and the page are fetched side
     * by side, so the wait is the slower of the two rather than their sum.
     */
    fun load(slug: String) {
        viewModelScope.launch {
            val cached = detailCache[slug]
            _state.update { st ->
                st.copy(
                    detail = cached ?: st.detail?.takeIf { it.slug == slug },
                    schema = schemaCache ?: st.schema,
                    loading = cached == null,
                    error = null
                )
            }
            val schemaJob = if (schemaCache == null) async { runCatching { api.institutionSchema() }.getOrNull() } else null
            val token = runCatching { auth.getBearerToken() }.getOrNull()
            val detail = runCatching { api.institutionDetail(token, slug) }.getOrNull()
            val schema = schemaJob?.await()?.also { schemaCache = it }
            if (detail != null) detailCache[slug] = detail
            _state.update { st ->
                val keep = detail ?: st.detail?.takeIf { it.slug == slug }
                st.copy(
                    detail = keep,
                    schema = schema ?: st.schema,
                    loading = false,
                    error = if (keep == null) "Could not load this page." else null
                )
            }
        }
    }

    /** Sends only the keys that changed; the server keeps everything else. */
    fun save(slug: String, patch: Map<String, JsonElement>) {
        viewModelScope.launch {
            val token = auth.getBearerToken() ?: return@launch
            _state.update { it.copy(saving = true, error = null, saved = false) }
            val res = runCatching { api.updateInstitutionProfile(token, slug, JsonObject(patch)) }
            val body = res.getOrNull()
            _state.update { st ->
                if (body != null) {
                    val next = st.detail?.copy(portfolio = body.portfolio)
                    if (next != null) detailCache[slug] = next
                    st.copy(saving = false, saved = true, detail = next)
                } else st.copy(saving = false, error = "Could not save. Check the values and try again.")
            }
        }
    }

    fun clearSaved() = _state.update { it.copy(saved = false) }
}

// Readers for the loose `details` map.
fun Map<String, JsonElement>.str(key: String): String = (this[key] as? JsonPrimitive)?.contentOrNull.orEmpty()
fun Map<String, JsonElement>.num(key: String): Long? = (this[key] as? JsonPrimitive)?.longOrNull
fun Map<String, JsonElement>.flag(key: String): Boolean = (this[key] as? JsonPrimitive)?.booleanOrNull ?: false
fun Map<String, JsonElement>.list(key: String): List<String> =
    (this[key] as? JsonArray)?.mapNotNull { (it as? JsonPrimitive)?.contentOrNull } ?: emptyList()
fun Map<String, JsonElement>.rows(key: String): List<Map<String, String>> =
    (this[key] as? JsonArray)?.mapNotNull { el ->
        runCatching { el.jsonObject.mapValues { it.value.jsonPrimitive.contentOrNull.orEmpty() } }.getOrNull()
    } ?: emptyList()

fun money(v: Long?): String = if (v == null) "" else "Rs " + "%,d".format(v)

/** What the list a user tapped from already knew about a page, so the page can name itself while it loads. */
object InstitutionPeek {
    data class Peek(val name: String, val kindLabel: String)
    private val rows = java.util.concurrent.ConcurrentHashMap<String, Peek>()
    fun put(slug: String, name: String, kindLabel: String) { rows[slug] = Peek(name, kindLabel) }
    fun get(slug: String): Peek? = rows[slug]
}
