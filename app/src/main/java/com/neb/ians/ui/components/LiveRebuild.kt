package com.neb.ians.ui.components

/** One marker pair written back in the only shape the Markdown renderer accepts. */
internal class Rebuilt(val text: String, val caret: Int)

/**
 * A pair is valid when no line of it starts or ends with a space and no line is empty. Typing a space at the end of
 * bold text, pressing Enter inside it, or deleting its last word all break that. This puts the pair back: spaces move
 * outside the markers, a pair that spans lines is closed and reopened on every line, and when the caret is left in an
 * empty run a hidden placeholder keeps the style switched on so the next letter is still bold.
 *
 * [inner] is the text between the markers, [ci] the caret inside it (or -1), [pendingOk] whether an emptied run under the
 * caret should stay armed. The result covers the markers too; its caret is relative to the start of the opener.
 */
internal fun rebuildPair(inner: String, mark: String, ci: Int, pendingOk: Boolean): Rebuilt {
    val z = LiveMarkdown.ZWSP
    val out = StringBuilder()
    var caretOut = -1
    var start = 0
    while (true) {
        var end = inner.indexOf('\n', start)
        if (end < 0) end = inner.length
        val last = end >= inner.length
        val has = ci in start..end
        val cp = if (has) inner.substring(start, ci).count { it != '\u200B' } else -1
        val clean = inner.substring(start, end).replace(z, "")
        var lead = 0
        while (lead < clean.length && clean[lead].isWhitespace()) lead++
        var trail = 0
        while (trail < clean.length - lead && clean[clean.length - 1 - trail].isWhitespace()) trail++
        val core = clean.length - lead - trail
        val segStart = out.length
        if (core == 0) {
            out.append(clean)
            if (has && pendingOk) {
                out.append(mark).append(z)
                caretOut = out.length
                out.append(mark)
            } else if (has) caretOut = segStart + cp.coerceAtMost(clean.length)
        } else {
            out.append(clean, 0, lead).append(mark)
            val coreStart = out.length
            out.append(clean, lead, lead + core).append(mark)
            val afterClose = out.length
            out.append(clean, lead + core, clean.length)
            if (has) {
                caretOut = when {
                    cp < lead -> segStart + cp
                    cp <= lead + core -> coreStart + (cp - lead)
                    cp < clean.length || !(last || pendingOk) -> afterClose + (cp - lead - core)
                    else -> {
                        // a space typed at the end of bold text: the space is plain, the next letter is bold again
                        out.append(mark).append(z)
                        val c = out.length
                        out.append(mark)
                        c
                    }
                }
            }
        }
        if (last) break
        out.append('\n')
        start = end + 1
    }
    return Rebuilt(out.toString(), caretOut)
}
