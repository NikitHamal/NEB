package com.agentx.app.worker

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import com.agentx.app.data.tools.AxScheduler
import dagger.hilt.android.AndroidEntryPoint
import javax.inject.Inject
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch

@AndroidEntryPoint
class BootReceiver : BroadcastReceiver() {
    @Inject lateinit var scheduler: AxScheduler

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action != Intent.ACTION_BOOT_COMPLETED) return
        val pending = goAsync()
        scope.launch {
            try {
                runCatching { scheduler.rescheduleAll() }
            } finally {
                pending.finish()
            }
        }
    }
}
