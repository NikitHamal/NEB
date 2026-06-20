package com.neb.ians.ui.components

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.ui.graphics.vector.ImageVector

fun getMaterialIcon(name: String): ImageVector {
    return when (name.lowercase().trim()) {
        "smart_toy" -> Icons.Filled.SmartToy
        "bolt", "electric_bolt" -> Icons.Filled.Bolt
        "settings" -> Icons.Filled.Settings
        "sensors" -> Icons.Filled.Sensors
        "build" -> Icons.Filled.Build
        "directions_car" -> Icons.Filled.DirectionsCar
        "route" -> Icons.Filled.Route
        "precision_manufacturing" -> Icons.Filled.PrecisionManufacturing
        "radar" -> Icons.Filled.Radar
        "toys" -> Icons.Filled.Toys
        "back_hand" -> Icons.Filled.BackHand
        "sports_score" -> Icons.Filled.SportsScore
        "sports_basketball" -> Icons.Filled.SportsBasketball
        "explore" -> Icons.Filled.Explore
        "science" -> Icons.Filled.Science
        "av_timer" -> Icons.Filled.AvTimer
        "rocket_launch" -> Icons.Filled.RocketLaunch
        "graphic_eq" -> Icons.Filled.GraphicEq
        "electric_meter" -> Icons.Filled.ElectricMeter
        "music_note" -> Icons.Filled.MusicNote
        "balance" -> Icons.Filled.Balance
        "settings_input_component" -> Icons.Filled.SettingsInputComponent
        "speed" -> Icons.Filled.Speed
        "center_focus_strong" -> Icons.Filled.CenterFocusStrong
        "change_history" -> Icons.Filled.ChangeHistory
        "straighten" -> Icons.Filled.Straighten
        "wb_sunny" -> Icons.Filled.WbSunny
        "travel_explore" -> Icons.Filled.TravelExplore
        "public" -> Icons.Filled.Public
        "dark_mode" -> Icons.Filled.DarkMode
        "brightness_3" -> Icons.Filled.Brightness3
        "gesture" -> Icons.Filled.Gesture
        "animation" -> Icons.Filled.Animation
        "fitness_center" -> Icons.Filled.FitnessCenter
        "auto_awesome" -> Icons.Filled.AutoAwesome
        "flare" -> Icons.Filled.Flare
        "local_fire_department" -> Icons.Filled.LocalFireDepartment
        "zoom_out_map" -> Icons.Filled.ZoomOutMap
        "school" -> Icons.Filled.School
        "history" -> Icons.Filled.History
        "language" -> Icons.Filled.Language
        "book" -> Icons.Filled.Book
        "menu_book" -> Icons.Filled.MenuBook
        "auto_stories" -> Icons.Filled.AutoStories
        "fact_check" -> Icons.Filled.FactCheck
        "campaign" -> Icons.Filled.Campaign
        "event" -> Icons.Filled.Event
        "upgrade" -> Icons.Filled.Upgrade
        "warning" -> Icons.Filled.Warning
        "info" -> Icons.Filled.Info
        "newspaper" -> Icons.Filled.Newspaper
        "apps" -> Icons.Filled.Apps
        "push_pin" -> Icons.Filled.PushPin
        "receipt_long" -> Icons.Filled.ReceiptLong
        "download" -> Icons.Filled.Download
        "construction" -> Icons.Filled.Construction
        "calculate" -> Icons.Filled.Calculate
        "account_tree" -> Icons.Filled.AccountTree
        "timeline" -> Icons.Filled.Timeline
        "open_with" -> Icons.Filled.OpenWith
        else -> Icons.Filled.HelpOutline
    }
}
