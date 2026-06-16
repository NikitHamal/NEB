package com.neb.ians.util

import android.app.Activity
import android.content.Intent
import android.util.Log
import androidx.activity.result.ActivityResult
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts
import com.google.android.play.core.appupdate.AppUpdateInfo
import com.google.android.play.core.appupdate.AppUpdateManager
import com.google.android.play.core.appupdate.AppUpdateManagerFactory
import com.google.android.play.core.appupdate.AppUpdateOptions
import com.google.android.play.core.install.InstallState
import com.google.android.play.core.install.InstallStateUpdatedListener
import com.google.android.play.core.install.model.AppUpdateType
import com.google.android.play.core.install.model.InstallStatus
import com.google.android.play.core.install.model.UpdateAvailability
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class InAppUpdateHelper @Inject constructor(
    @ApplicationContext private val context: android.content.Context
) {
    companion object {
        private const val TAG = "InAppUpdate"
        const val REQUEST_CODE_UPDATE = 9100
    }

    private val appUpdateManager: AppUpdateManager = AppUpdateManagerFactory.create(context)
    private var updateInfo: AppUpdateInfo? = null
    private var isChecking = false

    private val installStateListener = InstallStateUpdatedListener { state ->
        when (state.installStatus()) {
            InstallStatus.DOWNLOADING -> {
                Log.d(TAG, "Update downloading: ${state.bytesDownloaded()} / ${state.totalBytesToDownload()}")
            }
            InstallStatus.DOWNLOADED -> {
                Log.d(TAG, "Update downloaded, ready to install")
                appUpdateManager.completeUpdate()
            }
            InstallStatus.INSTALLING -> {
                Log.d(TAG, "Update installing...")
            }
            InstallStatus.INSTALLED -> {
                Log.d(TAG, "Update installed successfully")
                appUpdateManager.unregisterListener(installStateListener)
            }
            InstallStatus.FAILED -> {
                Log.w(TAG, "Update failed: ${state.installErrorCode()}")
                appUpdateManager.unregisterListener(installStateListener)
                updateInfo = null
                isChecking = false
            }
            InstallStatus.CANCELED -> {
                Log.w(TAG, "Update cancelled by user")
                appUpdateManager.unregisterListener(installStateListener)
                updateInfo = null
                isChecking = false
            }
            else -> {
                Log.d(TAG, "Install state: ${state.installStatus()}")
            }
        }
    }

    fun registerListener() {
        appUpdateManager.registerListener(installStateListener)
    }

    fun unregisterListener() {
        try {
            appUpdateManager.unregisterListener(installStateListener)
        } catch (_: IllegalStateException) {}
    }

    fun checkForUpdate(activity: Activity) {
        if (isChecking) return
        isChecking = true

        appUpdateManager.appUpdateInfo.addOnSuccessListener { info ->
            updateInfo = info
            handleUpdateInfo(info, activity)
        }.addOnFailureListener { e ->
            Log.w(TAG, "Failed to check for update: ${e.message}")
            isChecking = false
        }
    }

    fun onResume(activity: Activity) {
        appUpdateManager.appUpdateInfo.addOnSuccessListener { info ->
            updateInfo = info

            if (info.updateAvailability() == UpdateAvailability.DEVELOPER_TRIGGERED_UPDATE_IN_PROGRESS) {
                Log.d(TAG, "Update already in progress, resuming...")
                startImmediateUpdate(activity, info)
                return@addOnSuccessListener
            }

            if (info.installStatus() == InstallStatus.DOWNLOADED) {
                Log.d(TAG, "Update already downloaded, completing...")
                appUpdateManager.completeUpdate()
                return@addOnSuccessListener
            }

            if (info.updateAvailability() == UpdateAvailability.UPDATE_AVAILABLE &&
                info.isUpdateTypeAllowed(AppUpdateType.IMMEDIATE)
            ) {
                Log.d(TAG, "Update still available, re-prompting...")
                startImmediateUpdate(activity, info)
                return@addOnSuccessListener
            }
        }.addOnFailureListener { e ->
            Log.w(TAG, "Failed to check update state on resume: ${e.message}")
        }
    }

    fun onActivityResult(resultCode: Int): Boolean {
        when (resultCode) {
            Activity.RESULT_OK -> {
                Log.d(TAG, "Update flow accepted by user")
                return true
            }
            Activity.RESULT_CANCELED, Activity.RESULT_FIRST_USER -> {
                Log.w(TAG, "Update flow cancelled/deferred by user")
                return false
            }
            else -> {
                Log.w(TAG, "Unknown result code from update flow: $resultCode")
                return false
            }
        }
    }

    fun release() {
        unregisterListener()
        updateInfo = null
        isChecking = false
    }

    private fun handleUpdateInfo(info: AppUpdateInfo, activity: Activity) {
        if (info.updateAvailability() == UpdateAvailability.UPDATE_AVAILABLE &&
            info.isUpdateTypeAllowed(AppUpdateType.IMMEDIATE)
        ) {
            Log.d(TAG, "Immediate update available: v${info.availableVersionCode()}")
            startImmediateUpdate(activity, info)
        } else {
            Log.d(TAG, "No update available or not allowed. Status: ${info.updateAvailability()}, Install: ${info.installStatus()}")
            isChecking = false
        }
    }

    private fun startImmediateUpdate(activity: Activity, info: AppUpdateInfo) {
        registerListener()

        val options = AppUpdateOptions.newBuilder(AppUpdateType.IMMEDIATE)
            .setAllowAssetPackDeletion(false)
            .build()

        try {
            appUpdateManager.startUpdateFlowForResult(
                info,
                activity,
                options,
                REQUEST_CODE_UPDATE
            )
        } catch (e: Exception) {
            Log.e(TAG, "Failed to start immediate update: ${e.message}")
            isChecking = false
        }
    }
}
