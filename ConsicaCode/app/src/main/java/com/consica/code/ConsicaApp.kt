package com.consica.code

import android.app.Application
import com.consica.code.core.di.AppContainer

class ConsicaApp : Application() {
    lateinit var container: AppContainer
        private set

    override fun onCreate() {
        super.onCreate()
        container = AppContainer(this)
    }
}
