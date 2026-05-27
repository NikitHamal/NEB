package com.neb.ians.ui.main

import android.content.Intent
import android.os.Bundle
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.WindowCompat
import com.neb.ians.R
import com.neb.ians.databinding.ActivityMainBinding
import com.neb.ians.ui.forum.ForumActivity
import com.neb.ians.ui.resources.ResourceListActivity
import com.neb.ians.ui.common.SettingsActivity

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private val viewModel: MainViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        WindowCompat.setDecorFitsSystemWindows(window, false)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupToolbar()
        setupBottomNav()
        setupCards()
    }

    private fun setupToolbar() {
        setSupportActionBar(binding.toolbar)
        supportActionBar?.setDisplayShowTitleEnabled(false)
    }

    private fun setupBottomNav() {
        binding.bottomNav.setOnItemSelectedListener { item ->
            when (item.itemId) {
                R.id.nav_home -> {
                    // Already home
                    true
                }
                R.id.nav_resources -> {
                    startActivity(Intent(this, ResourceListActivity::class.java))
                    true
                }
                R.id.nav_forum -> {
                    startActivity(Intent(this, ForumActivity::class.java))
                    true
                }
                R.id.nav_settings -> {
                    startActivity(Intent(this, SettingsActivity::class.java))
                    true
                }
                else -> false
            }
        }
    }

    private fun setupCards() {
        binding.cardResources.setOnClickListener {
            startActivity(Intent(this, ResourceListActivity::class.java))
        }
        binding.cardForum.setOnClickListener {
            startActivity(Intent(this, ForumActivity::class.java))
        }
    }
}
