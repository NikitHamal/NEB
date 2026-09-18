package com.agentx.app.ui.screens.tools

import android.Manifest
import android.content.Context
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.agentx.app.data.engine.ToolCallSpec
import com.agentx.app.data.tools.ToolCatalog
import com.agentx.app.data.tools.ToolExecutor
import com.agentx.app.data.tools.ToolMeta
import com.agentx.app.util.PermissionUtils
import dagger.hilt.android.lifecycle.HiltViewModel
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.SharedFlow
import kotlinx.coroutines.launch

@HiltViewModel
class ToolsViewModel @Inject constructor(
    private val executor: ToolExecutor,
    @ApplicationContext private val context: Context
) : ViewModel() {

    enum class PermState { NONE, GRANTED, RUNTIME_NEEDED, SETTINGS_NEEDED }

    private val _result = MutableSharedFlow<String>(extraBufferCapacity = 1)
    val result: SharedFlow<String> = _result

    fun metasFor(group: String): List<ToolMeta> =
        ToolCatalog.metas.values.filter { it.group == group }

    fun permissionState(meta: ToolMeta): PermState {
        val key = keyFor(meta.name) ?: return PermState.NONE
        return when {
            key == PermissionUtils.SPECIAL_WRITE_SETTINGS ->
                if (PermissionUtils.canWriteSettings(context)) PermState.GRANTED else PermState.SETTINGS_NEEDED
            key == PermissionUtils.SPECIAL_DND_ACCESS ->
                if (PermissionUtils.hasDndAccess(context)) PermState.GRANTED else PermState.SETTINGS_NEEDED
            key == PermissionUtils.SPECIAL_EXACT_ALARM ->
                if (PermissionUtils.canScheduleExact(context)) PermState.GRANTED else PermState.SETTINGS_NEEDED
            PermissionUtils.has(context, key) -> PermState.GRANTED
            else -> PermState.RUNTIME_NEEDED
        }
    }

    fun keyFor(tool: String): String? = when (tool) {
        "set_brightness", "set_screen_timeout", "set_auto_rotate" -> PermissionUtils.SPECIAL_WRITE_SETTINGS
        "toggle_flashlight" -> Manifest.permission.CAMERA
        "set_do_not_disturb" -> PermissionUtils.SPECIAL_DND_ACCESS
        "place_call" -> Manifest.permission.CALL_PHONE
        "send_message" -> Manifest.permission.SEND_SMS
        "find_contact" -> Manifest.permission.READ_CONTACTS
        "create_reminder" -> PermissionUtils.SPECIAL_EXACT_ALARM
        else -> null
    }

    fun isDirect(meta: ToolMeta): Boolean =
        meta.name == "device_status" || meta.name == "list_reminders" || meta.name == "list_routines"

    fun runDirect(name: String) {
        viewModelScope.launch {
            val result = executor.execute(ToolCallSpec(name, emptyMap()))
            _result.emit(result.message)
        }
    }

    fun samplePrompt(name: String): String = when (name) {
        "set_brightness" -> "Set brightness to 40%"
        "adjust_volume" -> "Turn the media volume down"
        "set_screen_timeout" -> "Set screen timeout to 2 minutes"
        "set_auto_rotate" -> "Turn off auto-rotate"
        "toggle_flashlight" -> "Turn on the flashlight"
        "set_do_not_disturb" -> "Turn on Do Not Disturb"
        "media_control" -> "Pause the music"
        "open_app" -> "Open the clock"
        "app_info" -> "Show app info for the camera"
        "place_call" -> "Call Mom"
        "send_message" -> "Text Mom that I am on my way"
        "find_contact" -> "Find contact Mom"
        "set_alarm" -> "Set an alarm for 7 AM"
        "set_timer" -> "Set a 5 minute timer"
        "create_reminder" -> "Remind me to stretch in 30 minutes"
        "cancel_reminder" -> "Cancel reminder 1"
        "create_note" -> "Note that the gate code is 4410"
        "search_notes" -> "Search notes for gate code"
        "create_routine" -> "Make a bedtime routine that enables Do Not Disturb and dims to 10 percent"
        "run_routine" -> "Run my bedtime routine"
        "open_settings_page" -> "Open wifi settings"
        "copy_to_clipboard" -> "Copy hello world"
        "share_text" -> "Share hello world"
        else -> name
    }
}
