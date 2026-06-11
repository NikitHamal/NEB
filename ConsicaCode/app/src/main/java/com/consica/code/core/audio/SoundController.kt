package com.consica.code.core.audio

import android.media.AudioManager
import android.media.ToneGenerator
import androidx.compose.runtime.staticCompositionLocalOf

/** Soft, optional sound feedback generated with [ToneGenerator] — no audio assets required. */
enum class Sfx { Tap, Success, Reward, GentleError, Grow }

class SoundController {
    @Volatile var enabled: Boolean = true

    private val tone: ToneGenerator? = runCatching {
        ToneGenerator(AudioManager.STREAM_MUSIC, 55) // low, child-friendly volume
    }.getOrNull()

    fun play(sfx: Sfx) {
        if (!enabled) return
        val gen = tone ?: return
        runCatching {
            when (sfx) {
                Sfx.Tap -> gen.startTone(ToneGenerator.TONE_PROP_BEEP, 40)
                Sfx.Success -> gen.startTone(ToneGenerator.TONE_CDMA_ALERT_CALL_GUARD, 150)
                Sfx.Reward -> gen.startTone(ToneGenerator.TONE_CDMA_HIGH_L, 220)
                Sfx.GentleError -> gen.startTone(ToneGenerator.TONE_PROP_NACK, 120)
                Sfx.Grow -> gen.startTone(ToneGenerator.TONE_CDMA_PIP, 160)
            }
        }
    }

    fun release() = runCatching { tone?.release() }
}

val LocalSoundController = staticCompositionLocalOf { SoundController() }
