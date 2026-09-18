package com.agentx.app.data.tools

import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonObjectBuilder
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.buildJsonObject

internal fun JsonObjectBuilder.put(key: String, value: String) = put(key, JsonPrimitive(value))

data class ToolMeta(
    val name: String,
    val title: String,
    val description: String,
    val group: String,
    val permissionLabel: String? = null,
    val confirmAlways: Boolean = false,
    val backgroundBlocked: Boolean = false
)

object ToolCatalog {

    private fun str(desc: String): JsonObject = buildJsonObject {
        put("type", "string")
        put("description", desc)
    }

    private fun enumStr(desc: String, vararg options: String): JsonObject = buildJsonObject {
        put("type", "string")
        put("description", desc)
        put("enum", JsonArray(options.map { JsonPrimitive(it) }))
    }

    private fun intArg(desc: String): JsonObject = buildJsonObject {
        put("type", "integer")
        put("description", desc)
    }

    private fun boolArg(desc: String): JsonObject = buildJsonObject {
        put("type", "boolean")
        put("description", desc)
    }

    private fun tool(
        name: String,
        desc: String,
        properties: Map<String, JsonElement>,
        required: List<String>,
        triggers: List<String> = emptyList()
    ): JsonObject = buildJsonObject {
        put("name", name)
        put("description", desc)
        put("parameters", buildJsonObject {
            put("type", "object")
            put("properties", JsonObject(properties))
            put("required", JsonArray(required.map { JsonPrimitive(it) }))
        })
        if (triggers.isNotEmpty()) {
            put("triggers", JsonArray(triggers.map { JsonPrimitive(it) }))
        }
    }

    private val stepsSchema: JsonObject = buildJsonObject {
        put("type", "array")
        put("description", "Ordered steps. Each step names a tool from this catalog plus its arguments.")
        put("items", buildJsonObject {
            put("type", "object")
            put("properties", buildJsonObject {
                put("tool", str("Tool name, exactly as listed in this catalog"))
                put("args", buildJsonObject {
                    put("type", "object")
                    put("description", "Arguments for the tool")
                })
            })
            put("required", JsonArray(listOf(JsonPrimitive("tool"))))
        })
    }

