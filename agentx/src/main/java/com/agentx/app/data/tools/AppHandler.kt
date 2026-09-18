package com.agentx.app.data.tools

import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.provider.Settings
import com.agentx.app.data.engine.ToolCallSpec
import com.agentx.app.util.FuzzyMatch
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject
import javax.inject.Singleton

data class LaunchableApp(val name: String, val packageName: String)

@Singleton
class AppHandler @Inject constructor(
    @ApplicationContext private val context: Context
) {
    fun launchableApps(): List<LaunchableApp> {
        val manager = context.packageManager
        val main = Intent(Intent.ACTION_MAIN, null).addCategory(Intent.CATEGORY_LAUNCHER)
        return manager.queryIntentActivities(main, 0).mapNotNull { info ->
            val label = info.loadLabel(manager)?.toString()?.trim().orEmpty()
            val pkg = info.activityInfo?.packageName.orEmpty()
            if (label.isEmpty() || pkg.isEmpty()) null else LaunchableApp(label, pkg)
        }.sortedBy { it.name.lowercase() }
    }

    fun resolve(name: String): List<FuzzyMatch.Scored<LaunchableApp>> {
        val query = FuzzyMatch.normalize(name)
        if (query.isEmpty()) return emptyList()
        val apps = launchableApps()
        val exact = apps.filter { FuzzyMatch.normalize(it.name) == query }
        if (exact.isNotEmpty()) return exact.map { FuzzyMatch.Scored(it, 1000) }
        return FuzzyMatch.rank(name, apps, { it.name }, 5).filter { it.score >= 60 }
    }

    fun openApp(spec: ToolCallSpec): ToolExecution {
        val name = spec.arg("name") ?: return ToolExecution.fail("Which app should I open?")
        val matches = resolve(name)
        if (matches.isEmpty()) {
            val hint = launchableApps().take(8).joinToString(", ") { it.name }
            return ToolExecution.fail("No app matching " + name + ". Try one of: " + hint)
        }
        val top = matches.first()
        val close = matches.filter { it.score >= top.score - 40 }.take(3)
        if (close.size > 1 && close[0].score < 900) {
            return ToolExecution.fail(
                "Which one? " + close.joinToString(", ") { it.item.name },
                options = close.map { "Open " + it.item.name }
            )
        }
        val intent = context.packageManager.getLaunchIntentForPackage(top.item.packageName)
            ?: return ToolExecution.fail("Could not launch " + top.item.name)
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        runCatching { context.startActivity(intent) }.onFailure {
            return ToolExecution.fail("Could not launch " + top.item.name)
        }
        return ToolExecution.done("Opened " + top.item.name)
    }

    fun appInfo(spec: ToolCallSpec): ToolExecution {
        val name = spec.arg("name") ?: return ToolExecution.fail("Which app?")
        val matches = resolve(name)
        if (matches.isEmpty()) return ToolExecution.fail("No app matching " + name)
        val pkg = matches.first().item.packageName
        val intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS).apply {
            data = Uri.fromParts("package", pkg, null)
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        runCatching { context.startActivity(intent) }.onFailure {
            return ToolExecution.fail("Could not open app info")
        }
        return ToolExecution.done("App info opened")
    }

    fun appNamesForSearch(): List<String> = launchableApps().map { it.name }
}
