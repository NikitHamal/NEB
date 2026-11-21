package com.neb.ians.data.api

import android.content.Context
import android.os.Build
import com.neb.ians.BuildConfig
import okhttp3.Interceptor
import okhttp3.Response
import java.util.Locale
import java.util.TimeZone

/**
 * Adds one `X-Neb-Device` header to every request to our own backend.
 *
 * It carries the coarse device facts the server needs to say which kind of device an
 * account, a post view or an interaction came from. The server seals the precise
 * parts, keeps no user id next to them, and never returns them to any client.
 * Nothing here is an advertising id or a hardware serial.
 */
class DeviceSignalInterceptor(context: Context) : Interceptor {

    private val appCtx: Context = context.applicationContext
    private val value: String = build(appCtx)

    override fun intercept(chain: Interceptor.Chain): Response {
        val req = chain.request()
        if (req.header(HEADER) != null || !req.url.host.endsWith(HOST_SUFFIX)) {
            return chain.proceed(req)
        }
        val ts = (System.currentTimeMillis() / 1000L).toString()
        val nonce = java.lang.Long.toHexString(java.util.concurrent.ThreadLocalRandom.current().nextLong())
        val sig = sign(req.method, req.url.encodedPath, ts, nonce)
        val flags = com.neb.ians.util.AppIntegrity.flags(appCtx)
        val proof = if (flags == 0) "t=$ts;n=$nonce;s=$sig" else "t=$ts;n=$nonce;f=${Integer.toHexString(flags)};s=$sig"
        return chain.proceed(
            req.newBuilder()
                .header(HEADER, value)
                .header(PROOF_HEADER, proof)
                .build()
        )
    }

    private fun sign(method: String, path: String, ts: String, nonce: String): String {
        val payload = "$method|$path|$ts|$nonce|${BuildConfig.VERSION_CODE}"
        return com.neb.ians.speech.NativeSpeech.safeSignProof(payload) ?: "0"
    }

    private fun build(ctx: Context): String {
        val dm = ctx.resources.displayMetrics
        val cfg = ctx.resources.configuration
        val tablet = cfg.smallestScreenWidthDp >= 600
        val parts = linkedMapOf(
            "v" to "1",
            "app" to BuildConfig.VERSION_NAME,
            "build" to BuildConfig.VERSION_CODE.toString(),
            "os" to "Android ${Build.VERSION.RELEASE}",
            "sdk" to Build.VERSION.SDK_INT.toString(),
            "model" to Build.MODEL,
            "brand" to Build.MANUFACTURER,
            "screen" to "${dm.widthPixels}x${dm.heightPixels}",
            "dpi" to dm.densityDpi.toString(),
            "lang" to Locale.getDefault().toLanguageTag(),
            "tz" to TimeZone.getDefault().id,
            "abi" to (Build.SUPPORTED_ABIS.firstOrNull() ?: ""),
            "tablet" to if (tablet) "1" else "0",
        )
        return parts.entries
            .filter { it.value.isNotBlank() }
            .joinToString(";") { "${it.key}=${clean(it.value)}" }
    }

    /** Header-safe ASCII; `;` and `=` would break the key/value split on the server. */
    private fun clean(raw: String): String =
        raw.replace(HEADER_CLEAN_REGEX, "").trim().take(48)

    companion object {
        private fun unxor(enc: IntArray, key: Int): String =
            String(CharArray(enc.size) { i -> (enc[i] xor ((key + i * 5) and 0xff)).toChar() })

        val HEADER: String = unxor(
            intArrayOf(0x1f, 0x61, 0x1f, 0x33, 0x39, 0x4d, 0x21, 0x0f, 0x19, 0x1d, 0x1a, 0x1b),
            0x47
        )
        val PROOF_HEADER: String = unxor(
            intArrayOf(0x01, 0x73, 0x2d, 0x0d, 0x0f, 0x5f, 0x27, 0x0e, 0xee, 0xe9, 0xed),
            0x59
        )
        private val HOST_SUFFIX: String = unxor(
            intArrayOf(0x50, 0x57, 0x53, 0x31, 0x2e, 0x2f, 0x30, 0x78, 0x38, 0x0f, 0x08, 0x44, 0x01, 0x04),
            0x33
        )
        private val HEADER_CLEAN_REGEX = Regex("[^A-Za-z0-9 ._+\\-/:,()]")
    }
}
