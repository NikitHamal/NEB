package com.neb.ians.ui.screens.canvas

import org.json.JSONArray
import org.json.JSONObject

object CanvasJsonSerializer {
    fun serializeNodes(nodes: List<CanvasNode>): String {
        val array = JSONArray()
        nodes.forEach { node ->
            val obj = JSONObject()
            obj.put("id", node.id)
            obj.put("boardId", node.boardId)
            obj.put("parentId", node.parentId ?: "")
            val connArray = JSONArray()
            node.connections.forEach { connArray.put(it) }
            obj.put("connections", connArray)
            obj.put("prompt", node.prompt)
            obj.put("title", node.title)
            obj.put("status", node.status)
            obj.put("x", node.x.toDouble())
            obj.put("y", node.y.toDouble())
            obj.put("width", node.width.toDouble())
            obj.put("kind", node.kind)
            obj.put("color", node.color)
            obj.put("webSearchEnabled", node.webSearchEnabled)
            obj.put("modelUsed", node.modelUsed)
            obj.put("createdAt", node.createdAt)
            obj.put("updatedAt", node.updatedAt)

            val contentObj = JSONObject()
            contentObj.put("title", node.content.title)
            contentObj.put("summary", node.content.summary)

            val sectionsArray = JSONArray()
            node.content.sections.forEach { sec ->
                val secObj = JSONObject()
                secObj.put("type", sec.type)
                sec.title?.let { secObj.put("title", it) }
                sec.content?.let { secObj.put("content", it) }

                sec.nodes?.let { dNodes ->
                    val dnArray = JSONArray()
                    dNodes.forEach { dn ->
                        val dnObj = JSONObject()
                        dnObj.put("id", dn.id)
                        dnObj.put("label", dn.label)
                        dnObj.put("desc", dn.desc)
                        dnArray.put(dnObj)
                    }
                    secObj.put("nodes", dnArray)
                }

                sec.headers?.let { hdrs ->
                    val hArray = JSONArray()
                    hdrs.forEach { hArray.put(it) }
                    secObj.put("headers", hArray)
                }

                sec.rows?.let { rows ->
                    val rArray = JSONArray()
                    rows.forEach { r ->
                        val rowArray = JSONArray()
                        r.forEach { rowArray.put(it) }
                        rArray.put(rowArray)
                    }
                    secObj.put("rows", rArray)
                }

                sec.cardItems?.let { cards ->
                    val cArray = JSONArray()
                    cards.forEach { c ->
                        val cObj = JSONObject()
                        cObj.put("title", c.title)
                        cObj.put("subtitle", c.subtitle)
                        cObj.put("desc", c.desc)
                        val bArray = JSONArray()
                        c.bullets.forEach { bArray.put(it) }
                        cObj.put("bullets", bArray)
                        cArray.put(cObj)
                    }
                    secObj.put("cardItems", cArray)
                }

                sec.bulletItems?.let { bullets ->
                    val bArray = JSONArray()
                    bullets.forEach { bArray.put(it) }
                    secObj.put("bulletItems", bArray)
                }

                sec.timelineItems?.let { tls ->
                    val tArray = JSONArray()
                    tls.forEach { tl ->
                        val tObj = JSONObject()
                        tObj.put("number", tl.number)
                        tObj.put("title", tl.title)
                        tObj.put("subtitle", tl.subtitle)
                        tArray.put(tObj)
                    }
                    secObj.put("timelineItems", tArray)
                }

                sectionsArray.put(secObj)
            }
            contentObj.put("sections", sectionsArray)
            obj.put("content", contentObj)

            array.put(obj)
        }
        return array.toString()
    }

