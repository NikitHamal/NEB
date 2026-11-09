package com.neb.ians.ui.screens.reader.pdf

/** A rectangle in page fractions (0..1), origin top left. */
data class FRect(val l: Float, val t: Float, val r: Float, val b: Float) {
    fun contains(x: Float, y: Float) = x in l..r && y in t..b
    val w: Float get() = r - l
    val h: Float get() = b - t
}

/** A tappable area: either a place in this document ([page] >= 0, [y] the fraction to land on) or a web or mail address. */
data class PdfLink(val rect: FRect, val page: Int, val y: Float, val uri: String?)

/** One row of the document's own table of contents. */
data class OutlineItem(val title: String, val level: Int, val page: Int, val y: Float)

private data class Dest(val page: Int, val y: Float)

/** Links on page [index], resolved: named destinations looked up, page references turned into page numbers. */
internal fun PdfFile.links(index: Int): List<PdfLink> {
    val node = pages().getOrNull(index) ?: return emptyList()
    val annots = list(node.dict["Annots"]) ?: return emptyList()
    val out = ArrayList<PdfLink>()
    val g = node.geom
    for (a in annots) {
        if (out.size >= 4000) break
        val d = dict(a) ?: continue
        if (name(d["Subtype"]) != "Link") continue
        if ((resolve(d["F"]).int(0) and 2) != 0) continue  // hidden
        val r = list(d["Rect"]) ?: continue
        if (r.size < 4) continue
        val v = DoubleArray(4) { resolve(r[it]).num() }
        val xa = g.fx(v[0], v[1]); val xb = g.fx(v[2], v[3])
        val ya = g.fy(v[0], v[1]); val yb = g.fy(v[2], v[3])
        val w = g.width.coerceAtLeast(1.0); val h = g.height.coerceAtLeast(1.0)
        val rect = FRect(
            (minOf(xa, xb) / w).toFloat().coerceIn(0f, 1f), (minOf(ya, yb) / h).toFloat().coerceIn(0f, 1f),
            (maxOf(xa, xb) / w).toFloat().coerceIn(0f, 1f), (maxOf(ya, yb) / h).toFloat().coerceIn(0f, 1f)
        )
        if (rect.w <= 0f || rect.h <= 0f) continue
        var dest: Dest? = null
        var uri: String? = null
        val action = dict(d["A"])
        if (action != null) {
            when (name(action["S"])) {
                "GoTo" -> dest = destination(action["D"])
                "URI" -> uri = (resolve(action["URI"]) as? PdfString)?.text()?.trim()
                "Named" -> dest = when (name(action["N"])) {
                    "NextPage" -> Dest((index + 1).coerceAtMost(pages().size - 1), 0f)
                    "PrevPage" -> Dest((index - 1).coerceAtLeast(0), 0f)
                    "FirstPage" -> Dest(0, 0f)
                    "LastPage" -> Dest(pages().size - 1, 0f)
                    else -> null
                }
            }
        } else if (d["Dest"] != null) {
            dest = destination(d["Dest"])
        }
        if (dest != null) out.add(PdfLink(rect, dest.page, dest.y, null))
        else if (!uri.isNullOrBlank()) out.add(PdfLink(rect, -1, 0f, uri))
    }
    return out
}

/** The table of contents stored in the file, flattened in reading order. */
internal fun PdfFile.outline(): List<OutlineItem> {
    val root = dict(catalog?.get("Outlines")) ?: return emptyList()
    val out = ArrayList<OutlineItem>()
    val seen = HashSet<Any>()
    fun walk(first: Any?, level: Int) {
        var cur = first
        var guard = 0
        while (cur != null && guard++ < 5000 && out.size < 6000) {
            val key: Any = (cur as? PdfRef) ?: break
            if (!seen.add(key)) break
            val d = dict(cur) ?: break
            val title = (resolve(d["Title"]) as? PdfString)?.text()?.trim().orEmpty()
            val dest = when {
                d["Dest"] != null -> destination(d["Dest"])
                else -> dict(d["A"])?.takeIf { name(it["S"]) == "GoTo" }?.let { destination(it["D"]) }
            }
            if (title.isNotEmpty() && dest != null) out.add(OutlineItem(title, level, dest.page, dest.y))
            if (d["First"] != null && level < 8) walk(d["First"], level + 1)
            cur = d["Next"]
        }
    }
    walk(root["First"], 0)
    return out
}

private fun PdfFile.destination(x: Any?): Dest? {
    var target = resolve(x)
    var guard = 0
    while (guard++ < 4) {
        target = when (target) {
            is PdfName -> namedDestination(target.v)
            is PdfString -> namedDestination(String(target.bytes, Charsets.ISO_8859_1))
            is Map<*, *> -> resolve(target["D"])
            else -> break
        }
    }
    val arr = target as? List<*> ?: return null
    if (arr.isEmpty()) return null
    val page = when (val p = arr[0]) {
        is PdfRef -> pageIndex(p.num)
        is Int -> p
        else -> -1
    }
    if (page < 0 || page >= pages().size) return null
    val node = pages()[page]
    val mode = (resolve(arr.getOrNull(1)) as? PdfName)?.v
    val top: Double? = when (mode) {
        "XYZ" -> (resolve(arr.getOrNull(3)) as? Number)?.toDouble()
        "FitH", "FitBH" -> (resolve(arr.getOrNull(2)) as? Number)?.toDouble()
        "FitR" -> (resolve(arr.getOrNull(5)) as? Number)?.toDouble()
        else -> null
    }
    val left: Double = (resolve(arr.getOrNull(2)) as? Number)?.toDouble() ?: node.geom.x0
    val y = if (top == null) 0f else (node.geom.fy(left, top) / node.geom.height.coerceAtLeast(1.0)).toFloat().coerceIn(0f, 1f)
    return Dest(page, y)
}

private fun PdfFile.namedDestination(name: String): Any? {
    val cat = catalog ?: return null
    dict(cat["Dests"])?.let { dests -> dests[name]?.let { return resolve(it) } }
    val tree = dict(dict(cat["Names"])?.get("Dests")) ?: return null
    return searchNameTree(tree, name, 0)?.let { resolve(it) }
}

private fun PdfFile.searchNameTree(node: PdfDict, key: String, depth: Int): Any? {
    if (depth > 24) return null
    list(node["Names"])?.let { names ->
        var i = 0
        while (i + 1 < names.size) {
            val k = resolve(names[i]) as? PdfString
            if (k != null && String(k.bytes, Charsets.ISO_8859_1) == key) return names[i + 1]
            i += 2
        }
    }
    val kids = list(node["Kids"]) ?: return null
    // limits narrow the search; if they are wrong, fall back to looking in every branch
    for (pass in 0..1) {
        for (kid in kids) {
            val kd = dict(kid) ?: continue
            if (pass == 0) {
                val limits = list(kd["Limits"])
                if (limits != null && limits.size >= 2) {
                    val lo = (resolve(limits[0]) as? PdfString)?.let { String(it.bytes, Charsets.ISO_8859_1) }
                    val hi = (resolve(limits[1]) as? PdfString)?.let { String(it.bytes, Charsets.ISO_8859_1) }
                    if (lo != null && hi != null && (key < lo || key > hi)) continue
                }
            }
            searchNameTree(kd, key, depth + 1)?.let { return it }
        }
        if (kids.size <= 1) break
    }
    return null
}
