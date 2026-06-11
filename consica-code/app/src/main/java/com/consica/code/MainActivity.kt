package com.consica.code

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.core.splashscreen.SplashScreen.Companion.installSplashScreen
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.navigation.compose.rememberNavController
import com.consica.code.data.prefs.AppSettings
import com.consica.code.data.prefs.UserPreferencesRepository
import com.consica.code.domain.model.AgeGroup
import com.consica.code.domain.model.TerraExpression
import com.consica.code.ui.character.CharacterGuide
import com.consica.code.ui.character.GuideTrigger
import com.consica.code.ui.character.TerraToast
import com.consica.code.ui.navigation.CcodeNavHost
import com.consica.code.ui.navigation.Routes
import com.consica.code.ui.theme.CcodeTheme
import com.consica.code.util.ConnectivityObserver
import dagger.hilt.android.AndroidEntryPoint
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import javax.inject.Inject

@HiltViewModel
class AppViewModel @Inject constructor(
    prefs: UserPreferencesRepository,
    connectivityObserver: ConnectivityObserver,
) : ViewModel() {
    val onboardingComplete: StateFlow<Boolean?> = prefs.onboardingComplete
        .stateIn(viewModelScope, SharingStarted.Eagerly, null)

    val settings: StateFlow<AppSettings?> = prefs.settings
        .stateIn(viewModelScope, SharingStarted.Eagerly, null)

    val ageGroup: StateFlow<AgeGroup> = kotlinx.coroutines.flow.combine(
        prefs.profile, prefs.onboardingComplete,
    ) { profile, _ -> profile.ageGroup }
        .stateIn(viewModelScope, SharingStarted.Eagerly, AgeGroup.KIDS)

    val isOnline: StateFlow<Boolean> = connectivityObserver.isOnline
        .stateIn(viewModelScope, SharingStarted.Eagerly, true)
}

@AndroidEntryPoint
class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        val splash = installSplashScreen()
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        var ready = false
        splash.setKeepOnScreenCondition { !ready }

        setContent {
            val viewModel: AppViewModel = hiltViewModel()
            val onboardingComplete by viewModel.onboardingComplete.collectAsState()
            val settings by viewModel.settings.collectAsState()
            ready = onboardingComplete != null && settings != null
            if (!ready) return@setContent

            CcodeTheme(
                darkTheme = isSystemInDarkTheme(),
                highContrast = settings?.highContrast ?: false,
                reducedMotion = settings?.reducedMotion ?: false,
            ) {
                AppContent(
                    viewModel = viewModel,
                    startDestination = if (onboardingComplete == true) Routes.MAP else Routes.ONBOARDING,
                )
            }
        }
    }
}

@Composable
private fun AppContent(
    viewModel: AppViewModel,
    startDestination: String,
) {
    val navController = rememberNavController()
    val isOnline by viewModel.isOnline.collectAsState()
    val ageGroup by viewModel.ageGroup.collectAsState()

    var offlineToastVisible by remember { mutableStateOf(false) }
    var wasOnline by remember { mutableStateOf(isOnline) }
    LaunchedEffect(isOnline) {
        if (wasOnline && !isOnline) offlineToastVisible = true
        wasOnline = isOnline
    }

    Box(Modifier.fillMaxSize()) {
        CcodeNavHost(navController = navController, startDestination = startDestination)
        TerraToast(
            text = stringResource(CharacterGuide.messageFor(GuideTrigger.OFFLINE, ageGroup)),
            expression = TerraExpression.HAPPY,
            visible = offlineToastVisible,
            onDismiss = { offlineToastVisible = false },
            modifier = Modifier
                .align(Alignment.TopCenter)
                .statusBarsPadding()
                .padding(12.dp),
        )
    }
}
