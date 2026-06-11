package com.consica.code.ui.screens.rewards

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.consica.code.data.prefs.UserPreferencesRepository
import com.consica.code.data.repository.ProgressRepository
import com.consica.code.domain.model.PlayerStats
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import java.time.LocalDate
import javax.inject.Inject

data class RewardsUiState(
    val stats: PlayerStats = PlayerStats(),
    val earnedBadgeIds: Set<String> = emptySet(),
    val unlockedItemIds: Set<String> = emptySet(),
    val activeEpochDays: Set<Long> = emptySet(),
    val activeToday: Boolean = false,
)

@HiltViewModel
class RewardsViewModel @Inject constructor(
    prefs: UserPreferencesRepository,
    progressRepository: ProgressRepository,
) : ViewModel() {

    val uiState: StateFlow<RewardsUiState> = combine(
        prefs.stats,
        progressRepository.earnedBadges,
        progressRepository.ecosystemItems,
        progressRepository.streakDays,
    ) { stats, badges, items, days ->
        val dayset = days.map { it.epochDay }.toSet()
        RewardsUiState(
            stats = stats,
            earnedBadgeIds = badges.map { it.badgeId }.toSet(),
            unlockedItemIds = items.map { it.itemId }.toSet(),
            activeEpochDays = dayset,
            activeToday = LocalDate.now().toEpochDay() in dayset,
        )
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), RewardsUiState())
}
