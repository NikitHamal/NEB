package com.agentx.app.data.tools

import com.agentx.app.data.engine.ToolCallSpec
import javax.inject.Inject
import javax.inject.Singleton

data class ToolExecution(
    val ok: Boolean,
    val message: String,
    val needsPermission: String? = null,
    val permissionLabel: String? = null,
    val options: List<String> = emptyList(),
    val repairable: Boolean = false,
    val repairHint: String? = null
) {
    companion object {
        fun done(message: String, options: List<String> = emptyList()) =
            ToolExecution(ok = true, message = message, options = options)
        fun fail(message: String, options: List<String> = emptyList()) =
            ToolExecution(ok = false, message = message, options = options)
        fun needPermission(permission: String, label: String, message: String) =
            ToolExecution(ok = false, message = message, needsPermission = permission, permissionLabel = label)
    }
}

@Singleton
class ToolExecutor @Inject constructor(
    private val device: DeviceHandler,
    private val apps: AppHandler,
    private val comms: CommsHandler,
    private val time: TimeHandler,
    private val reminders: ReminderHandler,
    private val notes: NoteHandler,
    private val routines: RoutineHandler
) {
    suspend fun execute(spec: ToolCallSpec, background: Boolean = false): ToolExecution {
        val meta = ToolCatalog.metas[spec.name]
            ?: return ToolExecution.fail("Unknown tool " + spec.name)
        if (background && meta.backgroundBlocked) {
            return ToolExecution.fail(meta.title + " needs you in the app, so this scheduled run skips it")
        }
        return try {
            dispatch(spec, background)
        } catch (e: SecurityException) {
            ToolExecution.fail("A permission was denied: " + (e.message ?: meta.title))
        } catch (e: Exception) {
            ToolExecution.fail(e.message ?: (meta.title + " failed"))
        }
    }

    private suspend fun dispatch(spec: ToolCallSpec, background: Boolean): ToolExecution {
        return when (spec.name) {
            "set_brightness" -> device.setBrightness(spec)
            "adjust_volume" -> device.adjustVolume(spec)
            "set_screen_timeout" -> device.setScreenTimeout(spec)
            "set_auto_rotate" -> device.setAutoRotate(spec)
            "toggle_flashlight" -> device.toggleFlashlight(spec)
            "set_do_not_disturb" -> device.setDoNotDisturb(spec)
            "media_control" -> device.mediaControl(spec)
            "device_status" -> device.deviceStatus()
            "open_settings_page" -> device.openSettingsPage(spec)
            "copy_to_clipboard" -> device.copyToClipboard(spec, background)
            "share_text" -> device.shareText(spec)
            "open_app" -> apps.openApp(spec)
            "app_info" -> apps.appInfo(spec)
            "place_call" -> comms.placeCall(spec)
            "send_message" -> comms.sendMessage(spec)
            "find_contact" -> comms.findContact(spec)
            "set_alarm" -> time.setAlarm(spec)
            "set_timer" -> time.setTimer(spec)
            "create_reminder" -> reminders.create(spec)
            "list_reminders" -> reminders.list()
            "cancel_reminder" -> reminders.cancel(spec)
            "create_note" -> notes.create(spec)
            "search_notes" -> notes.search(spec)
            "create_routine" -> routines.create(spec)
            "run_routine" -> routines.run(spec, background)
            "list_routines" -> routines.list()
            else -> ToolExecution.fail("Unknown tool " + spec.name)
        }
    }
}
