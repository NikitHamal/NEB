package com.consica.code.ui.common

import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import com.consica.code.AppContainer
import com.consica.code.CcodeApp

/** Creates a ViewModel wired to the [AppContainer] without a DI framework. */
@Composable
inline fun <reified VM : ViewModel> appViewModel(
    key: String? = null,
    crossinline create: (AppContainer) -> VM,
): VM {
    val app = LocalContext.current.applicationContext as CcodeApp
    return viewModel(
        key = key,
        factory = viewModelFactory {
            initializer { create(app.container) }
        },
    )
}
