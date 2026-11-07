package com.neb.ians.ui.screens.notes

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.speech.LocalTtsId
import com.neb.ians.speech.ModelState
import com.neb.ians.speech.PhononEngine
import com.neb.ians.speech.PhononVoice
import com.neb.ians.speech.ReadState
import com.neb.ians.speech.SpeechModelId
import com.neb.ians.speech.SpeechModelManager
import com.neb.ians.speech.VoiceCatalog
import com.neb.ians.speech.WhistleEngine
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import javax.inject.Inject

/** State and actions for setting up the on-device speech models. */
@HiltViewModel
class SpeechViewModel @Inject constructor(
    private val models: SpeechModelManager,
    private val whistle: WhistleEngine,
    private val phonon: PhononEngine,
) : ViewModel() {
    val stt: StateFlow<ModelState> = models.stt

    /** The Phonon model on its own. */
    val phononState: StateFlow<ModelState> = models.tts

    /** Installed as soon as any read-aloud voice is on the phone, Phonon or a local ONNX voice. */
    val tts: StateFlow<ModelState> = combine(models.tts, models.local) { phononModel, local ->
        when {
            phononModel is ModelState.Installed -> phononModel
            else -> local.values.filterIsInstance<ModelState.Installed>().firstOrNull() ?: phononModel
        }
    }.stateIn(viewModelScope, SharingStarted.Eagerly, models.tts.value)

    val local: StateFlow<Map<LocalTtsId, ModelState>> = models.local
    val localVoices: StateFlow<Map<LocalTtsId, String>> = models.localVoices
    val engine: StateFlow<String> = models.engine

    val sttLanguage: StateFlow<String> = models.sttLanguage
    val voice: StateFlow<String> = models.voice
    val installedVoices: StateFlow<List<String>> = models.installedVoices
    val voiceBusy: StateFlow<Set<String>> = models.voiceBusy
    val catalog: StateFlow<VoiceCatalog> = models.catalog
    val readState: StateFlow<ReadState> = phonon.state

    val sttSupported: Boolean get() = whistle.supported
    val ttsSupported: Boolean get() = phonon.supported

    fun download(id: SpeechModelId) = models.download(id)
    fun cancel(id: SpeechModelId) = models.cancel(id)
    fun remove(id: SpeechModelId) = models.remove(id)
    fun setSttLanguage(code: String) = models.setSttLanguage(code)
    fun loadCatalog() = models.loadCatalog()
    fun downloadVoice(v: PhononVoice) = models.downloadVoice(v)
    fun removeVoice(name: String) = models.removeVoice(name)

    fun useVoice(name: String) {
        models.setEngine("phonon")
        models.setVoice(name)
    }

    fun downloadLocal(id: LocalTtsId) = models.downloadLocal(id)
    fun cancelLocal(id: LocalTtsId) = models.cancelLocal(id)
    fun removeLocal(id: LocalTtsId) {
        models.removeLocal(id)
        if (models.engine.value == id.key) models.setEngine("phonon")
    }

    fun useLocalVoice(id: LocalTtsId, voice: String) {
        models.setEngine(id.key)
        models.setLocalVoice(id, voice)
    }

    fun preview(name: String) {
        if (phonon.state.value == ReadState.Speaking || phonon.state.value == ReadState.Loading) {
            phonon.stop()
            return
        }
        phonon.play(listOf("Hello, this is how I will read your notes."), 0, name, "phonon")
    }

    fun previewLocal(id: LocalTtsId, voice: String) {
        if (phonon.state.value == ReadState.Speaking || phonon.state.value == ReadState.Loading) {
            phonon.stop()
            return
        }
        phonon.play(listOf("Hello, this is how I will read your notes."), 0, voice, id.key)
    }

    fun stopPreview() = phonon.stop()
    fun clearError() = phonon.clearError()

    override fun onCleared() {
        phonon.stop()
        super.onCleared()
    }
}
