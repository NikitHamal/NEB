package com.neb.ians

import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage

class NebFirebaseMessagingService : FirebaseMessagingService() {
    override fun onMessageReceived(message: RemoteMessage) {
        NotificationHelper.ensureChannel(this)
        val title = message.notification?.title
            ?: message.data["title"]
            ?: "NEBians update"
        val body = message.notification?.body
            ?: message.data["body"]
            ?: "Open NEBians for the latest study updates."
        NotificationHelper.show(this, title, body)
    }

    override fun onNewToken(token: String) {
        super.onNewToken(token)
        // A production backend can register this token for announcement and community topics.
    }
}
