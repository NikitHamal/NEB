package com.neb.ians.ui.forum

import android.content.Intent
import android.os.Bundle
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.IntentCompat
import androidx.core.view.WindowCompat
import androidx.recyclerview.widget.LinearLayoutManager
import com.neb.ians.data.model.ForumThread
import com.neb.ians.databinding.ActivityThreadDetailBinding
import com.neb.ians.ui.forum.adapters.ReplyAdapter
import com.neb.ians.utils.formatTimestamp

class ThreadDetailActivity : AppCompatActivity() {

    private lateinit var binding: ActivityThreadDetailBinding
    private val viewModel: ForumViewModel by viewModels()
    private lateinit var adapter: ReplyAdapter
    private lateinit var thread: ForumThread

    companion object {
        const val EXTRA_THREAD = "extra_thread"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        WindowCompat.setDecorFitsSystemWindows(window, false)
        binding = ActivityThreadDetailBinding.inflate(layoutInflater)
        setContentView(binding.root)

        thread = IntentCompat.getParcelableExtra(intent, EXTRA_THREAD, ForumThread::class.java) ?: run {
            finish()
            return
        }

        setupToolbar()
        setupUI()
        setupRecycler()

        viewModel.replies.observe(this) { list ->
            adapter.submitList(list)
        }

        viewModel.loadReplies(thread.id)
    }

    private fun setupToolbar() {
        binding.toolbar.setNavigationOnClickListener { finish() }
    }

    private fun setupUI() {
        binding.tvThreadTitle.text = thread.title
        binding.tvThreadBody.text = thread.body
        binding.tvLikes.text = thread.likes.toString()

        binding.btnLike.setOnClickListener {
            viewModel.likeThread(thread.id)
        }

        binding.btnReply.setOnClickListener {
            val intent = Intent(this, ReplyActivity::class.java).apply {
                putExtra(ReplyActivity.EXTRA_THREAD_ID, thread.id)
                putExtra(ReplyActivity.EXTRA_THREAD_TITLE, thread.title)
            }
            startActivity(intent)
        }
    }

    private fun setupRecycler() {
        adapter = ReplyAdapter(onLike = { reply ->
            viewModel.likeReply(reply.id)
        })
        binding.recyclerReplies.layoutManager = LinearLayoutManager(this)
        binding.recyclerReplies.adapter = adapter
    }

    override fun onResume() {
        super.onResume()
        viewModel.loadReplies(thread.id)
    }
}
