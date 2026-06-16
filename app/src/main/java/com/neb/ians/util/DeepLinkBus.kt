package com.neb.ians.util

import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

object DeepLinkBus {
    private val _pendingDeepLink = MutableStateFlow<NotificationDeepLink?>(null)
    val pendingDeepLink: StateFlow<NotificationDeepLink?> = _pendingDeepLink.asStateFlow()

    fun emit(deepLink: NotificationDeepLink) {
        _pendingDeepLink.value = deepLink
    }

    fun clear() {
        _pendingDeepLink.value = null
    }
}
