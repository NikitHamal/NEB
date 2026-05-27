package com.neb.ians.ui.forum.adapters

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.neb.ians.data.model.ForumThread
import com.neb.ians.databinding.ItemThreadBinding
import com.neb.ians.utils.formatTimestamp

class ThreadAdapter(
    private val onClick: (ForumThread) -> Unit,
    private val onLike: (ForumThread) -> Unit
) : ListAdapter<ForumThread, ThreadAdapter.ViewHolder>(DiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val binding = ItemThreadBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return ViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    inner class ViewHolder(private val binding: ItemThreadBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(thread: ForumThread) {
            binding.tvTitle.text = thread.title
            binding.tvPreview.text = thread.body
            binding.tvLikes.text = thread.likes.toString()
            binding.tvReplies.text = "${thread.repliesCount} replies"

            binding.cardRoot.setOnClickListener { onClick(thread) }
            // Like button could be wired directly if needed
        }
    }

    class DiffCallback : DiffUtil.ItemCallback<ForumThread>() {
        override fun areItemsTheSame(oldItem: ForumThread, newItem: ForumThread) = oldItem.id == newItem.id
        override fun areContentsTheSame(oldItem: ForumThread, newItem: ForumThread) = oldItem == newItem
    }
}
