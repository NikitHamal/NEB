@file:OptIn(
    androidx.compose.material3.ExperimentalMaterial3Api::class,
    androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class
)

package com.neb.ians.ui.screens.marketplace

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyListScope
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Verified
import androidx.compose.material.icons.outlined.CheckCircle
import androidx.compose.material.icons.outlined.ErrorOutline
import androidx.compose.material.icons.outlined.HourglassTop
import androidx.compose.material.icons.outlined.Lock
import androidx.compose.material.icons.outlined.School
import androidx.compose.material.icons.outlined.Storefront
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import coil.compose.AsyncImage
import com.neb.ians.data.api.ApiMarketplaceCourseDetail
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebLoader
import com.neb.ians.ui.components.WebCardShape
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.nebBorderSubtle
import com.neb.ians.ui.screens.resource.ResourcePurchaseSheet
import com.neb.ians.util.rememberTactileFeedback
import com.neb.ians.util.TactileType
import kotlinx.coroutines.flow.collectLatest

/**
 * One offering, and the same QR checkout a paid library resource uses.
 *
 * The sheet is literally the resource purchase sheet — one verification flow,
 * one set of words about it, whichever kind of thing is being bought.
 */
@Composable
fun MarketplaceCourseScreen(
    onNavigateBack: () -> Unit,
    onCreatorClick: (String) -> Unit,
    onResourceClick: (String) -> Unit,
    onSignInRequired: () -> Unit,
    viewModel: MarketplaceCourseViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val purchaseSubmitting by viewModel.purchaseSubmitting.collectAsStateWithLifecycle()
    val purchaseSheetVisible by viewModel.purchaseSheetVisible.collectAsStateWithLifecycle()
    val snackbarMessage by viewModel.snackbarMessage.collectAsStateWithLifecycle()
    val tactile = rememberTactileFeedback()
    var transientMessage by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(Unit) { viewModel.load() }
    LaunchedEffect(snackbarMessage) {
        if (!snackbarMessage.isNullOrBlank()) {
            transientMessage = snackbarMessage
            viewModel.clearSnackbar()
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text(
                            text = uiState.course?.title ?: "Offering",
                            fontWeight = FontWeight.SemiBold,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                        uiState.course?.page?.let { page ->
                            Text(
                                text = page.displayName,
                                style = MaterialTheme.typography.labelMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                maxLines = 1
                            )
                        }
                    }
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { padding ->
        val course = uiState.course
        when {
            uiState.isLoading && course == null ->
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(padding),
                    contentAlignment = Alignment.Center
                ) { NebLoader() }

            uiState.error != null && course == null ->
                Box(modifier = Modifier.fillMaxSize().padding(padding)) {
                    ErrorCard(
                        message = uiState.error ?: "Something went wrong",
                        onRetry = viewModel::load,
                        modifier = Modifier.padding(16.dp)
                    )
                }

            course == null ->
                Box(modifier = Modifier.fillMaxSize().padding(padding)) {
                    NebEmptyState(
                        icon = Icons.Outlined.Storefront,
                        title = "This offering is not available",
                        subtitle = "Its creator may have unpublished it."
                    )
                }

            else -> {
                val accent = creatorAccent(course.page?.accentHex ?: "#1F2937")
                LazyColumn(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(padding),
                    contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 8.dp, bottom = 120.dp),
                    verticalArrangement = Arrangement.spacedBy(14.dp)
                ) {
                    item(key = "hero") { CourseHero(course, accent) }
                    if (course.description.isNotBlank()) {
                        item(key = "about") {
                            CourseSection("About this offering") {
                                Text(
                                    text = course.description,
                                    style = MaterialTheme.typography.bodyMedium,
                                    color = MaterialTheme.colorScheme.onSurface
                                )
                            }
                        }
                    }
                    if (course.includes.isNotEmpty()) {
                        item(key = "includes") {
                            CourseSection("What's included") {
                                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                    course.includes.forEach { entry ->
                                        Row(
                                            verticalAlignment = Alignment.CenterVertically,
                                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                                        ) {
                                            Icon(
                                                imageVector = Icons.Filled.Check,
                                                contentDescription = null,
                                                tint = accent,
                                                modifier = Modifier.size(17.dp)
                                            )
                                            Text(entry, style = MaterialTheme.typography.bodyMedium)
                                        }
                                    }
                                }
                            }
                        }
                    }
                    if (uiState.courseResources.isNotEmpty()) {
                        item(key = "material") {
                            CourseSection("Course material") {
                                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                    uiState.courseResources.forEach { resource ->
                                        Row(
                                            modifier = Modifier
                                                .fillMaxWidth()
                                                .clip(WebCardShape)
                                                .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                                                .clickable {
                                                    tactile.perform(TactileType.LightTap)
                                                    onResourceClick(resource.id)
                                                }
                                                .padding(12.dp),
                                            verticalAlignment = Alignment.CenterVertically,
                                            horizontalArrangement = Arrangement.spacedBy(10.dp)
                                        ) {
                                            Text(
                                                text = resource.title,
                                                style = MaterialTheme.typography.bodyMedium,
                                                modifier = Modifier.weight(1f),
                                                maxLines = 1,
                                                overflow = TextOverflow.Ellipsis
                                            )
                                            // Buying the course covers its material, so the
                                            // chip says so instead of quoting a second price.
                                            if (resource.isPaid) {
                                                Surface(
                                                    shape = WebPillShape,
                                                    color = MaterialTheme.colorScheme.surfaceContainerHigh
                                                ) {
                                                    Text(
                                                        text = if (course.hasAccess) "Included"
                                                               else "Rs. ${resource.price.ifBlank { "0" }}",
                                                        style = MaterialTheme.typography.labelSmall,
                                                        fontWeight = FontWeight.SemiBold,
                                                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                                                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp)
                                                    )
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                    item(key = "buy") {
                        CourseBuyPanel(
                            course = course,
                            accent = accent,
                            isOwner = uiState.isOwner,
                            canCheckout = uiState.isAuthenticated,
                            isRefreshing = uiState.isSubmittingPurchase,
                            onBuy = {
                                if (uiState.isAuthenticated) {
                                    tactile.perform(TactileType.ButtonTap)
                                    viewModel.openPurchaseSheet()
                                } else {
                                    onSignInRequired()
                                }
                            },
                            onCreatorClick = onCreatorClick
                        )
                    }
                }
            }
        }
    }

    if (purchaseSheetVisible && uiState.course != null) {
        val course = uiState.course!!
        ResourcePurchaseSheet(
            price = course.price.ifBlank { "0" },
            sellerName = course.page?.displayName?.ifBlank { "the creator" } ?: "the creator",
            purchaseStatus = course.purchaseStatus,
            submitting = purchaseSubmitting,
            isAuthenticated = uiState.isAuthenticated,
            onDismiss = { viewModel.dismissPurchaseSheet() },
            onSubmit = { transactionId, proofFile -> viewModel.submitPurchase(transactionId, proofFile) },
            onSignInPrompt = {
                viewModel.dismissPurchaseSheet()
                onSignInRequired()
            }
        )
    }

    transientMessage?.let { message ->
        LaunchedEffect(message) {
            kotlinx.coroutines.delay(2600)
            transientMessage = null
        }
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(20.dp),
            contentAlignment = Alignment.BottomCenter
        ) {
            Surface(
                shape = WebPillShape,
                color = MaterialTheme.colorScheme.surfaceContainerHigh
            ) {
                Text(
                    text = message,
                    style = MaterialTheme.typography.bodySmall,
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 10.dp)
                )
            }
        }
    }
}

@Composable
private fun CourseHero(course: ApiMarketplaceCourseDetail, accent: Color) {
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(180.dp)
                .clip(WebPanelShape)
                .background(MaterialTheme.colorScheme.surfaceContainerHigh)
        ) {
            if (course.coverUrl.isNotBlank()) {
                AsyncImage(
                    model = course.coverUrl,
                    contentDescription = null,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )
            }
        }
        Text(
            text = if (course.isFree) "FREE OFFERING" else "PAID OFFERING",
            style = MaterialTheme.typography.labelSmall,
            fontWeight = FontWeight.Bold,
            color = accent
        )
        Text(
            text = course.title,
            style = MaterialTheme.typography.headlineSmall,
            fontWeight = FontWeight.SemiBold
        )
        if (course.summary.isNotBlank()) {
            Text(
                text = course.summary,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
            listOfNotNull(
                course.level.takeIf { it.isNotBlank() },
                course.durationLabel.takeIf { it.isNotBlank() },
                course.lessonCount.takeIf { it > 0 }?.let { "$it lessons" },
                course.seatLimit.takeIf { it > 0 }?.let { "$it seats" }
            ).take(3).forEach { chip ->
                Surface(shape = WebPillShape, color = MaterialTheme.colorScheme.surfaceContainer) {
                    Text(
                        text = chip,
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.padding(horizontal = 9.dp, vertical = 3.dp)
                    )
                }
            }
        }
    }
}

@Composable
private fun CourseSection(title: String, content: @Composable () -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Text(
            text = title,
            style = MaterialTheme.typography.titleMediumEmphasized,
            fontWeight = FontWeight.SemiBold
        )
        content()
        HorizontalDivider(color = nebBorderSubtle(), thickness = 1.dp)
    }
}

@Composable
private fun CourseBuyPanel(
    course: ApiMarketplaceCourseDetail,
    accent: Color,
    isOwner: Boolean,
    canCheckout: Boolean,
    isRefreshing: Boolean,
    onBuy: () -> Unit,
    onCreatorClick: (String) -> Unit
) {
    val shape = WebPanelShape
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(shape)
            .background(MaterialTheme.colorScheme.surfaceContainerLow)
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = if (course.isFree) "Free" else "Rs. ${course.price.ifBlank { "0" }}",
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = if (course.isFree) "No payment needed" else "One-time payment",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            course.page?.let { page ->
                Row(
                    modifier = Modifier
                        .clip(WebPillShape)
                        .clickable {
                            if (page.slug.isNotBlank()) onCreatorClick(page.slug)
                        }
                        .padding(horizontal = 8.dp, vertical = 4.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    Icon(
                        imageVector = Icons.Outlined.School,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.size(15.dp)
                    )
                    Text(
                        text = page.displayName,
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    if (page.verified) {
                        Icon(
                            imageVector = Icons.Filled.Verified,
                            contentDescription = null,
                            tint = accent,
                            modifier = Modifier.size(13.dp)
                        )
                    }
                }
            }
        }

        when {
            isOwner -> Text(
                text = "You own this offering. Manage it in your studio.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )

            course.hasAccess -> AccessState(
                icon = Icons.Outlined.CheckCircle,
                title = "Unlocked",
                detail = when (course.accessReason) {
                    "purchased" -> "Your payment was verified."
                    "free" -> "Free for every Nebian."
                    else -> "You already have access."
                },
                accent = accent
            )

            else -> {
                if (course.purchaseStatus == "pending") {
                    AccessState(
                        icon = Icons.Outlined.HourglassTop,
                        title = "Awaiting verification",
                        detail = "We received your payment. Access unlocks as soon as our team approves it.",
                        accent = accent
                    )
                } else if (course.purchaseStatus == "rejected") {
                    AccessState(
                        icon = Icons.Outlined.ErrorOutline,
                        title = "Payment not verified",
                        detail = "Check the reference and submit again.",
                        accent = MaterialTheme.colorScheme.error
                    )
                }

                Text(
                    text = "Pay Rs. ${course.price.ifBlank { "0" }} to the NEBians QR, then submit the transaction ID or a screenshot. Access unlocks after verification.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )

                if (course.isFree) {
                    NebButton(
                        text = "Open",
                        onClick = onBuy,
                        icon = Icons.Outlined.School,
                        tone = NebButtonTone.Primary,
                        size = NebButtonSize.Small,
                        fillWidth = true
                    )
                } else {
                    NebButton(
                        text = if (canCheckout) "Buy this offering" else "Sign in to buy",
                        onClick = onBuy,
                        icon = Icons.Outlined.Lock,
                        tone = NebButtonTone.Primary,
                        size = NebButtonSize.Feature,
                        fillWidth = true,
                        loading = isRefreshing
                    )
                }
            }
        }
    }
}

@Composable
private fun AccessState(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    title: String,
    detail: String,
    accent: Color
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(WebCardShape)
            .background(MaterialTheme.colorScheme.surfaceContainerLowest)
            .padding(12.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Icon(icon, contentDescription = null, tint = accent, modifier = Modifier.size(20.dp))
        Column {
            Text(title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
            Text(
                text = detail,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}
