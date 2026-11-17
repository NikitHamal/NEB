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
    data class Doc(val uri: Uri, val name: String)
    data class State(
        val detail: ApiInstDetail? = null,
        val application: ApiInstApplication? = null,
        val docs: List<Doc> = emptyList(),
        val loading: Boolean = true,
        val sending: Boolean = false,
        val error: String? = null,
        val canClaim: Boolean = true
    )

    private val _state = MutableStateFlow(State())
    val state: StateFlow<State> = _state.asStateFlow()

    fun load(slug: String) = viewModelScope.launch {
        val token = runCatching { auth.getBearerToken() }.getOrNull()
        val detail = runCatching { api.institutionDetail(token, slug) }.getOrNull()
        val mine = token?.let { runCatching { api.myInstitution(it) }.getOrNull() }
        _state.update { it.copy(detail = detail, application = mine?.application?.takeIf { a -> a.status != "rejected" },
            loading = false, canClaim = token != null) }
    }

    fun addDocs(uris: List<Uri>) {
        val add = uris.map { u -> Doc(u, nameOf(u)) }
        _state.update { it.copy(docs = (it.docs + add).distinctBy { d -> d.uri }.take(4), error = null) }
    }

    fun removeDoc(d: Doc) = _state.update { it.copy(docs = it.docs - d) }

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
                s.docs.mapNotNull { d ->
                    runCatching {
                        val mime = context.contentResolver.getType(d.uri) ?: "application/octet-stream"
                        val bytes = context.contentResolver.openInputStream(d.uri)!!.use { it.readBytes() }
                        MultipartBody.Part.createFormData("documents", d.name, bytes.toRequestBody(mime.toMediaTypeOrNull()))
                    }.getOrNull()
                }
            }
            val res = runCatching {
                api.claimInstitution(token, slug, fields.mapValues { it.value.toRequestBody(text) }, parts)
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

    private fun errorOf(e: Throwable?): String {
        val body = (e as? HttpException)?.response()?.errorBody()?.string()
        val msg = body?.let { runCatching { JSONObject(it).optString("error") }.getOrNull() }
        return msg?.takeIf { it.isNotBlank() } ?: "Could not send. Check your connection and try again."
    }
}
