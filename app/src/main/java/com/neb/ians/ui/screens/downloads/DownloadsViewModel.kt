package com.neb.ians.ui.screens.downloads

import androidx.lifecycle.ViewModel
import com.neb.ians.util.ResourceDownloadManager
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject

@HiltViewModel
class DownloadsViewModel @Inject constructor(
    private val downloadManager: ResourceDownloadManager
) : ViewModel() {
    val downloads = downloadManager.downloads
    val progress = downloadManager.downloadProgress

    fun delete(resourceId: String) {
        downloadManager.deleteDownload(resourceId)
    }
}
