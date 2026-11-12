package com.neb.ians.ui.components

import android.content.Context
import android.widget.Toast
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.navigationBars
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.material3.SnackbarDuration
import androidx.compose.material3.SnackbarHostState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.launch

/**
 * One way to say something short from anywhere (a screen, a click handler, a download callback) without a
 * scaffold of your own. [nebToast] sends the message to the host [NebToastBusHost] draws over the whole app, so it is
 * the same card as every other toast. With no host on screen (a crash screen, a background callback while the app is
 * away) it falls back to the system toast, so a message is never lost.
 */
object NebToastBus {
    internal class Message(val text: String, val long: Boolean)

    internal val messages = MutableSharedFlow<Message>(extraBufferCapacity = 8)

    fun show(context: Context, text: String, long: Boolean = false) {
        if (messages.subscriptionCount.value == 0 || !messages.tryEmit(Message(text, long))) {
            Toast.makeText(context.applicationContext, text, if (long) Toast.LENGTH_LONG else Toast.LENGTH_SHORT).show()
        }
    }
}

/** Short message, drawn as [NebToast]. Safe to call from any thread. */
fun Context.nebToast(text: String, long: Boolean = false) {
    val ctx = this
    if (android.os.Looper.myLooper() == android.os.Looper.getMainLooper()) {
        NebToastBus.show(ctx, text, long)
    } else {
        android.os.Handler(android.os.Looper.getMainLooper()).post { NebToastBus.show(ctx, text, long) }
    }
}

/** The app-wide host: place once, over the navigation host. Keeps clear of the navigation bar. */
@Composable
fun BoxScope.NebToastBusHost() {
    val state = remember { SnackbarHostState() }
    LaunchedEffect(Unit) {
        NebToastBus.messages.collect { m ->
            state.currentSnackbarData?.dismiss()
            launch {
                state.showSnackbar(
                    message = m.text,
                    duration = if (m.long) SnackbarDuration.Long else SnackbarDuration.Short
                )
            }
        }
    }
    Box(Modifier.align(Alignment.BottomCenter).windowInsetsPadding(WindowInsets.navigationBars)) {
        NebToastHost(state)
    }
}
