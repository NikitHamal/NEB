package com.neb.ians.util

import android.app.ActivityManager
import android.content.Context
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.platform.LocalContext

object DevicePerformance {
    @Volatile
    private var cachedIsLowEnd: Boolean? = null

    fun isLowEndDevice(context: Context): Boolean {
        cachedIsLowEnd?.let { return it }
        val am = context.getSystemService(Context.ACTIVITY_SERVICE) as? ActivityManager
        val maxMemMb = Runtime.getRuntime().maxMemory() / (1024 * 1024)
        val isLow = am?.isLowRamDevice == true || maxMemMb < 192
        cachedIsLowEnd = isLow
        return isLow
    }
}

@Composable
fun rememberIsLowEndDevice(): Boolean {
    val context = LocalContext.current
    return remember(context) {
        DevicePerformance.isLowEndDevice(context)
    }
}
