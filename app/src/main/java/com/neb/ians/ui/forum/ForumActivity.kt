package com.neb.ians.ui.forum

import android.content.Intent
import android.os.Bundle
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.WindowCompat
import androidx.recyclerview.widget.LinearLayoutManager
import com.neb.ians.R
import com.neb.ians.databinding.ActivityForumBinding
import com.neb.ians.ui.forum.adapters.ThreadAdapter
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.google.android.material.textfield.TextInputEditText

class ForumActivity : AppCompatActivity() {

    private lateinit var binding: ActivityForumBinding
    private val viewModel: ForumViewModel by viewModels()
    private lateinit var adapter: ThreadAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        WindowCompat.setDecorFitsSystemWindows(window, false)
        binding = ActivityForumBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupToolbar()
        setupRecycler()

        viewModel.threads.observe(this) { list ->
            adapter.submitList(list)
            binding.tvEmpty.visibility = if (list.isEmpty()) android.view.View.VISIBLE else android.view.View.GONE
        }
    }

    private fun setupToolbar() {
        binding.toolbar.setNavigationOnClickListener { finish() }
        binding.toolbar.setOnMenuItemClickListener { item ->
            if (item.itemId == R.id.action_new_thread) {
                showNewThreadDialog()
                true
            } else false
        }
    }

    private fun setupRecycler() {
        adapter = ThreadAdapter(
            onClick = { thread ->
                val intent = Intent(this, ThreadDetailActivity::class.java).apply {
                    putExtra(ThreadDetailActivity.EXTRA_THREAD, thread)
                }
                startActivity(intent)
            },
            onLike = { thread ->
                viewModel.likeThread(thread.id)
            }
        )
        binding.recyclerThreads.layoutManager = LinearLayoutManager(this)
        binding.recyclerThreads.adapter = adapter
    }

    private fun showNewThreadDialog() {
        val view = layoutInflater.inflate(R.layout.dialog_new_thread, null)
        val etTitle = view.findViewById<TextInputEditText>(R.id.etTitle)
        val etBody = view.findViewById<TextInputEditText>(R.id.etBody)

        MaterialAlertDialogBuilder(this)
            .setTitle("New Discussion")
            .setView(view)
            .setPositiveButton("Post") { _, _ ->
                val title = etTitle.text?.toString()?.trim() ?: ""
                val body = etBody.text?.toString()?.trim() ?: ""
                if (title.isNotEmpty() && body.isNotEmpty()) {
                    viewModel.createThread(title, body)
                }
            }
            .setNegativeButton("Cancel", null)
            .show()
    }
}
