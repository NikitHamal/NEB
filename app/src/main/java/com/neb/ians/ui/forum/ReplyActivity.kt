package com.neb.ians.ui.forum

import android.os.Bundle
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.WindowCompat
import com.neb.ians.databinding.ActivityReplyBinding

class ReplyActivity : AppCompatActivity() {

    private lateinit var binding: ActivityReplyBinding
    private val viewModel: ForumViewModel by viewModels()

    companion object {
        const val EXTRA_THREAD_ID = "thread_id"
        const val EXTRA_THREAD_TITLE = "thread_title"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        WindowCompat.setDecorFitsSystemWindows(window, false)
        binding = ActivityReplyBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val threadId = intent.getStringExtra(EXTRA_THREAD_ID) ?: run {
            finish()
            return
        }
        val title = intent.getStringExtra(EXTRA_THREAD_TITLE) ?: ""

        setupToolbar()
        binding.tvReplyingTo.text = "Replying to: $title"

        binding.btnCancel.setOnClickListener { finish() }
        binding.btnPost.setOnClickListener {
            val body = binding.etBody.text?.toString()?.trim() ?: ""
            if (body.isNotEmpty()) {
                viewModel.addReply(threadId, body)
                Toast.makeText(this, "Reply posted", Toast.LENGTH_SHORT).show()
                finish()
            } else {
                Toast.makeText(this, "Reply cannot be empty", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun setupToolbar() {
        binding.toolbar.setNavigationOnClickListener { finish() }
    }
}