    val tools: List<JsonObject> = listOf(
        tool(
            "set_brightness",
            "Set the screen brightness from 0 (darkest) to 100 (brightest). Use for dim/brighten requests.",
            mapOf("level" to intArg("Brightness level 0-100")),
            listOf("level"),
            listOf("\\bbright", "\\bdim\\b", "screen\\s+(light|dark)")
        ),
        tool(
            "adjust_volume",
            "Change a volume stream. action set needs level 0-100; up/down step it; mute/unmute toggle it.",
            mapOf(
                "stream" to enumStr("Which volume stream", "media", "ring", "alarm"),
                "action" to enumStr("What to do", "set", "up", "down", "mute", "unmute"),
                "level" to intArg("Volume level 0-100, required when action is set")
            ),
            listOf("stream", "action"),
            listOf("\\bvolume\\b", "\\blouder\\b", "\\bquieter\\b", "\\bmute\\b", "\\bsilent\\b")
        ),
        tool(
            "set_screen_timeout",
            "How long of inactivity before the screen turns off, in seconds. Common values: 15, 30, 60, 120, 300, 600, 1800.",
            mapOf("seconds" to intArg("Timeout in seconds")),
            listOf("seconds")
        ),
        tool(
            "set_auto_rotate",
            "Turn automatic screen rotation on or off.",
            mapOf("on" to boolArg("true to enable auto-rotate, false to lock orientation")),
            listOf("on")
        ),
        tool(
            "toggle_flashlight",
            "Turn the camera flashlight torch on or off.",
            mapOf("on" to boolArg("true for on, false for off")),
            listOf("on"),
            listOf("\\bflashlight\\b", "\\btorch\\b", "\\bflash\\s+light\\b")
        ),
        tool(
            "set_do_not_disturb",
            "Turn Do Not Disturb mode on or off to silence calls and notifications.",
            mapOf("on" to boolArg("true to enable, false to disable")),
            listOf("on"),
            listOf("do\\s+not\\s+disturb", "\\bdnd\\b", "silence\\s+(calls|notifications|phone)")
        ),
        tool(
            "media_control",
            "Control whatever media is playing: play, pause, toggle play/pause, or skip next/previous track.",
            mapOf("action" to enumStr("Media key to send", "play", "pause", "toggle", "next", "previous")),
            listOf("action"),
            listOf("\\bpause\\b.*\\bmusic\\b", "\\bplay\\b.*\\bmusic\\b", "\\bnext\\s+(song|track)\\b", "\\bskip\\b.*\\bsong\\b")
        ),
        tool(
            "open_app",
            "Open an installed app by its display name, for example Camera, Clock, Gallery, Messages, YouTube. Use a short plain name.",
            mapOf("name" to str("App display name, e.g. Camera")),
            listOf("name"),
            listOf("\\bopen\\b", "\\blaunch\\b", "\\bstart\\b")
        ),
        tool(
            "app_info",
            "Open the system App info page for an installed app.",
            mapOf("name" to str("App display name")),
            listOf("name")
        ),
        tool(
            "place_call",
            "Place a phone call to a contact name or a phone number. Prefer a contact name when the user says one.",
            mapOf("target" to str("Contact name or phone number")),
            listOf("target"),
            listOf("\\bcall\\b", "\\bphone\\b", "\\bring\\b", "\\bdial\\b")
        ),
        tool(
            "send_message",
            "Send an SMS text message to a contact name or phone number. text is the full message body.",
            mapOf(
                "target" to str("Contact name or phone number"),
                "text" to str("Full message body to send")
            ),
            listOf("target", "text"),
            listOf("\\btext\\b", "\\bsms\\b", "\\bmessage\\b.*\\b(send|to)\\b", "\\bsend\\b.*\\b(message|text)\\b")
        ),
        tool(
            "find_contact",
            "Look up contacts by name and return their names and phone numbers. Use before calling or texting when unsure.",
            mapOf("name" to str("Name or partial name to search")),
            listOf("name")
        ),
        tool(
            "set_alarm",
            "Set a clock alarm at a 24-hour time. Convert am/pm to 24 hours (7pm is 19). days is optional comma names like mon,tue.",
            mapOf(
                "hour" to intArg("Hour 0-23"),
                "minute" to intArg("Minute 0-59"),
                "label" to str("Optional alarm label"),
                "days" to str("Optional comma-separated weekday names, e.g. mon,tue,wed")
            ),
            listOf("hour", "minute"),
            listOf("\\balarm\\b", "\\bwake\\s+me\\b")
        ),
        tool(
            "set_timer",
            "Start a countdown timer. Convert the duration to seconds: minutes times 60, hours times 3600.",
            mapOf(
                "seconds" to intArg("Timer length in seconds"),
                "label" to str("Optional timer label")
            ),
            listOf("seconds"),
            listOf("\\btimer\\b", "\\bcountdown\\b")
        ),
        tool(
            "create_reminder",
            "Save a reminder that fires a notification at the given time. trigger_at must be YYYY-MM-DD HH:MM in 24-hour time.",
            mapOf(
                "title" to str("Short reminder title"),
                "trigger_at" to str("Fire time as YYYY-MM-DD HH:MM, 24-hour"),
                "note" to str("Optional extra detail")
            ),
            listOf("title", "trigger_at"),
            listOf("\\bremind\\b", "\\breminder\\b")
        ),
        tool(
            "list_reminders",
            "List saved reminders, soonest first.",
            emptyMap(),
            emptyList()
        ),
        tool(
            "cancel_reminder",
            "Delete a saved reminder by its numeric id from list_reminders.",
            mapOf("id" to intArg("Reminder id number")),
            listOf("id")
        ),
        tool(
            "create_note",
            "Save a note on the device. Use when the user wants to remember, jot down, or store a piece of text.",
            mapOf(
                "body" to str("The note text"),
                "title" to str("Optional short title")
            ),
            listOf("body"),
            listOf("\\bnote\\b.*\\b(save|take|write|remember|jot)\\b", "\\bremember\\b.*\\bthat\\b")
        ),
        tool(
            "search_notes",
            "Search saved notes by keywords, for example an invoice number, a name, or a topic.",
            mapOf("query" to str("Keywords to search for")),
            listOf("query")
        ),
        tool(
            "create_routine",
            "Save a named routine: an ordered list of tool calls from this catalog that run together later. Keep steps small and concrete.",
            mapOf(
                "name" to str("Routine name, e.g. Bedtime"),
                "steps" to stepsSchema
            ),
            listOf("name", "steps"),
            listOf("\\broutine\\b", "\\bmacro\\b", "\\bevery\\s+(morning|night|day)\\b")
        ),
        tool(
            "run_routine",
            "Run a saved routine by name right now.",
            mapOf("name" to str("Routine name")),
            listOf("name")
        ),
        tool(
            "list_routines",
            "List saved routines and their steps.",
            emptyMap(),
            emptyList()
        ),
        tool(
            "device_status",
            "Read current device state: battery, volumes, brightness, do-not-disturb, wifi, bluetooth, storage.",
            emptyMap(),
            emptyList(),
            listOf("\\bbattery\\b", "\\bdevice\\s+status\\b", "\\bhow\\s+much\\s+battery\\b")
        ),
        tool(
            "open_settings_page",
            "Open a system settings page the app cannot change directly.",
            mapOf("page" to enumStr("Which settings page", "wifi", "bluetooth", "display", "sound", "battery", "apps", "notifications", "location", "storage", "about")),
            listOf("page")
        ),
        tool(
            "copy_to_clipboard",
            "Copy text to the clipboard.",
            mapOf("text" to str("Text to copy")),
            listOf("text")
        ),
        tool(
            "share_text",
            "Open the share sheet for a piece of text.",
            mapOf("text" to str("Text to share")),
            listOf("text")
        )
    )

