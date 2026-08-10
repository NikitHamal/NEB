package com.neb.ians.util

import android.content.Context
import android.content.Intent
import android.os.Process
import com.neb.ians.ui.crash.CrashActivity
import java.io.PrintWriter
import java.io.StringWriter
import kotlin.system.exitProcess

class CrashHandler private constructor(private val context: Context) : Thread.UncaughtExceptionHandler {

    private val defaultHandler = Thread.getDefaultUncaughtExceptionHandler()

    override fun uncaughtException(thread: Thread, throwable: Throwable) {
        runCatching {
            val stackTrace = getStackTraceString(throwable)
            val prefs = context.getSharedPreferences("nebians_crash_logs", Context.MODE_PRIVATE)
            prefs.edit()
                .putString("last_crash_log", stackTrace)
                .putString("last_crash_type", throwable.javaClass.simpleName)
                .putString("last_crash_message", throwable.localizedMessage ?: "Unknown error")
                .putLong("last_crash_timestamp", System.currentTimeMillis())
                .apply()

            val intent = Intent(context, CrashActivity::class.java).apply {
                putExtra("crash_log", stackTrace)
                putExtra("crash_type", throwable.javaClass.simpleName)
                putExtra("crash_message", throwable.localizedMessage ?: "Unknown error")
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK)
            }
            context.startActivity(intent)
        }

        defaultHandler?.uncaughtException(thread, throwable)
        Process.killProcess(Process.myPid())
        exitProcess(10)
    }

    private fun getStackTraceString(throwable: Throwable): String {
        val sw = StringWriter()
        val pw = PrintWriter(sw)
        throwable.printStackTrace(pw)
        return sw.toString()
    }

    companion object {
        fun init(context: Context) {
            val handler = CrashHandler(context.applicationContext)
            Thread.setDefaultUncaughtExceptionHandler(handler)
        }
    }
}
