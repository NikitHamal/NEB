package com.neb.ians.ui.screens.profile

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.UserProfileResponse
import com.neb.ians.ui.components.compactCount

// ---------------------------------------------------------------------------
// The About tab.
//
// Four bordered cards became four labelled lists. The progress card is gone
// entirely: it drew three bars that were hard-coded to zero, so it told every
// visitor the same untrue thing. What is left is only what the server
// actually knows about this person.
// ---------------------------------------------------------------------------

private val AboutIndent = 20.dp

@Composable
fun ProfileAbout(
    profile: UserProfileResponse,
    followerCount: Int,
    repliesCount: Int,
    resourcesCount: Int,
    modifier: Modifier = Modifier
) {
    val details = remember(profile) { buildDetails(profile) }

    Column(modifier = modifier.fillMaxWidth()) {
        AboutSection("Activity") {
            AboutRow("Posts", compactCount(profile.postCount))
            AboutRow("Replies", compactCount(maxOf(repliesCount, profile.replyCount)))
            if (resourcesCount > 0) AboutRow("Resources", compactCount(resourcesCount))
            AboutRow("Followers", compactCount(followerCount))
            AboutRow("Following", compactCount(profile.followingCount))
            if (profile.likesReceivedCount > 0) {
                AboutRow("Likes received", compactCount(profile.likesReceivedCount))
            }
            if (profile.likesGivenCount > 0) {
                AboutRow("Likes given", compactCount(profile.likesGivenCount))
            }
            if (profile.contributionScore > 0) {
                AboutRow("Contribution score", compactCount(profile.contributionScore))
            }
        }

        if (details.isNotEmpty()) {
            Spacer(modifier = Modifier.height(22.dp))
            AboutSection("Details") {
                details.forEach { (label, value) -> AboutRow(label, value) }
            }
        }

        Spacer(modifier = Modifier.height(28.dp))
    }
}

@Composable
private fun AboutSection(label: String, content: @Composable () -> Unit) {
    Column(modifier = Modifier.fillMaxWidth()) {
        Text(
            text = label.uppercase(),
            style = MaterialTheme.typography.labelSmall,
            fontWeight = FontWeight.SemiBold,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.padding(start = AboutIndent, bottom = 4.dp)
        )
        content()
    }
}

@Composable
private fun AboutRow(label: String, value: String) {
    if (value.isBlank()) return
    val scheme = MaterialTheme.colorScheme
    Column(modifier = Modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = AboutIndent, vertical = 11.dp),
            verticalAlignment = Alignment.Top,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                text = label,
                style = MaterialTheme.typography.bodyMedium,
                color = scheme.onSurfaceVariant
            )
            Spacer(modifier = Modifier.width(20.dp))
            Text(
                text = value,
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.Medium,
                color = scheme.onSurface,
                textAlign = TextAlign.End,
                modifier = Modifier.weight(1f, fill = false)
            )
        }
        HorizontalDivider(
            color = scheme.outlineVariant.copy(alpha = 0.5f),
            modifier = Modifier.padding(start = AboutIndent)
        )
    }
}

/** Only the fields this person actually filled in, in reading order. */
private fun buildDetails(p: UserProfileResponse): List<Pair<String, String>> {
    val rows = mutableListOf<Pair<String, String>>()

    fun add(label: String, value: String?) {
        val v = value?.trim().orEmpty()
        if (v.isNotBlank()) rows.add(label to v)
    }

    when (p.role) {
        "teacher" -> {
            add("Role", if (p.verificationLevel > 0) "Verified teacher" else "Teacher")
            add("Teaches", subjectList(p.teachingSubjects))
        }
        "institution" -> {
            add("Role", when (p.institutionType) {
                "school" -> "School"
                "college" -> "College"
                "academy" -> "Academy"
                else -> "Institution"
            })
        }
        "explorer" -> add("Role", "Explorer")
        else -> add("Class", classLabel(p.classLevel))
    }

    add("Subjects", subjectList(p.subjects))
    add("School", p.school)
    add("Location", profileLocation(p))
    add("Gender", p.gender?.replaceFirstChar { it.uppercase() })
    if (p.moderatorLevel > 0) {
        add("Moderator", when (p.moderatorLevel) {
            1 -> "Community mod"
            2 -> "Senior mod"
            else -> "Community lead"
        })
    }
    add("Joined", formatJoined(p.createdAt).removePrefix("Joined "))
    if (p.isLocked == 1) add("Account", "Private")

    return rows
}
