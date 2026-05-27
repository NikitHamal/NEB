package com.neb.ians.ui.common

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.WindowCompat
import com.neb.ians.databinding.ActivitySettingsBinding
import com.neb.ians.utils.ThemeManager

class SettingsActivity : AppCompatActivity() {

    private lateinit var binding: ActivitySettingsBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        WindowCompat.setDecorFitsSystemWindows(window, false)
        binding = ActivitySettingsBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupToolbar()
        setupSwitches()
    }

    private fun setupToolbar() {
        binding.toolbar.setNavigationOnClickListener { finish() }
    }

    private fun setupSwitches() {
        binding.switchDarkMode.isChecked = ThemeManager.isDarkMode()
        binding.switchDarkMode.setOnCheckedChangeListener { _, isChecked ->
            ThemeManager.setDarkMode(isChecked)
            recreate()
        }

        binding.switchNotifications.isChecked = ThemeManager.areNotificationsEnabled()
        binding.switchNotifications.setOnCheckedChangeListener { _, isChecked ->
            ThemeManager.setNotificationsEnabled(isChecked)
        }
    }
}
