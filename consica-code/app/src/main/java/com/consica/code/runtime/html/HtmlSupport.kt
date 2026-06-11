package com.consica.code.runtime.html

/**
 * Lightweight, offline HTML helpers: tag inspection for challenge validation
 * and a safe wrapper document for the sandboxed preview WebView.
 */
object HtmlSupport {

    private val VOID_TAGS = setOf("img", "br", "hr", "input", "meta", "link", "area", "base", "col", "embed", "source", "track", "wbr")

    /** True when [source] contains a `<tag>` element, optionally with [content] inside it. */
    fun hasTag(source: String, tag: String, content: String? = null): Boolean {
        val lower = tag.lowercase()
        if (lower in VOID_TAGS) {
            return Regex("<\\s*$lower(\\s[^>]*)?/?>", RegexOption.IGNORE_CASE).containsMatchIn(source)
        }
        val regex = Regex(
            "<\\s*$lower(\\s[^>]*)?>(.*?)</\\s*$lower\\s*>",
            setOf(RegexOption.IGNORE_CASE, RegexOption.DOT_MATCHES_ALL),
        )
        val match = regex.find(source) ?: return false
        if (content == null) return true
        return match.groupValues[2].contains(content, ignoreCase = true)
    }

    /** Simple structural lint: returns unclosed/unmatched tag names (best effort). */
    fun findUnclosedTags(source: String): List<String> {
        val stack = ArrayDeque<String>()
        val problems = mutableListOf<String>()
        val tagRegex = Regex("<\\s*(/?)([a-zA-Z][a-zA-Z0-9]*)([^>]*)>")
        for (m in tagRegex.findAll(source)) {
            val closing = m.groupValues[1] == "/"
            val name = m.groupValues[2].lowercase()
            val selfClosed = m.groupValues[3].trimEnd().endsWith("/")
            if (name in VOID_TAGS || selfClosed) continue
            if (!closing) {
                stack.addLast(name)
            } else {
                if (stack.isNotEmpty() && stack.last() == name) {
                    stack.removeLast()
                } else {
                    val idx = stack.lastIndexOf(name)
                    if (idx >= 0) {
                        while (stack.size > idx) {
                            val unclosed = stack.removeLast()
                            if (unclosed != name) problems += unclosed
                        }
                    } else {
                        problems += "/$name"
                    }
                }
            }
        }
        problems += stack
        return problems.distinct()
    }

    /**
     * Wraps user HTML in a minimal safe document for the offline preview.
     * If the user already provided a full document, it is used as-is.
     * JavaScript stays disabled at the WebView level; this is presentation only.
     */
    fun wrapForPreview(source: String, darkMode: Boolean): String {
        if (source.contains("<html", ignoreCase = true)) return source
        val bg = if (darkMode) "#111511" else "#ffffff"
        val fg = if (darkMode) "#e8f5e9" else "#1a1a1a"
        return """
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
              body { font-family: sans-serif; padding: 16px; background: $bg; color: $fg; }
              img { max-width: 100%; }
            </style>
            </head>
            <body>
            $source
            </body>
            </html>
        """.trimIndent()
    }
}
