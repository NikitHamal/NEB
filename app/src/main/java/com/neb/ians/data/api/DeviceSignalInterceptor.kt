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

    private val value: String = build(context.applicationContext)

    override fun intercept(chain: Interceptor.Chain): Response {
        val req = chain.request()
        if (req.header(HEADER) != null || !req.url.host.endsWith("consica.com.np")) {
            return chain.proceed(req)
        }
        return chain.proceed(req.newBuilder().header(HEADER, value).build())
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
        raw.replace(Regex("[^A-Za-z0-9 ._+\\-/:,()]"), "").trim().take(48)

    companion object {
        const val HEADER = "X-Neb-Device"
    }
}
