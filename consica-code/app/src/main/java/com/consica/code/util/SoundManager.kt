package com.consica.code.util

import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioTrack
import com.consica.code.data.prefs.UserPreferencesRepository
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject
import javax.inject.Singleton
import kotlin.math.PI
import kotlin.math.min
import kotlin.math.sin

enum class AppSound { TAP, SUCCESS, REWARD, GENTLE_ERROR, GROW }

/**
 * Plays soft, synthesized chimes so no audio assets are required and the app
 * stays small and fully offline. All sounds respect the learner's setting.
 */
@Singleton
class SoundManager @Inject constructor(
    prefs: UserPreferencesRepository,
) {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)
    private val soundEnabled = prefs.settings
        .map { it.soundEnabled }
        .stateIn(scope, SharingStarted.Eagerly, true)

    fun play(sound: AppSound) {
        if (!soundEnabled.value) return
        scope.launch {
            runCatching {
                when (sound) {
                    AppSound.TAP -> tone(listOf(660.0 to 60))
                    AppSound.SUCCESS -> tone(listOf(523.25 to 90, 659.25 to 90, 783.99 to 140))
                    AppSound.REWARD -> tone(listOf(523.25 to 80, 659.25 to 80, 783.99 to 80, 1046.5 to 180))
                    AppSound.GENTLE_ERROR -> tone(listOf(392.0 to 110, 329.63 to 160))
                    AppSound.GROW -> tone(listOf(440.0 to 70, 554.37 to 70, 659.25 to 130))
                }
            }
        }
    }

    private fun tone(notes: List<Pair<Double, Int>>, sampleRate: Int = 22050) {
        val totalMs = notes.sumOf { it.second }
        val totalSamples = sampleRate * totalMs / 1000
        val buffer = ShortArray(totalSamples)
        var index = 0
        for ((freq, durationMs) in notes) {
            val samples = sampleRate * durationMs / 1000
            for (i in 0 until samples) {
                if (index >= totalSamples) break
                val t = i.toDouble() / sampleRate
                val fadeIn = min(1.0, i / (sampleRate * 0.005))
                val fadeOut = min(1.0, (samples - i) / (sampleRate * 0.03))
                val amplitude = 0.18 * fadeIn * fadeOut
                buffer[index++] = (sin(2 * PI * freq * t) * amplitude * Short.MAX_VALUE).toInt().toShort()
            }
        }

        val track = AudioTrack.Builder()
            .setAudioAttributes(
                AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_GAME)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                    .build()
            )
            .setAudioFormat(
                AudioFormat.Builder()
                    .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                    .setSampleRate(sampleRate)
                    .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
                    .build()
            )
            .setTransferMode(AudioTrack.MODE_STATIC)
            .setBufferSizeInBytes(buffer.size * 2)
            .build()

        track.write(buffer, 0, buffer.size)
        track.play()
        Thread.sleep(totalMs.toLong() + 50)
        track.release()
    }
}
