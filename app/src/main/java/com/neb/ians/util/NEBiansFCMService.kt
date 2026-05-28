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
        // Register token with the Cloudflare Worker API in the background
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val userToken = authRepository.tokenFlow.first()
                val bearer = userToken?.let { "Bearer $it" }
                apiService.registerFcmToken(bearer, FcmTokenRequest(token))
            } catch (e: Exception) {
                // Silently ignore during background token refreshing
            }
        }
    }

    override fun onMessageReceived(message: RemoteMessage) {
        super.onMessageReceived(message)
        
        // Extract title and body from the payload
        val title = message.notification?.title ?: message.data["title"] ?: "NEBians Board Notification"
        val body = message.notification?.body ?: message.data["message"] ?: "Check out new resources and updates."
        val channelId = message.data["channel_id"] ?: "announcements"

        // Trigger local notification delivery
        NotificationHelper.sendImmediateNotification(
            context = this,
            title = title,
            message = body,
            channelId = channelId
        )
    }
}
