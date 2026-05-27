package com.neb.ians.ui.resources.adapters

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.neb.ians.data.model.Resource
import com.neb.ians.databinding.ItemResourceBinding

class ResourceAdapter(
    private val onOpen: (Resource) -> Unit
) : ListAdapter<Resource, ResourceAdapter.ViewHolder>(DiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val binding = ItemResourceBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return ViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    inner class ViewHolder(private val binding: ItemResourceBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(resource: Resource) {
            binding.tvTitle.text = resource.title
            binding.tvMeta.text = "${resource.subject.displayName} • ${resource.grade.displayName} • ${resource.type.displayName}"
            binding.btnAction.setOnClickListener { onOpen(resource) }
            binding.cardRoot.setOnClickListener { onOpen(resource) }
        }
    }

    class DiffCallback : DiffUtil.ItemCallback<Resource>() {
        override fun areItemsTheSame(oldItem: Resource, newItem: Resource) = oldItem.id == newItem.id
        override fun areContentsTheSame(oldItem: Resource, newItem: Resource) = oldItem == newItem
    }
}
