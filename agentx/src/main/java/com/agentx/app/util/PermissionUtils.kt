package com.agentx.app.util

import android.Manifest
import android.app.NotificationManager
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.provider.Settings
import androidx.core.content.ContextCompat

object PermissionUtils {
    const val SPECIAL_WRITE_SETTINGS = "write_settings"
    const val SPECIAL_DND_ACCESS = "dnd_access"
    const val SPECIAL_EXACT_ALARM = "exact_alarm"

    fun has(context: Context, permission: String): Boolean =
        ContextCompat.checkSelfPermission(context, permission) == PackageManager.PERMISSION_GRANTED

    fun canWriteSettings(context: Context): Boolean = Settings.System.canWrite(context)

    fun hasDndAccess(context: Context): Boolean {
        val manager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        return manager.isNotificationPolicyAccessGranted
    }

    fun canScheduleExact(context: Context): Boolean {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.S) return true
        val manager = context.getSystemService(Context.ALARM_SERVICE) as android.app.AlarmManager
        return manager.canScheduleExactAlarms()
    }

    fun openAppSettings(context: Context) {
        val intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS).apply {
            data = Uri.fromParts("package", context.packageName, null)
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        context.startActivity(intent)
    }

    fun openWriteSettings(context: Context) {
        val intent = Intent(Settings.ACTION_MANAGE_WRITE_SETTINGS).apply {
            data = Uri.fromParts("package", context.packageName, null)
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        runCatching { context.startActivity(intent) }
    }

    fun openDndSettings(context: Context) {
        val intent = Intent(Settings.ACTION_NOTIFICATION_POLICY_ACCESS_SETTINGS).apply {
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        runCatching { context.startActivity(intent) }
    }

    fun openExactAlarmSettings(context: Context) {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.S) return
        val intent = Intent(Settings.ACTION_REQUEST_SCHEDULE_EXACT_ALARM).apply {
            data = Uri.fromParts("package", context.packageName, null)
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        runCatching { context.startActivity(intent) }
    }

    fun labelFor(permission: String): String = when (permission) {
        Manifest.permission.CALL_PHONE -> "Phone calls"
        Manifest.permission.SEND_SMS -> "SMS messages"
        Manifest.permission.READ_CONTACTS -> "Contacts"
        Manifest.permission.CAMERA -> "Camera (flashlight)"
        Manifest.permission.POST_NOTIFICATIONS -> "Notifications"
        SPECIAL_WRITE_SETTINGS -> "Modify system settings"
        SPECIAL_DND_ACCESS -> "Do Not Disturb access"
        SPECIAL_EXACT_ALARM -> "Exact alarms"
        else -> permission
    }
}
