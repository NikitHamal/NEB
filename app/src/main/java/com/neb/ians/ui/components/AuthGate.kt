package com.neb.ians.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.EditNote
import androidx.compose.material.icons.outlined.FavoriteBorder
import androidx.compose.material.icons.outlined.Lock
import androidx.compose.material.icons.outlined.Notifications
import androidx.compose.material.icons.outlined.Person
import androidx.compose.material.icons.outlined.PersonAdd
import androidx.compose.material.icons.outlined.Upload
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp

/** Why the app is asking a guest to sign in. Drives the one line the sheet shows. */
enum class GateReason(val title: String, val body: String, val icon: ImageVector) {
    Generic("Sign in to continue", "Create a free account or sign in to use this.", Icons.Outlined.Lock),
    Reply("Sign in to reply", "Join the discussion with your NEBians account.", Icons.Outlined.ChatBubbleOutline),
    Like("Sign in to react", "Your account keeps your likes and votes.", Icons.Outlined.FavoriteBorder),
    Save("Sign in to save", "Saved items follow you across devices.", Icons.Outlined.BookmarkBorder),
    Post("Sign in to post", "Ask, share and help other students.", Icons.Outlined.EditNote),
    Follow("Sign in to follow", "Follow people to fill your feed with them.", Icons.Outlined.PersonAdd),
    Upload("Sign in to upload", "Share resources and earn credit for them.", Icons.Outlined.Upload),
    Notifications("Sign in for alerts", "Replies, mentions and results show up here.", Icons.Outlined.Notifications),
    Profile("Sign in to see your profile", "Your profile, notes and progress live here.", Icons.Outlined.Person),
}

/**
 * The one door every protected action goes through. A signed-in user runs the action at once;
 * a guest gets the sign-in sheet and stays on the screen they were on.
 */
class AuthGate(
    val signedIn: Boolean,
    private val prompt: (GateReason) -> Unit,
) {
    fun require(reason: GateReason = GateReason.Generic, action: () -> Unit) {
        if (signedIn) action() else prompt(reason)
    }

    fun ask(reason: GateReason = GateReason.Generic) = prompt(reason)
}

/** Default is permissive so previews and tests never get stuck behind a sheet. */
val LocalAuthGate = staticCompositionLocalOf { AuthGate(true) { } }

@Composable
fun SignInSheet(
    reason: GateReason,
    onSignIn: () -> Unit,
    onDismiss: () -> Unit,
) {
    NebModalSheet(onDismiss = onDismiss) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 12.dp)
                .navigationBarsPadding(),
            verticalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            Surface(
                shape = CircleShape,
                color = MaterialTheme.colorScheme.primaryContainer,
                contentColor = MaterialTheme.colorScheme.onPrimaryContainer,
                modifier = Modifier.size(52.dp),
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(reason.icon, contentDescription = null, modifier = Modifier.size(26.dp))
                }
            }
            Spacer(Modifier.height(8.dp))
            Text(reason.title, style = MaterialTheme.typography.headlineSmall)
            Text(
                reason.body,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Spacer(Modifier.height(14.dp))
            NebButton(text = "Sign in or sign up", onClick = onSignIn, fillWidth = true)
            NebButton(
                text = "Not now",
                onClick = onDismiss,
                tone = NebButtonTone.Text,
                fillWidth = true,
            )
        }
    }
}

/** Stands in for the reply composer while signed out; one tap opens the sheet. */
@Composable
fun GuestReplyBar(onClick: () -> Unit, modifier: Modifier = Modifier, label: String = "Sign in to reply") {
    Surface(
        onClick = onClick,
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 12.dp, vertical = 8.dp),
        shape = RoundedCornerShape(28.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLow,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 18.dp, vertical = 14.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Icon(
                Icons.Outlined.Lock,
                contentDescription = null,
                modifier = Modifier.size(18.dp),
                tint = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Text(
                label,
                style = MaterialTheme.typography.bodyLarge,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.weight(1f),
            )
            Text(
                "Sign in",
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.primary,
            )
        }
    }
}

/** A full-screen stand-in for a tab that only makes sense signed in (profile, notifications). */
@Composable
fun GuestPlaceholder(reason: GateReason, onSignIn: () -> Unit, modifier: Modifier = Modifier) {
    Column(
        modifier = modifier
            .fillMaxWidth()
            .padding(32.dp)
            .clip(RoundedCornerShape(28.dp))
            .clickable(onClick = onSignIn),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(10.dp),
    ) {
        Icon(reason.icon, null, modifier = Modifier.size(40.dp), tint = MaterialTheme.colorScheme.primary)
        Text(reason.title, style = MaterialTheme.typography.titleLarge)
        Text(
            reason.body,
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        NebButton(text = "Sign in", onClick = onSignIn)
    }
}
