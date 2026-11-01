package com.neb.ians.data.api

import kotlinx.coroutines.flow.MutableSharedFlow

object AuthExpiryBus {
    // replay = 0 on purpose. A replay cache would outlive the event: sign in
    // again after an expiry, rotate the device, and the recreated NavHost
    // collector would immediately re-deliver the stale expiry and sign the
    // freshly signed-in user straight back out. Delivery to a live collector is
    // what we want; a dropped event only costs a recovery until the next 401.
    val events = MutableSharedFlow<Unit>(extraBufferCapacity = 1, replay = 0)

    fun tryEmitExpired() {
        events.tryEmit(Unit)
    }
}
