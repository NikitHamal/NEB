package com.neb.ians.utils

import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

fun Long.formatTimestamp(): String {
    val sdf = SimpleDateFormat("MMM dd, yyyy • hh:mm a", Locale.getDefault())
    return sdf.format(Date(this))
}
