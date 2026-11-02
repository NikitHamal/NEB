---
subject: Mobile Programming
grade: BCA Semester 6
unit: 5
title: Networking, JSON and Background Work
hours: 7
area: BCA 352 · Mobile Programming · Unit 5
---

Most useful apps talk to a server: a wallet checks a balance, a news app loads headlines, a school app syncs attendance. Mobile networks are slow, expensive and unreliable, and the main thread must never wait for them. This unit covers HTTP and REST from the app's viewpoint, parsing JSON (executed on a sample), keeping the UI responsive with threads and coroutines, **retrying with exponential backoff** (computed), and scheduling work that must survive the app being closed with WorkManager.

::: key What this unit gives you
- HTTP methods and status codes, REST conventions, HTTPS and certificate trust.
- JSON parsing and object mapping; the Retrofit/OkHttp stack (not executed).
- Threads, coroutines and the main-thread rule; ViewModel + repository pattern for loading states.
- Retry/backoff, caching, and WorkManager for reliable background work; battery-friendly design.
:::

## 5.1 HTTP and REST in brief

The app sends an HTTP **request** (method, URL, headers, optional body) and receives a **response** (status code, headers, body).

| Method | Meaning | Example |
|---|---|---|
| GET | Read a resource | `GET /api/notes?page=2` |
| POST | Create | `POST /api/notes` with a JSON body |
| PUT / PATCH | Replace / partially update | `PATCH /api/notes/42` |
| DELETE | Remove | `DELETE /api/notes/42` |

Status codes: **2xx** success (200 OK, 201 Created), **3xx** redirect, **4xx** client error (400 bad request, 401 unauthorised, 403 forbidden, 404 not found, 429 too many requests), **5xx** server error (500, 503). A **REST** API models *resources* as URLs and uses the methods above and JSON bodies. Always use **HTTPS**: it encrypts the traffic and authenticates the server with a certificate, and modern Android blocks plain HTTP by default (cleartext traffic). Authentication uses tokens sent in an `Authorization: Bearer ...` header; tokens are stored encrypted and refreshed when they expire. Set **timeouts** (connect, read) so that a dead connection does not hang the app.

## 5.2 JSON

**JSON** is the standard data format: objects `{"key": value}`, arrays `[...]`, strings, numbers, booleans and null. An app parses the text into objects, either by hand (`org.json.JSONObject`) or by mapping into data classes (**Moshi**, **Gson**, **kotlinx.serialization**). The following executed program parses a sample response and totals the order; it reads the bytes first so the payload size is visible, which matters on prepaid data.

```python
import json
payload = '{"status":"ok","items":[{"id":1,"name":"Dal","price":180,"qty":2},{"id":2,"name":"Rice","price":95,"qty":10},{"id":3,"name":"Oil","price":260,"qty":1}]}'
data = json.loads(payload)
total = sum(i["price"] * i["qty"] for i in data["items"])
print(len(data["items"]), "items, total Rs", total)
print(len(payload.encode()), "bytes of JSON")
```
```output
3 items, total Rs 1570
152 bytes of JSON
```
Never assume the structure: fields can be missing or null, numbers can arrive as strings, and the list can be empty. Mapping libraries need **default values** and nullable types, and unknown fields should be ignored so that a server upgrade does not break old app versions. For large payloads use **pagination** (`?page=2&size=20`), request only needed fields, and enable **gzip** compression (OkHttp does this transparently).

Not executed (needs the Android SDK, Retrofit and Moshi): a typed API client.

```kotlin
data class Item(val id: Int, val name: String, val price: Int, val qty: Int)
data class OrderResponse(val status: String, val items: List<Item>)

interface ShopApi {
    @GET("orders/{id}")
    suspend fun order(@Path("id") id: Int): OrderResponse
}
val api = Retrofit.Builder().baseUrl("https://api.example.np/")
    .addConverterFactory(MoshiConverterFactory.create()).build()
    .create(ShopApi::class.java)
```

## 5.3 Keeping the main thread free

The main thread draws the UI and must stay free (Unit 3). Network access on it is forbidden: Android throws `NetworkOnMainThreadException`. Options for background work, from old to new: `Thread` and `AsyncTask` (deprecated), `Executor`s and `Handler`s, RxJava, and today **Kotlin coroutines**. A coroutine is a lightweight suspendable computation: `suspend` functions pause without blocking a thread, and the *dispatcher* decides where code runs (`Dispatchers.Main` for UI, `Dispatchers.IO` for network and disk, `Dispatchers.Default` for CPU work). A **ViewModel** launches coroutines in `viewModelScope`, which is cancelled automatically when the screen is gone.

Not executed (needs the Android SDK): a ViewModel exposing loading, success and error states.

```kotlin
sealed interface UiState {
    object Loading : UiState
    data class Ok(val items: List<Item>) : UiState
    data class Error(val message: String) : UiState
}
class OrderViewModel(private val api: ShopApi) : ViewModel() {
    private val _state = MutableStateFlow<UiState>(UiState.Loading)
    val state: StateFlow<UiState> = _state
    fun load(id: Int) = viewModelScope.launch {
        _state.value = UiState.Loading
        _state.value = try {
            UiState.Ok(withContext(Dispatchers.IO) { api.order(id).items })
        } catch (e: IOException) {
            UiState.Error("No connection")
        }
    }
}
```

