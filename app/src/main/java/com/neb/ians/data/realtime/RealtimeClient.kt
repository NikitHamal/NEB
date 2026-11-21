package com.neb.ians.data.realtime

import android.util.Log
import com.neb.ians.data.api.ApiRealtimeConfig
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
import kotlinx.coroutines.withContext
import kotlinx.serialization.json.JsonPrimitive
import okhttp3.Call
import okhttp3.HttpUrl.Companion.toHttpUrl
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
 * Realtime client for NEBians. Mirrors the web `realtime.js`:
 *  - hosted transport: Server-Sent Events straight to Ably with a short-lived
 *    subscribe token from GET /api/realtime/config/ (no tunnel, the server holds
 *    no socket). The old self-hosted WebSocket is used only if the server says so.
 *  - the stream is dropped while the app is stopped (Ably counts concurrent
 *    connections) and resumed with lastEvent so nothing is missed
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

    private val streamClient: OkHttpClient by lazy(LazyThreadSafetyMode.PUBLICATION) {
        OkHttpClient.Builder()
            .connectionPool(ApiService.sharedPool)
            .apply {
                if (!com.neb.ians.BuildConfig.DEBUG) {
                    proxy(java.net.Proxy.NO_PROXY)
                    connectionSpecs(listOf(okhttp3.ConnectionSpec.MODERN_TLS, okhttp3.ConnectionSpec.COMPATIBLE_TLS))
                }
            }
            .connectTimeout(10, TimeUnit.SECONDS)
            .readTimeout(0, TimeUnit.MILLISECONDS) // streaming
            .pingInterval(25, TimeUnit.SECONDS)
            .build()
    }
    private val wsClient: OkHttpClient get() = streamClient
    private val sseClient: OkHttpClient get() = streamClient

    private var webSocket: WebSocket? = null
    @Volatile private var sseCall: Call? = null
    @Volatile private var restartRequested = false
    @Volatile private var lastEventId = ""
    @Volatile private var userChannel = ""
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
        sseCall?.cancel()
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
            if (count == 0) {
                sendRaw(buildJsonObject {
                    put("action", "subscribe")
                    put("channel", channel)
                }.toString())
                requestSseRestart()
            }
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
                    requestSseRestart()
                } else {
                    subscriptions[channel] = current - 1
                }
            }
        }
    }

    private suspend fun connectLoop() {
        var shardHint: Int? = null
        while (desiredRunning) {
            val cfg = fetchConfig(shardHint)
            if (cfg == null) {
                delay(30_000)
                continue
            }
            when {
                cfg.transport == "ably-sse" && cfg.token.isNotBlank() && cfg.sseUrl.isNotBlank() -> {
                    userChannel = cfg.userChannel
                    val opened = runSse(cfg)
                    // Same Ably app while it works; the next one when it would not open (quota, outage).
                    shardHint = if (opened || cfg.shards <= 1) cfg.shard else (cfg.shard + 1) % cfg.shards
                    if (restartRequested) {
                        restartRequested = false
                        continue
                    }
                }
                cfg.wsUrl.isNotBlank() -> {
                    runWebSocket(cfg.wsUrl)
                }
                else -> {
                    delay(60_000)
                    continue
                }
            }
            if (!desiredRunning) break
            reconnectAttempt++
            val backoff = min(30_000L, 1000L shl min(reconnectAttempt, 5))
            delay(backoff)
        }
    }

    /** Channels this client may read through Ably (private user channels only for the signed-in user). */
    private fun sseChannels(cfg: ApiRealtimeConfig): List<String> {
        val wanted = synchronized(lock) { subscriptions.keys.toList() }
        val out = LinkedHashSet<String>()
        for (ch in wanted) {
            when {
                ch == "user" -> if (cfg.userChannel.isNotBlank()) out.add(cfg.userChannel)
                ch.startsWith("user.") -> if (ch == cfg.userChannel) out.add(ch)
                ch == "forum.public" || ch.startsWith("post.") || ch.startsWith("resource.") ||
                    ch.startsWith("resource_request.") -> out.add(ch)
            }
        }
        return out.toList()
    }

    private fun requestSseRestart() {
        val call = sseCall ?: return
        restartRequested = true
        call.cancel()
    }

    /** One SSE stream until it ends, the token nears expiry, or the channel set changes. */
    private suspend fun runSse(cfg: ApiRealtimeConfig): Boolean {
        val channels = sseChannels(cfg)
        if (channels.isEmpty()) {
            delay(10_000) // nothing subscribed yet: no connection, no cost
            return true
        }
        val url = try {
            cfg.sseUrl.toHttpUrl().newBuilder()
                .addQueryParameter("v", "1.2")
                .addQueryParameter("accessToken", cfg.token)
                .addQueryParameter("channels", channels.joinToString(","))
                .apply { if (lastEventId.isNotBlank()) addQueryParameter("lastEvent", lastEventId) }
                .build()
        } catch (e: Exception) {
            Log.d(TAG, "bad sse url: ${e.message}")
            return false
        }
        val call = sseClient.newCall(
            Request.Builder().url(url).header("Accept", "text/event-stream").build()
        )
        sseCall = call
        val renewAt = System.currentTimeMillis() + cfg.expiresIn * 800L
        var opened = false
        try {
            withContext(Dispatchers.IO) {
                call.execute().use { response ->
                    if (!response.isSuccessful) return@use
                    val source = response.body?.source() ?: return@use
                    _connected.value = true
                    opened = true
                    reconnectAttempt = 0
                    val data = StringBuilder()
                    var id = ""
                    while (desiredRunning && !call.isCanceled()) {
                        val line = source.readUtf8Line() ?: break
                        if (line.isEmpty()) {
                            if (data.isNotEmpty()) handleAbly(data.toString())
                            data.setLength(0)
                            if (id.isNotEmpty()) lastEventId = id
                            continue
                        }
                        when {
                            line.startsWith("data:") -> data.append(line.removePrefix("data:").trim())
                            line.startsWith("id:") -> id = line.removePrefix("id:").trim()
                        }
                        if (System.currentTimeMillis() > renewAt) break
                    }
                }
            }
        } catch (e: Exception) {
            Log.d(TAG, "sse ended: ${e.message}")
        } finally {
            _connected.value = false
            sseCall = null
        }
        return opened
    }

    /** An Ably message: {"name": event, "channel": ..., "data": "<json>"}. */
    private fun handleAbly(text: String) {
        try {
            val obj = json.parseToJsonElement(text).jsonObject
            val event = obj["name"]?.jsonPrimitive?.content ?: return
            var channel = obj["channel"]?.jsonPrimitive?.content ?: return
            if (userChannel.isNotBlank() && channel == userChannel) channel = "user"
            val raw = obj["data"]
            val data = when {
                raw is JsonPrimitive && raw.isString -> json.parseToJsonElement(raw.content)
                else -> raw
            }
            dispatchEvent(channel, event, data as? JsonObject)
        } catch (e: Exception) {
            Log.d(TAG, "sse message parse failed: ${e.message}")
        }
    }

    /** Legacy self-hosted WebSocket (only when the server publishes a ws_url). */
    private suspend fun runWebSocket(url: String) {
        run {
            val token = authRepository.getToken()
            val currentCookies = com.neb.ians.data.api.WafChallengeInterceptor.cachedCookieHeader()
            val request = Request.Builder()
                .url(url)
                .header("User-Agent", "Mozilla/5.0 (Linux; Android 11; Build/RQ3A.210705.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36")
                .apply { 
                    if (!token.isNullOrBlank()) header("Authorization", "Bearer $token")
                    if (!currentCookies.isNullOrEmpty()) header("Cookie", currentCookies)
                }
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

    private suspend fun fetchConfig(shard: Int? = null): ApiRealtimeConfig? {
        return try {
            apiService.getRealtimeConfig(shard)
        } catch (e: Exception) {
            Log.d(TAG, "realtime config fetch failed: ${e.message}")
            null
        }
    }

    companion object {
        private const val TAG = "RealtimeClient"
    }
}