    fun buildJson(): String = "[" + tools.joinToString(",") { it.toString() } + "]"

    val metas: Map<String, ToolMeta> = mapOf(
        "set_brightness" to ToolMeta("set_brightness", "Brightness", "Set screen brightness 0-100", "Display and sound", "Modify system settings"),
        "adjust_volume" to ToolMeta("adjust_volume", "Volume", "Media, ring and alarm volume", "Display and sound", null),
        "set_screen_timeout" to ToolMeta("set_screen_timeout", "Screen timeout", "Inactivity delay before screen off", "Display and sound", "Modify system settings"),
        "set_auto_rotate" to ToolMeta("set_auto_rotate", "Auto-rotate", "Lock or free screen orientation", "Display and sound", "Modify system settings"),
        "toggle_flashlight" to ToolMeta("toggle_flashlight", "Flashlight", "Camera torch on or off", "Display and sound", "Camera"),
        "set_do_not_disturb" to ToolMeta("set_do_not_disturb", "Do Not Disturb", "Silence calls and notifications", "Display and sound", "Do Not Disturb access"),
        "media_control" to ToolMeta("media_control", "Media keys", "Play, pause and skip tracks", "Display and sound", null),
        "open_app" to ToolMeta("open_app", "Open app", "Launch an installed app by name", "Apps", null),
        "app_info" to ToolMeta("app_info", "App info", "Open an app system page", "Apps", null),
        "place_call" to ToolMeta("place_call", "Phone call", "Call a contact or number", "Calls and messages", "Phone + Contacts", confirmAlways = true, backgroundBlocked = true),
        "send_message" to ToolMeta("send_message", "Text message", "Send an SMS", "Calls and messages", "SMS + Contacts", confirmAlways = true, backgroundBlocked = true),
        "find_contact" to ToolMeta("find_contact", "Find contact", "Look up names and numbers", "Calls and messages", "Contacts"),
        "set_alarm" to ToolMeta("set_alarm", "Alarm", "Set a clock alarm", "Time", null),
        "set_timer" to ToolMeta("set_timer", "Timer", "Start a countdown", "Time", null),
        "create_reminder" to ToolMeta("create_reminder", "Reminder", "Notification at a set time", "Reminders and notes", "Alarms"),
        "list_reminders" to ToolMeta("list_reminders", "List reminders", "Show saved reminders", "Reminders and notes", null),
        "cancel_reminder" to ToolMeta("cancel_reminder", "Cancel reminder", "Delete by id", "Reminders and notes", null),
        "create_note" to ToolMeta("create_note", "Save note", "Store text on device", "Reminders and notes", null),
        "search_notes" to ToolMeta("search_notes", "Search notes", "Keyword plus semantic search", "Reminders and notes", null),
        "create_routine" to ToolMeta("create_routine", "New routine", "Save a multi-step macro", "Routines", null),
        "run_routine" to ToolMeta("run_routine", "Run routine", "Execute a saved macro now", "Routines", null),
        "list_routines" to ToolMeta("list_routines", "List routines", "Show saved macros", "Routines", null),
        "device_status" to ToolMeta("device_status", "Device status", "Battery, volumes, radios", "System", null),
        "open_settings_page" to ToolMeta("open_settings_page", "Settings page", "Open system settings", "System", null),
        "copy_to_clipboard" to ToolMeta("copy_to_clipboard", "Copy", "Copy text to clipboard", "System", null),
        "share_text" to ToolMeta("share_text", "Share", "Open the share sheet", "System", null)
    )

    val groups: List<String> = listOf(
        "Display and sound", "Apps", "Calls and messages", "Time",
        "Reminders and notes", "Routines", "System"
    )
}
