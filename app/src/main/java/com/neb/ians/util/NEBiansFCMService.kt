package com.neb.ians.util

import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.FcmTokenRequest
import com.neb.ians.data.repository.AuthRepository
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import javax.inject.Inject

@AndroidEntryPoint
class NEBiansFCMService : FirebaseMessagingService() {

    @Inject
    lateinit var apiService: ApiService

    @Inject
    lateinit var authRepository: AuthRepository

    override fun onNewToken(token: String) {
        super.onNewToken(token)
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val userToken = authRepository.tokenFlow.first()
                val bearer = userToken?.let { "Bearer $it" }
                apiService.registerFcmToken(bearer, FcmTokenRequest(token))
            } catch (e: Exception) {
            }
        }
    }

    override fun onMessageReceived(message: RemoteMessage) {
        super.onMessageReceived(message)

        val title = message.notification?.title ?: message.data["title"] ?: "NEBians"
        val body = message.notification?.body ?: message.data["message"] ?: "New activity on your account"

        val deepLink = NotificationDeepLink.fromFcmData(message.data)

        val channelId = resolveChannelId(deepLink.verb, deepLink.targetType)

        NotificationHelper.sendImmediateNotification(
            context = this,
            title = title,
            message = body,
            channelId = channelId,
            deepLink = deepLink
        )
    }

    private fun resolveChannelId(verb: String, targetType: String): String {
        if (verb == "system") return CHANNEL_ANNOUNCEMENTS
        if (targetType == "resource" || targetType == "resource_comment") return CHANNEL_DOWNLOADS
        return CHANNEL_FORUM
    }

    companion object {
        const val CHANNEL_ANNOUNCEMENTS = "announcements"
        const val CHANNEL_FORUM = "forum_activity"
        const val CHANNEL_DOWNLOADS = "downloads"
    }
}
