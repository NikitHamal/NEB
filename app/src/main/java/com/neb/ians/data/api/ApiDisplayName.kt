package com.neb.ians.data.api

/** The name people chose to show. Falls back to the username. Navigation keeps using `authorName` (the username). */
val ApiPost.shownName: String get() = authorDisplayName?.takeIf { it.isNotBlank() } ?: authorName
val ApiReply.shownName: String get() = authorDisplayName?.takeIf { it.isNotBlank() } ?: authorName
