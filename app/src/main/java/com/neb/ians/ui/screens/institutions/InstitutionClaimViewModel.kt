package com.neb.ians.ui.screens.institutions

import android.content.Context
import android.net.Uri
import android.provider.OpenableColumns
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiInstApplication
import com.neb.ians.data.api.ApiInstDetail
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import retrofit2.HttpException
import javax.inject.Inject

/** Claim an institution in the app: details, documents, then the review status. */
@HiltViewModel
class InstitutionClaimViewModel @Inject constructor(
    @ApplicationContext private val context: Context,
    private val api: ApiService,
    private val auth: AuthRepository
) : ViewModel() {
    data class Doc(val uri: Uri, val name: String, val type: String = "registration", val size: Long = 0)
    data class State(
        val detail: ApiInstDetail? = null,
        val application: ApiInstApplication? = null,
        val docs: List<Doc> = emptyList(),
        val loading: Boolean = true,
        val sending: Boolean = false,
        val error: String? = null,
        val canClaim: Boolean = true,
        val role: String = "",
        val email: String = "",
        val signedIn: Boolean = true
    )

    private val _state = MutableStateFlow(State())
    val state: StateFlow<State> = _state.asStateFlow()

    /** [slug] is [NEW] for an institution that is not in the catalogue: there is no page to read, only the form. */
    fun load(slug: String) = viewModelScope.launch {
        val token = runCatching { auth.getBearerToken() }.getOrNull()
        val detail = if (slug == NEW) null else runCatching { api.institutionDetail(token, slug) }.getOrNull()
        val mine = token?.let { runCatching { api.myInstitution(it) }.getOrNull() }
        _state.update {
            it.copy(detail = detail, application = mine?.application?.takeIf { a -> a.status != "rejected" },
                loading = false, signedIn = token != null, role = mine?.role.orEmpty(), email = mine?.email.orEmpty(),
                canClaim = token != null && (mine == null || mine.role == "institution"))
        }
    }

    fun setDocType(d: Doc, type: String) = _state.update { st -> st.copy(docs = st.docs.map { if (it == d) it.copy(type = type) else it }) }

    fun addDocs(uris: List<Uri>) {
        _state.update { st ->
            val seen = st.docs.map { it.uri }.toSet()
            val fresh = uris.filter { it !in seen }.mapIndexed { i, u ->
                Doc(u, nameOf(u), type = if (st.docs.isEmpty() && i == 0) "registration" else "other", size = sizeOf(u))
            }
            val big = fresh.any { it.size > MAX_BYTES }
            st.copy(
                docs = (st.docs + fresh.filter { it.size <= MAX_BYTES }).take(6),
                error = if (big) "Each document must be under 8 MB" else null
            )
        }
    }

    fun fail(message: String) = _state.update { it.copy(error = message) }

    fun removeDoc(d: Doc) = _state.update { it.copy(docs = it.docs - d) }

    private fun sizeOf(u: Uri): Long = runCatching {
        context.contentResolver.query(u, null, null, null, null)?.use { c ->
            val i = c.getColumnIndex(OpenableColumns.SIZE)
            if (c.moveToFirst() && i >= 0) c.getLong(i) else 0L
        }
    }.getOrNull() ?: 0L

    private fun nameOf(u: Uri): String = runCatching {
        context.contentResolver.query(u, null, null, null, null)?.use { c ->
            val i = c.getColumnIndex(OpenableColumns.DISPLAY_NAME)
            if (c.moveToFirst() && i >= 0) c.getString(i) else null
        }
    }.getOrNull() ?: "document"

    fun send(slug: String, fields: Map<String, String>) {
        val s = _state.value
        if (s.sending) return
        if (s.docs.isEmpty()) { _state.update { it.copy(error = "Attach at least one document") }; return }
        viewModelScope.launch {
            _state.update { it.copy(sending = true, error = null) }
            val token = auth.getBearerToken()
            if (token == null) { _state.update { it.copy(sending = false, error = "Sign in first") }; return@launch }
            val text = "text/plain".toMediaTypeOrNull()
            val parts = withContext(Dispatchers.IO) {
                // doc_type repeats once per document, in file order, so each pair goes in together
                s.docs.flatMap { d ->
                    runCatching {
                        val mime = context.contentResolver.getType(d.uri) ?: "application/octet-stream"
                        val bytes = context.contentResolver.openInputStream(d.uri)!!.use { it.readBytes() }
                        listOf(
                            MultipartBody.Part.createFormData("doc_type", d.type),
                            MultipartBody.Part.createFormData("documents", d.name, bytes.toRequestBody(mime.toMediaTypeOrNull()))
                        )
                    }.getOrDefault(emptyList())
                }
            }
            val body = fields.mapValues { it.value.toRequestBody(text) }
            val withTypes = LinkedHashMap<String, okhttp3.RequestBody>(body)
            val res = runCatching {
                if (slug == NEW) api.claimNewInstitution(token, withTypes, parts)
                else api.claimInstitution(token, slug, withTypes, parts)
            }
            val ok = res.getOrNull()
            _state.update {
                when {
                    ok?.application != null -> it.copy(sending = false, application = ok.application)
                    else -> it.copy(sending = false, error = errorOf(res.exceptionOrNull()))
                }
            }
        }
    }

    companion object {
        const val NEW = "new"
        const val MAX_BYTES = 8L * 1024 * 1024
    }

    private fun errorOf(e: Throwable?): String {
        val body = (e as? HttpException)?.response()?.errorBody()?.string()
        val msg = body?.let { runCatching { JSONObject(it).optString("error") }.getOrNull() }
        return msg?.takeIf { it.isNotBlank() } ?: "Could not send. Check your connection and try again."
    }
}
