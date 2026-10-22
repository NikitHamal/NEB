package com.neb.ians

/**
 * Features that are built but not public yet. The marketplace (creator pages, courses, the
 * studio) keeps all its code and routes; while this is false nothing in the app links to it.
 * The server gates the same feature with MARKETPLACE_ENABLED (nebians/features.py).
 */
object AppFeatures {
    const val MARKETPLACE = false
}
