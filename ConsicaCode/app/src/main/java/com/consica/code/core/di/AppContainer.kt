package com.consica.code.core.di

import android.content.Context
import com.consica.code.data.local.ConsicaDatabase
import com.consica.code.data.prefs.SettingsDataStore
import com.consica.code.data.repository.GameRepository
import com.consica.code.data.repository.WorkspaceRepository
import com.consica.code.domain.runner.CodeRunner
import com.consica.code.domain.runner.MiniPython

/**
 * Tiny manual DI container held by the Application. Keeps the dependency graph explicit and the
 * build free of annotation-processing DI frameworks (only Room uses KSP). Everything here is
 * process-singleton and offline.
 */
class AppContainer(context: Context) {
    private val appContext = context.applicationContext

    val settings: SettingsDataStore by lazy { SettingsDataStore(appContext) }

    private val database: ConsicaDatabase by lazy { ConsicaDatabase.get(appContext) }

    val gameRepository: GameRepository by lazy {
        GameRepository(
            settings = settings,
            lessonProgressDao = database.lessonProgressDao(),
            badgeDao = database.badgeDao(),
            ecosystemDao = database.ecosystemDao(),
            codeAttemptDao = database.codeAttemptDao(),
        )
    }

    val workspaceRepository: WorkspaceRepository by lazy {
        WorkspaceRepository(database.workspaceDao(), database.codeAttemptDao())
    }

    /** Swap [MiniPython] for a Pyodide-backed runner here to upgrade Python support. */
    val pythonRunner: CodeRunner by lazy { MiniPython() }
}