The screen *observes* the state and shows a spinner, the list or a retry button. Always model the three outcomes: users meet "Error" and "Loading" more often than developers expect.

## 5.4 Retry and backoff

Transient failures (a dropped connection, a 503) are common on mobile networks, but retrying immediately, in a tight loop, wastes battery and overloads the server. **Exponential backoff** waits longer after each failure: delay = min(cap, base × 2^attempt), often with random **jitter** so that thousands of phones do not retry in step. With base 1 s and cap 30 s:

```python
def backoff(attempt, base=1, cap=30):
    return min(cap, base * 2 ** attempt)

delays = [backoff(a) for a in range(7)]
print(delays)
print("total wait for 7 tries:", sum(delays), "seconds")
```
```output
[1, 2, 4, 8, 16, 30, 30]
total wait for 7 tries: 91 seconds
```
Retry only **idempotent** operations (GET, or a POST that carries an idempotency key) and only for transient errors (timeouts, 5xx, 429), never for 4xx errors such as 401 or 404. Cache responses (HTTP cache headers with OkHttp, or the Room copy) so that the app shows the last known data offline and refreshes in the background: the "offline-first" design suits Nepal's connectivity.

## 5.5 Background work that must finish

Work the user expects to complete even if they leave the app (uploading a photo, syncing attendance) cannot rely on a thread, because the process can die. **WorkManager** persists the work request and runs it when its **constraints** are met, retrying with backoff if it fails. Not executed (needs the Android SDK):

```kotlin
class SyncWorker(ctx: Context, p: WorkerParameters) : CoroutineWorker(ctx, p) {
    override suspend fun doWork(): Result =
        try { repository.sync(); Result.success() } catch (e: IOException) { Result.retry() }
}
val request = OneTimeWorkRequestBuilder<SyncWorker>()
    .setConstraints(Constraints.Builder()
        .setRequiredNetworkType(NetworkType.UNMETERED)
        .setRequiresBatteryNotLow(true).build())
    .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 30, TimeUnit.SECONDS)
    .build()
WorkManager.getInstance(context).enqueue(request)
```

Use `PeriodicWorkRequest` for recurring sync (minimum interval 15 minutes), a **foreground service** with a notification for user-visible long tasks such as navigation or a download, and exact **alarms** only for things like a calendar reminder. **Doze mode** and **App Standby** defer background activity when the phone is idle, so design for *eventual* execution. Battery-friendly rules: batch requests, prefer push notifications (Firebase Cloud Messaging) to polling, avoid wake locks, and let the user choose "sync on Wi-Fi only", which also saves their prepaid data.

## Chapter summary

- HTTP methods, status codes and REST resources; use HTTPS, tokens and timeouts.
- JSON is parsed into objects defensively (missing fields, pagination, compression); the sample parse gave 3 items totalling Rs 1570.
- Network and disk run off the main thread: coroutines with ViewModel and a Loading/Ok/Error state.
- Retry only transient, idempotent failures with exponential backoff (1, 2, 4, 8, 16, 30, 30 seconds).
- WorkManager runs deferrable work reliably under constraints; respect Doze and battery.

## Practice

1. Match each to a method: create a note, read notes, delete a note.
2. What do status codes 401, 404, 429 and 503 mean, and which of them might be retried?
3. Why must networking not run on the main thread?
4. Parse `{"items":[{"p":50,"q":2},{"p":30,"q":3}]}` and compute the total of p × q.
5. What are the three UI states a loading screen should model?
6. Compute the backoff delays for base 2 s, cap 20 s, five attempts.
7. What is an idempotent request and why does it matter for retries?
8. Why use WorkManager rather than a plain thread for uploading a photo?
9. Name three ways to reduce an app's battery and data use.
10. Why is offline-first design suitable for Nepal?

::: note Answers and worked solutions
**1.** POST (create), GET (read), DELETE (remove).
**2.** 401 unauthorised (refresh credentials, not blind retry), 404 not found (no retry), 429 too many requests (retry later), 503 service unavailable (retry with backoff).
**3.** It would freeze the UI (ANR) and Android throws `NetworkOnMainThreadException`.
**4.** 50 × 2 + 30 × 3 = 100 + 90 = **190**.
**5.** Loading, success (data) and error.
**6.** min(20, 2 × 2^a) for a = 0 to 4: **2, 4, 8, 16, 20**.
**7.** Repeating it has the same effect as doing it once (GET, or a POST with an idempotency key), so a retry cannot create duplicates.
**8.** WorkManager persists the request and reruns it after process death or reboot, with constraints and backoff.
**9.** Batch requests, push instead of polling, sync on Wi-Fi/unmetered networks, compress and paginate data, cache.
**10.** Connectivity is intermittent and data is costly, so showing cached data and syncing when possible gives a usable app.
:::
