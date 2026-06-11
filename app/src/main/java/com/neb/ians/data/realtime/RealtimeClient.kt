package com.neb.ians.data.realtime

import android.util.Log
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.repository.AuthRepository
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharedFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.int
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import kotlinx.serialization.json.put
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import okhttp3.WebSocket
import okhttp3.WebSocketListener
import java.util.concurrent.TimeUnit
import javax.inject.Inject
import javax.inject.Singleton
import kotlin.math.min

/** A realtime event received over the NEBians WebSocket. */
data class RealtimeEvent(
    val channel: String,
    val event: String,
    val data: JsonObject?
)

/**
 * WebSocket client for the NEBians realtime layer (Channels/Daphne behind a
 * Cloudflare tunnel). Mirrors the web `realtime.js` behavior:
 *  - URL discovery via GET /api/realtime/config/
 *  - Bearer-token auth (Authorization header)
 *  - auto-reconnect with exponential backoff (1s -> 30s)
 *  - heartbeat ping every 25s
 *  - channel subscribe/unsubscribe with reference counting
 *  - unread notification count kept live (notification.unread_count events)
 */
@Singleton
class RealtimeClient @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private val json = Json { ignoreUnknownKeys = true }

    private val wsClient = OkHttpClient.Builder()
        .connectTimeout(10, TimeUnit.SECONDS)
        .readTimeout(0, TimeUnit.MILLISECONDS) // streaming
        .pingInterval(25, TimeUnit.SECONDS)
        .build()

    private var webSocket: WebSocket? = null
    private var connectJob: Job? = null
    private var reconnectAttempt = 0
    @Volatile private var desiredRunning = false

    private val subscriptions = mutableMapOf<String, Int>() // channel -> refcount
    private val lock = Any()

    private val _events = MutableSharedFlow<RealtimeEvent>(extraBufferCapacity = 64)
    val events: SharedFlow<RealtimeEvent> = _events.asSharedFlow()

    private val _connected = MutableStateFlow(false)
    val connected: StateFlow<Boolean> = _connected.asStateFlow()

    private val _unreadCount = MutableStateFlow(0)
    /** Live unread notification count (badge in top bar / bottom nav). */
    val unreadCount: StateFlow<Int> = _unreadCount.asStateFlow()

    /** Start (or restart) the realtime connection. Safe to call repeatedly. */
    fun start() {
        if (desiredRunning) return
        desiredRunning = true
        reconnectAttempt = 0
        connectJob?.cancel()
        connectJob = scope.launch { connectLoop() }
        // Seed the unread badge from REST so it is correct even if WS is down.
        refreshUnreadCount()
    }

    fun stop() {
        desiredRunning = false
        connectJob?.cancel()
        webSocket?.close(1000, "bye")
        webSocket = null
        _connected.value = false
    }

    /** Re-fetch unread count over REST (used as fallback / initial value). */
    fun refreshUnreadCount() {
        scope.launch {
            try {
                val bearer = authRepository.getBearerToken() ?: return@launch
                _unreadCount.value = apiService.getUnreadNotificationCount(bearer).count
            } catch (e: Exception) {
                Log.d(TAG, "unread refresh failed: ${e.message}")
            }
        }
    }

    /** Optimistically clear the badge (e.g. after mark-all-read). */
    fun setUnreadCount(count: Int) {
        _unreadCount.value = count.coerceAtLeast(0)
    }

    /** Subscribe to a channel (e.g. "forum.public", "post.<id>"). Returns an unsubscribe handle. */
    fun subscribe(channel: String): () -> Unit {
        synchronized(lock) {
            val count = subscriptions.getOrPut(channel) { 0 }
            subscriptions[channel] = count + 1
            if (count == 0) sendRaw(buildJsonObject {
                put("action", "subscribe")
                put("channel", channel)
            }.toString())
        }
        return {
            synchronized(lock) {
                val current = subscriptions[channel] ?: 0
                if (current <= 1) {
                    subscriptions.remove(channel)
                    sendRaw(buildJsonObject {
                        put("action", "unsubscribe")
                        put("channel", channel)
                    }.toString())
                } else {
                    subscriptions[channel] = current - 1
                }
            }
        }
    }

    private suspend fun connectLoop() {
        while (desiredRunning) {
            val url = resolveUrl()
            if (url.isNullOrBlank()) {
                delay(30_000)
                continue
            }
            val token = authRepository.getToken()
            val request = Request.Builder()
                .url(url)
                .apply { if (!token.isNullOrBlank()) header("Authorization", "Bearer $token") }
                .build()

            val closed = kotlinx.coroutines.CompletableDeferred<Unit>()
            val ws = wsClient.newWebSocket(request, object : WebSocketListener() {
                override fun onOpen(webSocket: WebSocket, response: Response) {
                    reconnectAttempt = 0
                    _connected.value = true
                    // Re-subscribe all active channels after reconnect.
                    synchronized(lock) {
                        subscriptions.keys.forEach { channel ->
                            webSocket.send(buildJsonObject {
                                put("action", "subscribe")
                                put("channel", channel)
                            }.toString())
                        }
                    }
                }

                override fun onMessage(webSocket: WebSocket, text: String) {
                    handleMessage(webSocket, text)
                }

                override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
                    _connected.value = false
                    closed.complete(Unit)
                }

                override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                    _connected.value = false
                    closed.complete(Unit)
                }
            })
            webSocket = ws

            closed.await()
            webSocket = null
            if (!desiredRunning) break
            reconnectAttempt++
            val backoff = min(30_000L, 1000L shl min(reconnectAttempt, 5))
            delay(backoff)
        }
    }

    private fun handleMessage(ws: WebSocket, text: String) {
        try {
            val obj = json.parseToJsonElement(text).jsonObject
            when (obj["type"]?.jsonPrimitive?.content) {
                "ping" -> ws.send("{\"action\":\"pong\"}")
                "event" -> {
                    val channel = obj["channel"]?.jsonPrimitive?.content ?: return
                    val event = obj["event"]?.jsonPrimitive?.content ?: return
                    val data = obj["data"]
                    val batched = obj["batched"]?.jsonPrimitive?.content == "true"
                    if (batched && data != null && data is kotlinx.serialization.json.JsonArray) {
                        data.forEach { item ->
                            dispatchEvent(channel, event, item as? JsonObject)
                        }
                    } else {
                        dispatchEvent(channel, event, data as? JsonObject)
                    }
                }
            }
        } catch (e: Exception) {
            Log.d(TAG, "ws message parse failed: ${e.message}")
        }
    }

    private fun dispatchEvent(channel: String, event: String, data: JsonObject?) {
        if (event == "notification.unread_count") {
            data?.get("count")?.jsonPrimitive?.let { prim ->
                try { _unreadCount.value = prim.int } catch (_: Exception) {}
            }
        }
        if (event == "notification.new") {
            _unreadCount.value = _unreadCount.value + 1
        }
        _events.tryEmit(RealtimeEvent(channel, event, data))
    }

    private fun sendRaw(text: String) {
        try {
            webSocket?.send(text)
        } catch (_: Exception) {
        }
    }

    private suspend fun resolveUrl(): String? {
        return try {
            val cfg = apiService.getRealtimeConfig()
            cfg.wsUrl.ifBlank { null }
        } catch (e: Exception) {
            Log.d(TAG, "realtime config fetch failed: ${e.message}")
            null
        }
    }

    companion object {
        private const val TAG = "RealtimeClient"
    }
}
