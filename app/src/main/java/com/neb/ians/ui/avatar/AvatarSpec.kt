package com.neb.ians.ui.avatar

import android.net.Uri
import com.neb.ians.ui.avatar.blobatar.BlobatarOpts
import com.neb.ians.ui.avatar.blobatar.parseBlobatarOpts

data class AvatarSpec(val seed: String, val opts: BlobatarOpts, val anim: String?)

fun parseAvatarUrl(url: String?): AvatarSpec? {
    if (url.isNullOrBlank()) return null
    val trimmed = url.trim()
    if (!trimmed.contains("/avatar/")) return null
    return try {
        val uri = Uri.parse(trimmed)
        val path = uri.path ?: return null
        val name = path.substringAfter("/avatar/").substringBefore("/").substringBefore("?")
        if (name.isBlank()) return null
        val decoded = Uri.decode(name).ifBlank { name }
        val params = mutableMapOf<String, String>()
        uri.queryParameterNames.forEach { k ->
            uri.getQueryParameter(k)?.let { v -> params[k.lowercase()] = v }
        }
        if (params.containsKey("s") && !params.containsKey("size")) params["size"] = params["s"]!!
        val opts = parseBlobatarOpts(params)
        AvatarSpec(decoded, opts, opts.anim)
    } catch (_: Exception) {
        null
    }
}

fun isAvatarUrl(url: String?): Boolean = !url.isNullOrBlank() && url.contains("/avatar/")

fun avatarSeedFromUrl(url: String?): String? = parseAvatarUrl(url)?.seed

fun avatarAnimFromUrl(url: String?): String? = parseAvatarUrl(url)?.anim
