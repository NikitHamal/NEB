package com.consica.code.util

import android.media.AudioManager
import android.media.ToneGenerator

/**
 * Tiny synthesized sound effects (no bundled audio assets, fully offline).
 * Tones are kept short and quiet to stay child-friendly. All playback is
 * gated by the sound setting.
 */
class SoundManager {

    enum class Effect { TAP, SUCCESS, REWARD, GENTLE_ERROR, GROW }

    @Volatile
    var enabled: Boolean = true

    private fun tone(): ToneGenerator? = try {
        ToneGenerator(AudioManager.STREAM_MUSIC, 35)
    } catch (e: Exception) {
        null
    }

    fun play(effect: Effect) {
        if (!enabled) return
        val generator = tone() ?: return
        try {
            when (effect) {
                Effect.TAP -> generator.startTone(ToneGenerator.TONE_PROP_BEEP, 40)
                Effect.SUCCESS -> generator.startTone(ToneGenerator.TONE_PROP_ACK, 120)
                Effect.REWARD -> generator.startTone(ToneGenerator.TONE_CDMA_ALERT_CALL_GUARD, 160)
                Effect.GENTLE_ERROR -> generator.startTone(ToneGenerator.TONE_PROP_NACK, 80)
                Effect.GROW -> generator.startTone(ToneGenerator.TONE_PROP_BEEP2, 90)
            }
        } catch (ignored: Exception) {
        }
        // Release shortly after the tone finishes.
        Thread {
            try {
                Thread.sleep(400)
                generator.release()
            } catch (ignored: Exception) {
            }
        }.start()
    }
}
