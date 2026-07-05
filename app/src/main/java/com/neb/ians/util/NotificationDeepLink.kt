package com.neb.ians.util

import android.content.Intent
import android.os.Bundle
import com.neb.ians.ui.Screen

data class NotificationDeepLink(
    val notificationId: String?,
    val route: String?,
    val verb: String,
    val targetType: String,
    val targetId: String,
    val referenceType: String,
    val referenceId: String,
    val actorUsername: String?
) {

    fun toIntentExtras(): Bundle {
        return Bundle().apply {
            putString(EXTRA_NOTIFICATION_ID, notificationId)
            putString(EXTRA_VERB, verb)
            putString(EXTRA_TARGET_TYPE, targetType)
            putString(EXTRA_TARGET_ID, targetId)
            putString(EXTRA_REFERENCE_TYPE, referenceType)
            putString(EXTRA_REFERENCE_ID, referenceId)
            putString(EXTRA_ACTOR_USERNAME, actorUsername)
            putBoolean(EXTRA_IS_NOTIFICATION, true)
        }
    }

    companion object {
        const val EXTRA_IS_NOTIFICATION = "neb_extra_is_notification"
        const val EXTRA_NOTIFICATION_ID = "neb_extra_notification_id"
        const val EXTRA_VERB = "neb_extra_verb"
        const val EXTRA_TARGET_TYPE = "neb_extra_target_type"
        const val EXTRA_TARGET_ID = "neb_extra_target_id"
        const val EXTRA_REFERENCE_TYPE = "neb_extra_reference_type"
        const val EXTRA_REFERENCE_ID = "neb_extra_reference_id"
        const val EXTRA_ACTOR_USERNAME = "neb_extra_actor_username"

        fun fromIntent(intent: Intent): NotificationDeepLink? {
            val isNotification = intent.getBooleanExtra(EXTRA_IS_NOTIFICATION, false) ||
                    intent.hasExtra("verb") || intent.hasExtra("target_type")
            if (!isNotification) return null

            val verb = intent.getStringExtra(EXTRA_VERB) 
                ?: intent.getStringExtra("verb") 
                ?: ""
            val targetType = intent.getStringExtra(EXTRA_TARGET_TYPE)
                ?: intent.getStringExtra("target_type")
                ?: ""
            val targetId = intent.getStringExtra(EXTRA_TARGET_ID)
                ?: intent.getStringExtra("target_id")
                ?: ""
            val referenceType = intent.getStringExtra(EXTRA_REFERENCE_TYPE)
                ?: intent.getStringExtra("reference_type")
                ?: ""
            val referenceId = intent.getStringExtra(EXTRA_REFERENCE_ID)
                ?: intent.getStringExtra("reference_id")
                ?: ""
            val notificationId = intent.getStringExtra(EXTRA_NOTIFICATION_ID)
                ?: intent.getStringExtra("notification_id")
            val actorUsername = intent.getStringExtra(EXTRA_ACTOR_USERNAME)
                ?: intent.getStringExtra("actor_username")

            val route = resolveRoute(verb, targetType, targetId, referenceType, referenceId, actorUsername)
            return NotificationDeepLink(
                notificationId = notificationId,
                verb = verb,
                targetType = targetType,
                targetId = targetId,
                referenceType = referenceType,
                referenceId = referenceId,
                actorUsername = actorUsername,
                route = route
            )
        }

        fun fromBundle(extras: Bundle): NotificationDeepLink? {
            if (!extras.getBoolean(EXTRA_IS_NOTIFICATION, false)) return null
            val verb = extras.getString(EXTRA_VERB) ?: ""
            val targetType = extras.getString(EXTRA_TARGET_TYPE) ?: ""
            val targetId = extras.getString(EXTRA_TARGET_ID) ?: ""
            val referenceType = extras.getString(EXTRA_REFERENCE_TYPE) ?: ""
            val referenceId = extras.getString(EXTRA_REFERENCE_ID) ?: ""
            val notificationId = extras.getString(EXTRA_NOTIFICATION_ID)
            val actorUsername = extras.getString(EXTRA_ACTOR_USERNAME)
            val route = resolveRoute(verb, targetType, targetId, referenceType, referenceId, actorUsername)
            return NotificationDeepLink(
                notificationId = notificationId,
                verb = verb,
                targetType = targetType,
                targetId = targetId,
                referenceType = referenceType,
                referenceId = referenceId,
                actorUsername = actorUsername,
                route = route
            )
        }

        fun fromFcmData(data: Map<String, String>): NotificationDeepLink {
            val verb = data["verb"] ?: ""
            val targetType = data["target_type"] ?: ""
            val targetId = data["target_id"] ?: ""
            val referenceType = data["reference_type"] ?: ""
            val referenceId = data["reference_id"] ?: ""
            val notificationId = data["notification_id"]
            val actorUsername = data["actor_username"]?.takeIf { it.isNotBlank() }

            val route = resolveRoute(verb, targetType, targetId, referenceType, referenceId, actorUsername)

            return NotificationDeepLink(
                notificationId = notificationId,
                route = route,
                verb = verb,
                targetType = targetType,
                targetId = targetId,
                referenceType = referenceType,
                referenceId = referenceId,
                actorUsername = actorUsername
            )
        }

        fun resolveRoute(
            verb: String,
            targetType: String,
            targetId: String,
            referenceType: String,
            referenceId: String,
            actorUsername: String? = null
        ): String? {
            if (targetId.isBlank() && actorUsername.isNullOrBlank()) return null

            return when (verb) {
                "follow" -> {
                    if (!actorUsername.isNullOrBlank()) {
                        Screen.Profile.createRoute(actorUsername)
                    } else {
                        Screen.Notifications.route
                    }
                }
                else -> when (targetType) {
                    "post" -> Screen.ForumPostDetail.createRoute(targetId)
                    "reply" -> {
                        val postId = if (referenceType == "post") referenceId else ""
                        if (postId.isNotBlank()) {
                            Screen.ForumPostDetail.createRoute(postId)
                        } else {
                            Screen.Notifications.route
                        }
                    }
                    "resource" -> Screen.ResourceDetail.createRoute(targetId)
                    "resource_comment" -> {
                        val resourceId = if (referenceType == "resource") referenceId else ""
                        if (resourceId.isNotBlank()) {
                            Screen.ResourceDetail.createRoute(resourceId)
                        } else {
                            Screen.Notifications.route
                        }
                    }
                    "user" -> {
                        if (!actorUsername.isNullOrBlank()) {
                            Screen.Profile.createRoute(actorUsername)
                        } else {
                            Screen.Notifications.route
                        }
                    }
                    "system" -> {
                        if (targetType == "resource" && targetId.isNotBlank()) {
                            Screen.ResourceDetail.createRoute(targetId)
                        } else {
                            Screen.Notifications.route
                        }
                    }
                    else -> Screen.Notifications.route
                }
            }
        }
    }
}
