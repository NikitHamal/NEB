package com.neb.ians.data.api

import kotlinx.coroutines.flow.MutableSharedFlow

object AuthExpiryBus {
    val events = MutableSharedFlow<Unit>(extraBufferCapacity = 1, replay = 1)
}
