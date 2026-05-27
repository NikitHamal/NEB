package com.neb.ians.ui.pdf

import android.app.AlertDialog
import android.os.Bundle
import android.view.LayoutInflater
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.WindowCompat
import com.neb.ians.R
import com.neb.ians.data.model.AnnotationType
import com.neb.ians.databinding.ActivityPdfViewerBinding
import com.neb.ians.databinding.DialogAnnotationBinding
import java.io.File

class PdfViewerActivity : AppCompatActivity() {

    private lateinit var binding: ActivityPdfViewerBinding
    private val viewModel: PdfViewerViewModel by viewModels()

    companion object {
        const val EXTRA_PDF_PATH = "pdf_path"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        WindowCompat.setDecorFitsSystemWindows(window, false)
        binding = ActivityPdfViewerBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val pdfPath = intent.getStringExtra(EXTRA_PDF_PATH) ?: run {
            Toast.makeText(this, "No PDF provided", Toast.LENGTH_SHORT).show()
            finish()
            return
        }

        setupToolbar()
        setupControls()
        setupPdfView()

        viewModel.pageBitmap.observe(this) { bitmap ->
            binding.pdfPageView.setPageBitmap(bitmap)
        }
        viewModel.annotations.observe(this) { list ->
            binding.pdfPageView.setAnnotations(list)
        }
        viewModel.pageInfo.observe(this) { info ->
            binding.tvPageInfo.text = info
        }

        viewModel.openPdf(pdfPath)
    }

    private fun setupToolbar() {
        binding.toolbar.setNavigationOnClickListener { finish() }
        binding.toolbar.setOnMenuItemClickListener { item ->
            when (item.itemId) {
                R.id.action_annotate -> {
                    Toast.makeText(this, "Long-press and drag to select an area", Toast.LENGTH_SHORT).show()
                    true
                }
                else -> false
            }
        }
    }

    private fun setupControls() {
        binding.btnPrev.setOnClickListener { viewModel.prevPage() }
        binding.btnNext.setOnClickListener { viewModel.nextPage() }
    }

    private fun setupPdfView() {
        binding.pdfPageView.setOnAreaSelectedListener { x, y, w, h ->
            showAnnotationDialog(x, y, w, h)
        }
    }

    private fun showAnnotationDialog(x: Float, y: Float, w: Float, h: Float) {
        val dialogBinding = DialogAnnotationBinding.inflate(LayoutInflater.from(this))
        AlertDialog.Builder(this)
            .setView(dialogBinding.root)
            .create()
            .apply {
                dialogBinding.btnSave.setOnClickListener {
                    val type = when (dialogBinding.toggleType.checkedButtonId) {
                        R.id.btnHighlight -> AnnotationType.HIGHLIGHT
                        R.id.btnUnderline -> AnnotationType.UNDERLINE
                        else -> AnnotationType.STICKY_NOTE
                    }
                    val note = dialogBinding.etNote.text?.toString()
                    viewModel.addAnnotation(type, x, y, w, h, note)
                    dismiss()
                }
                dialogBinding.btnCancel.setOnClickListener { dismiss() }
                show()
            }
    }
}
