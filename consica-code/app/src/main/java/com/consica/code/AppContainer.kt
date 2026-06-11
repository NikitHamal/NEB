package com.consica.code

import android.content.Context
import com.consica.code.data.local.CcodeDatabase
import com.consica.code.data.prefs.UserPreferencesRepository
import com.consica.code.data.repo.LearningRepository
import com.consica.code.data.repo.WorkspaceRepository
import com.consica.code.util.ConnectivityObserver
import com.consica.code.util.SoundManager

/**
 * Simple manual dependency container — small surface, explicit wiring,
 * no annotation processing. Owned by [CcodeApp].
 */
class AppContainer(context: Context) {
    val database: CcodeDatabase by lazy { CcodeDatabase.get(context) }
    val prefs: UserPreferencesRepository by lazy { UserPreferencesRepository(context) }
    val learning: LearningRepository by lazy { LearningRepository(database, prefs) }
    val workspaces: WorkspaceRepository by lazy { WorkspaceRepository(database) }
    val connectivity: ConnectivityObserver by lazy { ConnectivityObserver(context) }
    val sound: SoundManager by lazy { SoundManager() }
}
