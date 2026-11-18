package com.neb.ians.ui.screens.profile

import androidx.compose.foundation.clickable
import com.neb.ians.ui.components.nebHorizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyListScope
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Dashboard
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.UserProfileResponse
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.WebResourceCard

/** Tab indices of the profile rail. Overview first, as in the Profile v3 concept. */
internal object ProfileTab {
    const val OVERVIEW = 0
    const val POSTS = 1
    const val REPLIES = 2
    const val RESOURCES = 3
    const val ABOUT = 4
}

/** A section title with a "See all" link that jumps to the tab that holds the rest. */
@Composable
private fun OverviewHead(title: String, count: Int? = null, onSeeAll: (() -> Unit)? = null) {
    val scheme = MaterialTheme.colorScheme
    Row(
        Modifier.fillMaxWidth().padding(horizontal = 20.dp).padding(top = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold,
            color = scheme.onSurface, modifier = Modifier.weight(1f)
        )
        if (count != null && count > 0) {
            Text(count.toString(), maxLines = 1, style = MaterialTheme.typography.labelLarge, color = scheme.onSurfaceVariant)
        }
        if (onSeeAll != null) {
            Box(
                Modifier.padding(start = 8.dp).heightIn(min = 44.dp).clip(RoundedCornerShape(14.dp))
                    .clickable(onClick = onSeeAll).padding(horizontal = 8.dp),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    "See all", style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold,
                    color = scheme.primary
                )
            }
        }
    }
}

/**
 * Overview: the person at a glance. Strength (own page), the three tonal tiles, Studying now, the latest post,
 * a rail of resources, achievements and portfolio. It only summarises and links; every list lives in its own tab.
 */
internal fun LazyListScope.overviewTab(
    profile: UserProfileResponse,
    isSelf: Boolean,
    uiState: ProfileUiState,
    onEditProfile: () -> Unit,
    onPostClick: (String) -> Unit,
    onResourceClick: (String) -> Unit,
    onProfileClick: (String) -> Unit,
    onTabSelected: (Int) -> Unit
) {
    val firstPost = uiState.posts.firstOrNull()
    val rail: List<ApiResource> = uiState.resources.take(6)
    val hasPortfolio = profile.role != "institution"
    val hasTiles = uiState.glance.isNotEmpty() || uiState.studying != null

    if (isSelf) item(key = "ov_strength") { OverviewSlot { ProfileStrengthCard(profile = profile, onEditProfile = onEditProfile) } }

    if (hasTiles) item(key = "ov_tiles") {
        Column(Modifier.padding(vertical = 6.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
            ProfileGlance(uiState.glance)
            uiState.studying?.let { ProfileStudyingNow(it, onOpenPost = onPostClick) }
        }
    }

    if (firstPost != null) {
        item(key = "ov_post_head") { OverviewHead("Latest post", onSeeAll = { onTabSelected(ProfileTab.POSTS) }) }
        item(key = "ov_post") { OverviewSlot { ProfilePostCard(post = firstPost, onClick = { onPostClick(firstPost.id) }) } }
    }

    if (rail.isNotEmpty()) {
        item(key = "ov_res_head") {
            OverviewHead("Resources", uiState.resourcesCount.takeIf { it > 0 }, onSeeAll = { onTabSelected(ProfileTab.RESOURCES) })
        }
        item(key = "ov_res") {
            Row(
                Modifier.nebHorizontalScroll(rememberScrollState()).padding(horizontal = 16.dp, vertical = 6.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                rail.forEach { r ->
                    Box(Modifier.width(264.dp)) { WebResourceCard(resource = r, onClick = { onResourceClick(r.id) }, minWidth = null) }
                }
            }
        }
    }

    item(key = "ov_achievements") { OverviewSlot { AboutAchievementsCard(profile = profile) } }

    if (hasPortfolio) item(key = "ov_portfolio") {
        OverviewSlot { ProfilePortfolioCard(profile = profile, isSelf = isSelf, onEditProfile = onEditProfile) }
    }

    if (!hasTiles && firstPost == null && rail.isEmpty() && !isSelf) item(key = "ov_empty") {
        NebEmptyState(icon = Icons.Outlined.Dashboard, title = "Nothing to show yet", subtitle = null)
    }
}

@Composable
private fun OverviewSlot(content: @Composable () -> Unit) {
    Box(Modifier.padding(horizontal = 16.dp, vertical = 6.dp)) { content() }
}
