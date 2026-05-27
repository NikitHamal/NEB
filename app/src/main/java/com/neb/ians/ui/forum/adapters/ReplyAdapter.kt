package com.neb.ians.ui.forum.adapters

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.neb.ians.data.model.ForumReply
import com.neb.ians.databinding.ItemReplyBinding

class ReplyAdapter(
    private val onLike: (ForumReply) -> Unit
) : ListAdapter<ForumReply, ReplyAdapter.ViewHolder>(DiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val binding = ItemReplyBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return ViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    inner class ViewHolder(private val binding: ItemReplyBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(reply: ForumReply) {
            binding.tvBody.text = reply.body
            binding.tvLikes.text = reply.likes.toString()
            binding.root.setOnClickListener { onLike(reply) }
        }
    }

    class DiffCallback : DiffUtil.ItemCallback<ForumReply>() {
        override fun areItemsTheSame(oldItem: ForumReply, newItem: ForumReply) = oldItem.id == newItem.id
        override fun areContentsTheSame(oldItem: ForumReply, newItem: ForumReply) = oldItem == newItem
    }
}
