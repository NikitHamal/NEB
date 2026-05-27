package com.neb.ians.ui.resources

import android.content.Intent
import android.os.Bundle
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.WindowCompat
import androidx.core.widget.doAfterTextChanged
import androidx.recyclerview.widget.LinearLayoutManager
import com.neb.ians.data.model.Resource
import com.neb.ians.databinding.ActivityResourceListBinding
import com.neb.ians.ui.pdf.PdfViewerActivity
import com.neb.ians.ui.resources.adapters.ResourceAdapter

class ResourceListActivity : AppCompatActivity() {

    private lateinit var binding: ActivityResourceListBinding
    private val viewModel: ResourceListViewModel by viewModels()
    private lateinit var adapter: ResourceAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        WindowCompat.setDecorFitsSystemWindows(window, false)
        binding = ActivityResourceListBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupToolbar()
        setupRecycler()
        setupSearch()
        setupFilters()

        viewModel.results.observe(this) { list ->
            adapter.submitList(list)
            binding.tvEmpty.visibility = if (list.isEmpty()) android.view.View.VISIBLE else android.view.View.GONE
        }

        viewModel.search("")
    }

    private fun setupToolbar() {
        binding.toolbar.setNavigationOnClickListener { finish() }
    }

    private fun setupRecycler() {
        adapter = ResourceAdapter(onOpen = { resource ->
            openResource(resource)
        })
        binding.recyclerResources.layoutManager = LinearLayoutManager(this)
        binding.recyclerResources.adapter = adapter
    }

    private fun setupSearch() {
        binding.etSearch.doAfterTextChanged { text ->
            viewModel.search(text?.toString() ?: "")
        }
    }

    private fun setupFilters() {
        binding.chipAll.setOnClickListener { viewModel.setGradeFilter(null) }
        binding.chipGrade11.setOnClickListener {
            viewModel.setGradeFilter(com.neb.ians.data.model.Grade.GRADE_11)
        }
        binding.chipGrade12.setOnClickListener {
            viewModel.setGradeFilter(com.neb.ians.data.model.Grade.GRADE_12)
        }
    }

    private fun openResource(resource: Resource) {
        val intent = Intent(this, PdfViewerActivity::class.java).apply {
            putExtra(PdfViewerActivity.EXTRA_PDF_PATH, resource.localPath ?: resource.remoteUrl)
        }
        startActivity(intent)
    }
}