    fun deserializeNodes(raw: String): List<CanvasNode> {
        val array = JSONArray(raw)
        val list = mutableListOf<CanvasNode>()
        for (i in 0 until array.length()) {
            val obj = array.getJSONObject(i)
            val parentId = obj.optString("parentId").ifBlank { null }
            val connList = mutableListOf<String>()
            val connJsonArray = obj.optJSONArray("connections")
            if (connJsonArray != null) {
                for (c in 0 until connJsonArray.length()) {
                    val targetId = connJsonArray.getString(c)
                    if (targetId.isNotBlank()) connList.add(targetId)
                }
            }
            val contentObj = obj.optJSONObject("content")

            var content = CanvasNodeContent()
            if (contentObj != null) {
                val sections = mutableListOf<CanvasSection>()
                val sectionsArray = contentObj.optJSONArray("sections")
                if (sectionsArray != null) {
                    for (j in 0 until sectionsArray.length()) {
                        val secObj = sectionsArray.getJSONObject(j)
                        val type = secObj.getString("type")
                        val title = if (secObj.has("title")) secObj.getString("title") else null
                        val textContent = if (secObj.has("content")) secObj.getString("content") else null

                        var dNodes: MutableList<DiagramNodeItem>? = null
                        val dArray = secObj.optJSONArray("nodes")
                        if (dArray != null) {
                            dNodes = mutableListOf()
                            for (k in 0 until dArray.length()) {
                                val d = dArray.getJSONObject(k)
                                dNodes.add(DiagramNodeItem(d.getString("id"), d.getString("label"), d.optString("desc", "")))
                            }
                        }

                        var headers: MutableList<String>? = null
                        val hArray = secObj.optJSONArray("headers")
                        if (hArray != null) {
                            headers = mutableListOf()
                            for (k in 0 until hArray.length()) headers.add(hArray.getString(k))
                        }

                        var rows: MutableList<List<String>>? = null
                        val rArray = secObj.optJSONArray("rows")
                        if (rArray != null) {
                            rows = mutableListOf()
                            for (k in 0 until rArray.length()) {
                                val row = rArray.getJSONArray(k)
                                val rowList = mutableListOf<String>()
                                for (l in 0 until row.length()) rowList.add(row.getString(l))
                                rows.add(rowList)
                            }
                        }

                        var cardItems: MutableList<CardRefItem>? = null
                        val cArray = secObj.optJSONArray("cardItems")
                        if (cArray != null) {
                            cardItems = mutableListOf()
                            for (k in 0 until cArray.length()) {
                                val c = cArray.getJSONObject(k)
                                val bullets = mutableListOf<String>()
                                val bArray = c.optJSONArray("bullets")
                                if (bArray != null) {
                                    for (l in 0 until bArray.length()) bullets.add(bArray.getString(l))
                                }
                                cardItems.add(CardRefItem(c.getString("title"), c.optString("subtitle", ""), bullets, c.optString("desc", "")))
                            }
                        }

                        var bulletItems: MutableList<String>? = null
                        val bArray = secObj.optJSONArray("bulletItems")
                        if (bArray != null) {
                            bulletItems = mutableListOf()
                            for (k in 0 until bArray.length()) bulletItems.add(bArray.getString(k))
                        }

                        var timelineItems: MutableList<TimelineItem>? = null
                        val tArray = secObj.optJSONArray("timelineItems")
                        if (tArray != null) {
                            timelineItems = mutableListOf()
                            for (k in 0 until tArray.length()) {
                                val tl = tArray.getJSONObject(k)
                                timelineItems.add(TimelineItem(tl.getInt("number"), tl.getString("title"), tl.optString("subtitle", "")))
                            }
                        }

                        sections.add(
                            CanvasSection(
                                type = type,
                                title = title,
                                content = textContent,
                                nodes = dNodes,
                                headers = headers,
                                rows = rows,
                                cardItems = cardItems,
                                bulletItems = bulletItems,
                                timelineItems = timelineItems
                            )
                        )
                    }
                }
                content = CanvasNodeContent(
                    title = contentObj.optString("title", ""),
                    summary = contentObj.optString("summary", ""),
                    sections = sections
                )
            }

            list.add(
                CanvasNode(
                    id = obj.getString("id"),
                    boardId = obj.optString("boardId", ""),
                    parentId = parentId,
                    connections = connList,
                    prompt = obj.optString("prompt", ""),
                    title = obj.optString("title", ""),
                    content = content,
                    status = obj.optString("status", "done"),
                    x = obj.optDouble("x", 0.0).toFloat(),
                    y = obj.optDouble("y", 0.0).toFloat(),
                    width = obj.optDouble("width", 460.0).toFloat(),
                    kind = obj.optString("kind", "topic"),
                    color = obj.optString("color", "default"),
                    webSearchEnabled = obj.optBoolean("webSearchEnabled", false),
                    modelUsed = obj.optString("modelUsed", "fast"),
                    createdAt = obj.optLong("createdAt", System.currentTimeMillis()),
                    updatedAt = obj.optLong("updatedAt", System.currentTimeMillis())
                )
            )
        }
        return list
    }
}
