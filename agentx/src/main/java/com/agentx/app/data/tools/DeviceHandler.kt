package com.agentx.app.data.tools

import android.app.NotificationManager
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.hardware.camera2.CameraManager
import android.media.AudioManager
import android.os.BatteryManager
import android.os.StatFs
import android.provider.Settings
import android.view.KeyEvent
import com.agentx.app.data.engine.ToolCallSpec
import com.agentx.app.util.PermissionUtils
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class DeviceHandler @Inject constructor(
    @ApplicationContext private val context: Context
) {
    private fun audio(): AudioManager = context.getSystemService(Context.AUDIO_SERVICE) as AudioManager

    fun setBrightness(spec: ToolCallSpec): ToolExecution {
        if (!PermissionUtils.canWriteSettings(context)) {
            return ToolExecution.needPermission(
                PermissionUtils.SPECIAL_WRITE_SETTINGS,
                "Modify system settings",
                "Brightness needs the modify-settings permission first"
            )
        }
        val level = (spec.argInt("level") ?: return ToolExecution.fail("Give a brightness level 0-100")).coerceIn(0, 100)
        val resolver = context.contentResolver
        Settings.System.putInt(resolver, Settings.System.SCREEN_BRIGHTNESS_MODE, Settings.System.SCREEN_BRIGHTNESS_MODE_MANUAL)
        Settings.System.putInt(resolver, Settings.System.SCREEN_BRIGHTNESS, (level * 255 / 100).coerceIn(1, 255))
        return ToolExecution.done("Brightness set to " + level + "%")
    }

    fun adjustVolume(spec: ToolCallSpec): ToolExecution {
        val stream = when ((spec.arg("stream") ?: "media").lowercase()) {
            "media" -> AudioManager.STREAM_MUSIC
            "ring" -> AudioManager.STREAM_RING
            "alarm" -> AudioManager.STREAM_ALARM
            else -> return ToolExecution.fail("Unknown stream. Use media, ring or alarm.")
        }
        val manager = audio()
        when ((spec.arg("action") ?: "up").lowercase()) {
            "set" -> {
                val level = spec.argInt("level") ?: return ToolExecution.fail("Give a level 0-100 to set")
                val max = manager.getStreamMaxVolume(stream)
                manager.setStreamVolume(stream, (level.coerceIn(0, 100) * max / 100), AudioManager.FLAG_SHOW_UI)
            }
            "up" -> manager.adjustStreamVolume(stream, AudioManager.ADJUST_RAISE, AudioManager.FLAG_SHOW_UI)
            "down" -> manager.adjustStreamVolume(stream, AudioManager.ADJUST_LOWER, AudioManager.FLAG_SHOW_UI)
            "mute" -> manager.adjustStreamVolume(stream, AudioManager.ADJUST_MUTE, AudioManager.FLAG_SHOW_UI)
            "unmute" -> manager.adjustStreamVolume(stream, AudioManager.ADJUST_UNMUTE, AudioManager.FLAG_SHOW_UI)
            else -> return ToolExecution.fail("Unknown action. Use set, up, down, mute or unmute.")
        }
        return ToolExecution.done("Volume updated")
    }

    fun setScreenTimeout(spec: ToolCallSpec): ToolExecution {
        if (!PermissionUtils.canWriteSettings(context)) {
            return ToolExecution.needPermission(
                PermissionUtils.SPECIAL_WRITE_SETTINGS,
                "Modify system settings",
                "Screen timeout needs the modify-settings permission first"
            )
        }
        val seconds = (spec.argInt("seconds") ?: return ToolExecution.fail("Give seconds, e.g. 60")).coerceIn(5, 3600)
        Settings.System.putInt(context.contentResolver, Settings.System.SCREEN_OFF_TIMEOUT, seconds * 1000)
        return ToolExecution.done("Screen turns off after " + seconds + " seconds idle")
    }

    fun setAutoRotate(spec: ToolCallSpec): ToolExecution {
        if (!PermissionUtils.canWriteSettings(context)) {
            return ToolExecution.needPermission(
                PermissionUtils.SPECIAL_WRITE_SETTINGS,
                "Modify system settings",
                "Auto-rotate needs the modify-settings permission first"
            )
        }
        val on = spec.argBool("on") ?: return ToolExecution.fail("Say on or off")
        Settings.System.putInt(context.contentResolver, Settings.System.ACCELEROMETER_ROTATION, if (on) 1 else 0)
        return ToolExecution.done(if (on) "Auto-rotate on" else "Orientation locked")
    }

    fun toggleFlashlight(spec: ToolCallSpec): ToolExecution {
        if (!PermissionUtils.has(context, android.Manifest.permission.CAMERA)) {
            return ToolExecution.needPermission(
                android.Manifest.permission.CAMERA,
                "Camera (flashlight)",
                "Flashlight needs camera permission first"
            )
        }
        val on = spec.argBool("on") ?: return ToolExecution.fail("Say on or off")
        val manager = context.getSystemService(Context.CAMERA_SERVICE) as CameraManager
        val cameraId = manager.cameraIdList.firstOrNull { id ->
            runCatching { manager.getCameraCharacteristics(id).get(android.hardware.camera2.CameraCharacteristics.FLASH_INFO_AVAILABLE) == true }.getOrDefault(false)
        } ?: return ToolExecution.fail("This device has no flashlight")
        runCatching { manager.setTorchMode(cameraId, on) }.onFailure {
            return ToolExecution.fail("Could not reach the flashlight: " + (it.message ?: "busy"))
        }
        return ToolExecution.done(if (on) "Flashlight on" else "Flashlight off")
    }

    fun setDoNotDisturb(spec: ToolCallSpec): ToolExecution {
        if (!PermissionUtils.hasDndAccess(context)) {
            return ToolExecution.needPermission(
                PermissionUtils.SPECIAL_DND_ACCESS,
                "Do Not Disturb access",
                "Do Not Disturb needs policy access first"
            )
        }
        val on = spec.argBool("on") ?: return ToolExecution.fail("Say on or off")
        val manager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        manager.setInterruptionFilter(
            if (on) NotificationManager.INTERRUPTION_FILTER_NONE else NotificationManager.INTERRUPTION_FILTER_ALL
        )
        return ToolExecution.done(if (on) "Do Not Disturb on" else "Do Not Disturb off")
    }

    fun mediaControl(spec: ToolCallSpec): ToolExecution {
        val code = when ((spec.arg("action") ?: "toggle").lowercase()) {
            "play" -> KeyEvent.KEYCODE_MEDIA_PLAY
            "pause" -> KeyEvent.KEYCODE_MEDIA_PAUSE
            "toggle" -> KeyEvent.KEYCODE_MEDIA_PLAY_PAUSE
            "next" -> KeyEvent.KEYCODE_MEDIA_NEXT
            "previous" -> KeyEvent.KEYCODE_MEDIA_PREVIOUS
            else -> return ToolExecution.fail("Use play, pause, toggle, next or previous")
        }
        val manager = audio()
        val down = KeyEvent(KeyEvent.ACTION_DOWN, code)
        val up = KeyEvent(KeyEvent.ACTION_UP, code)
        manager.dispatchMediaKeyEvent(down)
        manager.dispatchMediaKeyEvent(up)
        return ToolExecution.done("Media key sent")
    }

    fun deviceStatus(): ToolExecution {
        val battery = context.registerReceiver(null, android.content.IntentFilter(Intent.ACTION_BATTERY_CHANGED))
        val level = battery?.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) ?: -1
        val scale = battery?.getIntExtra(BatteryManager.EXTRA_SCALE, 100) ?: 100
        val pct = if (level >= 0) (level * 100 / scale) else -1
        val charging = battery?.getIntExtra(BatteryManager.EXTRA_PLUGGED, 0) != 0
        val manager = audio()
        val mediaPct = manager.getStreamVolume(AudioManager.STREAM_MUSIC) * 100 / manager.getStreamMaxVolume(AudioManager.STREAM_MUSIC).coerceAtLeast(1)
        val ringMode = when (manager.ringerMode) {
            AudioManager.RINGER_MODE_SILENT -> "silent"
            AudioManager.RINGER_MODE_VIBRATE -> "vibrate"
            else -> "normal"
        }
        val brightness = runCatching {
            Settings.System.getInt(context.contentResolver, Settings.System.SCREEN_BRIGHTNESS) * 100 / 255
        }.getOrDefault(-1)
        val dnd = (context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager)
            .currentInterruptionFilter != NotificationManager.INTERRUPTION_FILTER_ALL
        val net = (context.getSystemService(Context.CONNECTIVITY_SERVICE) as android.net.ConnectivityManager)
        val online = net.activeNetwork != null
        val free = StatFs(context.dataDir.absolutePath).availableBytes / (1024 * 1024)
        val lines = StringBuilder()
        lines.appendLine("Battery: " + (if (pct >= 0) pct.toString() + "%" else "unknown") + if (charging) " (charging)" else "")
        lines.appendLine("Media volume: " + mediaPct + "%, ringer: " + ringMode)
        if (brightness >= 0) lines.appendLine("Brightness: " + brightness + "%")
        lines.appendLine("Do Not Disturb: " + if (dnd) "on" else "off")
        lines.appendLine("Network: " + if (online) "connected" else "offline")
        lines.appendLine("Free storage: " + free + " MB")
        lines.append("Model: " + android.os.Build.MANUFACTURER + " " + android.os.Build.MODEL)
        return ToolExecution.done(lines.toString())
    }

    fun openSettingsPage(spec: ToolCallSpec): ToolExecution {
        val action = when ((spec.arg("page") ?: "").lowercase()) {
            "wifi" -> Settings.Panel.ACTION_INTERNET_CONNECTIVITY
            "bluetooth" -> Settings.ACTION_BLUETOOTH_SETTINGS
            "display" -> Settings.ACTION_DISPLAY_SETTINGS
            "sound" -> Settings.ACTION_SOUND_SETTINGS
            "battery" -> Settings.ACTION_BATTERY_SAVER_SETTINGS
            "apps" -> Settings.ACTION_APPLICATION_SETTINGS
            "notifications" -> Settings.ACTION_APP_NOTIFICATION_SETTINGS
            "location" -> Settings.ACTION_LOCATION_SOURCE_SETTINGS
            "storage" -> Settings.ACTION_INTERNAL_STORAGE_SETTINGS
            "about" -> Settings.ACTION_DEVICE_INFO_SETTINGS
            else -> return ToolExecution.fail("Unknown page. Use wifi, bluetooth, display, sound, battery, apps, notifications, location, storage or about.")
        }
        val intent = Intent(action).apply { addFlags(Intent.FLAG_ACTIVITY_NEW_TASK) }
        if (action == Settings.ACTION_APP_NOTIFICATION_SETTINGS) {
            intent.putExtra(Settings.EXTRA_APP_PACKAGE, context.packageName)
        }
        runCatching { context.startActivity(intent) }.onFailure {
            return ToolExecution.fail("Could not open settings")
        }
        return ToolExecution.done("Settings opened")
    }

    fun copyToClipboard(spec: ToolCallSpec, background: Boolean): ToolExecution {
        if (background) return ToolExecution.fail("Clipboard needs the app open, so this scheduled run skips it")
        val text = spec.arg("text") ?: return ToolExecution.fail("Nothing to copy")
        val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        clipboard.setPrimaryClip(ClipData.newPlainText("AgentX", text))
        return ToolExecution.done("Copied to clipboard")
    }

    fun shareText(spec: ToolCallSpec): ToolExecution {
        val text = spec.arg("text") ?: return ToolExecution.fail("Nothing to share")
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_TEXT, text)
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        val chooser = Intent.createChooser(intent, "Share").apply { addFlags(Intent.FLAG_ACTIVITY_NEW_TASK) }
        runCatching { context.startActivity(chooser) }.onFailure {
            return ToolExecution.fail("Could not open the share sheet")
        }
        return ToolExecution.done("Share sheet opened")
    }
}
