package com.neb.ians.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.ReadOnlyComposable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.luminance
import androidx.compose.runtime.Immutable

// ---------------------------------------------------------------------------
// The NEBians palette, and everything built on top of it.
//
// The ramps and the role values are no longer here. They are generated, for
// this app and for the website at the same time, by
//
//     tools/design/palette.py
//
// into Palette.kt next door -- which is where NebNeutral, NebBrandRamp,
// NebSteel, NebVioletRamp and every md_theme_* value now live. That script also
// refuses to emit either file unless a contrast audit passes, which is how the
// hairline that used to sit at 1.16:1 against the page is now held above 1.55
// on both platforms at once.
//
// What stays here is the part that is judgement rather than arithmetic: how a
// subject is dressed, what family an unknown subject belongs to, and the accent
// set the create menu picks from.
//
// Three families, and a rule for each.
//
//   Brand   the blue. Primary, links, selection, the create button -- anything
//           the user is meant to press or has just chosen. One hue, so pressing
//           always looks the same.
//   Steel   the blue's quieter relative, for secondary surfaces that should
//           belong to the brand without competing with it.
//   Violet  tertiary. Spent on the few places that need a third voice.
//
// What has NOT come back is hue as information. A subject still reads by its
// icon and its words first; the tint below is decoration on top of a label that
// already works in grey. And the sign-in journey's illustrations stay strictly
// ink-on-paper -- see NebAuthPalette, where the art ramp is deliberately
// neutral.
// ---------------------------------------------------------------------------

/**
 * The brand blue, for the rare caller that has no composition to read a scheme
 * from. Prefer `MaterialTheme.colorScheme.primary` everywhere else -- it flips
 * with the theme and this does not.
 */
val NebBrandBlue: Color = NebBrandRamp.B40

/** The brand blue as it must appear on a dark surface. */
val NebBrandBlueOnDark: Color = NebBrandRamp.B80

/** The brand blue resolved against whatever surface the caller is sitting on. */
@Composable
@ReadOnlyComposable
fun nebBrand(): Color =
    if (MaterialTheme.colorScheme.surface.luminance() < 0.5f) NebBrandBlueOnDark else NebBrandBlue

/**
 * The third text tier: placeholders, timestamps, disabled labels.
 *
 * Material's scheme stops at onSurfaceVariant, so everything quieter than
 * secondary text used to be onSurfaceVariant at some alpha -- which is how a
 * timestamp ended up at 2.31:1 in the light theme. This is a real colour,
 * audited like the rest, and it clears 3.2:1 on every surface.
 */
@Composable
@ReadOnlyComposable
fun nebOnSurfaceTertiary(): Color =
    if (MaterialTheme.colorScheme.surface.luminance() < 0.5f) md_theme_dark_onSurfaceTertiary
    else md_theme_light_onSurfaceTertiary

/**
 * How a subject, category or level is dressed.
 *
 * The tint is a second cue, never the only one. Every place that reads this also
 * shows the subject's icon and its name, which is what the user actually reads —
 * so nobody has to learn that teal means Biology. Unknown subjects fall back to
 * the brand, which is why the map needs no default entry per screen.
 */
data class SubjectTheme(
    val color: Color,
    val container: Color,
    val onContainer: Color
)

private data class SubjectHue(
    val light: Color,
    val lightContainer: Color,
    val onLightContainer: Color,
    val dark: Color,
    val darkContainer: Color,
    val onDarkContainer: Color
)

/**
 * One entry per subject the curriculum actually has. Light values are the web's
 * subject classes; dark values are the same hue lifted into the range that stays
 * legible on navy, because the light ones do not.
 */
private val SubjectHues: Map<String, SubjectHue> = mapOf(
    "Physics" to SubjectHue(
        Color(0xFF1D4ED8), Color(0xFFDBE7FE), Color(0xFF1B3FA8),
        Color(0xFF9DBBFF), Color(0xFF1B2A4D), Color(0xFFD6E3FF)
    ),
    "Chemistry" to SubjectHue(
        Color(0xFF15803D), Color(0xFFDCFCE7), Color(0xFF14602F),
        Color(0xFF7CD9A0), Color(0xFF14301F), Color(0xFFD3F5DF)
    ),
    "Mathematics" to SubjectHue(
        Color(0xFFB91C1C), Color(0xFFFEE2E2), Color(0xFF8F1717),
        Color(0xFFFF9C93), Color(0xFF3A1A18), Color(0xFFFFDAD6)
    ),
    "Biology" to SubjectHue(
        Color(0xFF0F766E), Color(0xFFCCFBF1), Color(0xFF0C5B55),
        Color(0xFF5FD3C4), Color(0xFF10302D), Color(0xFFCDF3ED)
    ),
    "English" to SubjectHue(
        Color(0xFF7E22CE), Color(0xFFF3E8FF), Color(0xFF631AA3),
        Color(0xFFD3B4FE), Color(0xFF2C1A44), Color(0xFFEDE0FF)
    ),
    "Nepali" to SubjectHue(
        Color(0xFF9A6206), Color(0xFFFEF3C7), Color(0xFF7A4E05),
        Color(0xFFE8B457), Color(0xFF32260E), Color(0xFFF7E6C2)
    ),
    "Computer Science" to SubjectHue(
        Color(0xFF0E7490), Color(0xFFCFFAFE), Color(0xFF0B5A70),
        Color(0xFF5CC8E0), Color(0xFF0E2C36), Color(0xFFC9EFF8)
    ),
    "Economics" to SubjectHue(
        Color(0xFFC2410C), Color(0xFFFFEDD5), Color(0xFF9A330A),
        Color(0xFFFFA76B), Color(0xFF3A2013), Color(0xFFFFE0CB)
    ),
    "Accountancy" to SubjectHue(
        Color(0xFF9D174D), Color(0xFFFCE7F3), Color(0xFF7D1240),
        Color(0xFFF79CC0), Color(0xFF3A1428), Color(0xFFFBDCE9)
    ),
    "Exam Tips" to SubjectHue(
        Color(0xFF6D28D9), Color(0xFFEDE9FE), Color(0xFF56209F),
        Color(0xFFC4B5FD), Color(0xFF261C46), Color(0xFFE6E0FF)
    )
)

private val BrandSubjectHue = SubjectHue(
    NebBrandRamp.B40, NebBrandRamp.B90, NebBrandRamp.B10,
    NebBrandRamp.B80, NebSteel.S20, NebBrandRamp.B90
)

/**
 * The families a subject can belong to.
 *
 * [SubjectHues] is keyed by exact name, which was fine while the only subjects
 * that existed were the ten on that list. They are not. Upload accepts
 * "Physics - Technical Stream", "Microbiology", "Visual Programming" and
 * "सामाजिक अध्ययन", and the subject field on a resource is free text besides —
 * real uploads carry things like "Health and Physical Education" and
 * "Compulsory English". Every one of those used to fall through to the brand
 * blue, so a whole shelf of unrelated material came out looking identical.
 *
 * A family is the coarse answer: what *kind* of subject is this. It decides the
 * hue when the exact name is unknown, and it decides which set of banner
 * drawings a resource is allowed to be given. [GENERAL] is the honest answer
 * for a subject we cannot place, and it has its own abstract art set rather
 * than borrowing someone else's.
 */
enum class SubjectFamily {
    PHYSICS, CHEMISTRY, MATH, BIOLOGY, SCIENCE, LANGUAGE,
    COMPUTING, COMMERCE, SOCIAL, HEALTH, EXAM, GENERAL
}

/**
 * Ordered keyword table. Order is load-bearing in three places:
 *
 *   HEALTH before PHYSICS — "Physical Education" must not be read as physics.
 *   COMPUTING before SCIENCE — "Computer Science" is not a science subject here.
 *   SOCIAL before SCIENCE — "Social Studies" contains neither, but "Social
 *   Science" does, and it belongs with the maps.
 */
private val SubjectFamilyKeywords: List<Pair<SubjectFamily, List<String>>> = listOf(
    SubjectFamily.HEALTH to listOf(
        "health", "physical education", "phy. edu", "hpe", "sport", "fitness",
        "nutrition", "yoga", "स्वास्थ्य"
    ),
    SubjectFamily.EXAM to listOf(
        "exam tip", "exam prep", "entrance", "model paper", "model set",
        "past paper", "question bank", "mock test", "revision"
    ),
    SubjectFamily.COMPUTING to listOf(
        "computer", "software", "programming", "informatics", "information tech",
        "digital", "coding", "algorithm", "database", "web dev"
    ),
    SubjectFamily.PHYSICS to listOf("physics", "भौतिक"),
    SubjectFamily.CHEMISTRY to listOf("chemistry", "chemical", "रसायन"),
    SubjectFamily.MATH to listOf(
        "math", "algebra", "geometry", "trigonometry", "calculus", "statistic",
        "गणित"
    ),
    SubjectFamily.BIOLOGY to listOf(
        "biology", "botany", "zoology", "microbio", "anatomy", "genetic",
        "जीव"
    ),
    SubjectFamily.SOCIAL to listOf(
        "social", "history", "geography", "civic", "population", "culture",
        "सामाजिक", "अध्ययन"
    ),
    SubjectFamily.COMMERCE to listOf(
        "economic", "account", "business", "finance", "commerce", "marketing",
        "banking", "book keeping", "bookkeeping", "अर्थ"
    ),
    SubjectFamily.LANGUAGE to listOf(
        "english", "nepali", "literature", "grammar", "language", "sanskrit",
        "hindi", "maithili", "newari", "writing", "नेपाली", "अंग्रेजी", "साहित्य"
    ),
    SubjectFamily.SCIENCE to listOf(
        "science", "environment", "astronomy", "geology", "laboratory", "विज्ञान"
    )
)

/** The coarse kind of a subject. Free text in, one of twelve answers out. */
fun subjectFamily(subject: String): SubjectFamily {
    val s = subject.trim().lowercase()
    if (s.isEmpty()) return SubjectFamily.GENERAL
    for ((family, keywords) in SubjectFamilyKeywords) {
        for (keyword in keywords) {
            if (s.contains(keyword)) return family
        }
    }
    return SubjectFamily.GENERAL
}

/**
 * The hue a family falls back to when the exact subject name is not on the
 * list. Six of these are the canonical subject's own hue, so "Physics -
 * Technical Stream" comes out the same blue as "Physics" instead of brand blue.
 * The three that have no canonical subject — science, social, health — get
 * their own, chosen to sit clear of the ten already in use.
 */
private val SubjectFamilyHues: Map<SubjectFamily, SubjectHue> = mapOf(
    SubjectFamily.PHYSICS to SubjectHues.getValue("Physics"),
    SubjectFamily.CHEMISTRY to SubjectHues.getValue("Chemistry"),
    SubjectFamily.MATH to SubjectHues.getValue("Mathematics"),
    SubjectFamily.BIOLOGY to SubjectHues.getValue("Biology"),
    SubjectFamily.LANGUAGE to SubjectHues.getValue("English"),
    SubjectFamily.COMPUTING to SubjectHues.getValue("Computer Science"),
    SubjectFamily.COMMERCE to SubjectHues.getValue("Economics"),
    SubjectFamily.EXAM to SubjectHues.getValue("Exam Tips"),
    // Jade. Clear of Chemistry's forest green and Biology's teal.
    SubjectFamily.SCIENCE to SubjectHue(
        Color(0xFF047857), Color(0xFFD1FAE5), Color(0xFF04604A),
        Color(0xFF6EDCB4), Color(0xFF0D2E25), Color(0xFFCFF5E6)
    ),
    // Steel. Maps, civics and history read as slate, not as another warm hue.
    SubjectFamily.SOCIAL to SubjectHue(
        Color(0xFF3F5A8A), Color(0xFFDDE6F6), Color(0xFF2C4066),
        Color(0xFF9CB7E8), Color(0xFF1B2638), Color(0xFFD9E4F7)
    ),
    // Rose. Sits between Mathematics' brick red and Accountancy's magenta, and
    // is the one hue a pulse line can be drawn in without looking like an error.
    SubjectFamily.HEALTH to SubjectHue(
        Color(0xFFBE123C), Color(0xFFFFE4E9), Color(0xFF8F0E2E),
        Color(0xFFFF9BB0), Color(0xFF3D1520), Color(0xFFFFD9E1)
    ),
    SubjectFamily.GENERAL to BrandSubjectHue
)

private fun subjectHue(subject: String): SubjectHue =
    SubjectHues[subject]
        ?: SubjectHues.entries.firstOrNull { it.key.equals(subject, ignoreCase = true) }?.value
        ?: SubjectFamilyHues[subjectFamily(subject)]
        ?: BrandSubjectHue

@Composable
@ReadOnlyComposable
fun getSubjectTheme(subject: String): SubjectTheme {
    val hue = subjectHue(subject)
    return if (MaterialTheme.colorScheme.surface.luminance() < 0.5f) {
        SubjectTheme(hue.dark, hue.darkContainer, hue.onDarkContainer)
    } else {
        SubjectTheme(hue.light, hue.lightContainer, hue.onLightContainer)
    }
}

@Composable
@ReadOnlyComposable
fun getSubjectColor(subject: String): Color = getSubjectTheme(subject).color

/**
 * The brand where there is no composition to read it from — a media
 * notification, a service, a value cached in a view model. The brand blue rather
 * than a subject's own hue, because whatever reads this cannot know which
 * surface it will be drawn on and the blue is the one that holds up on both.
 */
val SubjectAccentStatic: Color = NebBrandRamp.B40

fun subjectAccentArgb(): Long = 0xFF004AC6L

// ---------------------------------------------------------------------------
// Accents.
//
// The brand blue is the voice of action and the ramp carries the page. These
// hues are for the places where several choices sit side by side and the user is
// picking between them rather than reading them — the create menu is the case
// that asked for them, and the resource actions followed.
//
// Each carries a light and a dark value so the contrast holds either way, and
// none of them is load-bearing: nothing is knowable only by its hue.
// ---------------------------------------------------------------------------

@Immutable
data class NebAccent(val light: Color, val dark: Color)

object NebAccents {
    /** The brand itself, for the accent slot that should read as "the app". */
    val Brand = NebAccent(Color(0xFF004AC6), Color(0xFFB4C5FF))
    val Indigo = NebAccent(Color(0xFF4F46E5), Color(0xFFB4B0FF))
    val Violet = NebAccent(Color(0xFF7C3AED), Color(0xFFC9B6FE))
    val Amber = NebAccent(Color(0xFF9A6206), Color(0xFFE8B457))
    val Teal = NebAccent(Color(0xFF0F766E), Color(0xFF5FD3C4))
    val Green = NebAccent(Color(0xFF15803D), Color(0xFF7CD9A0))
    val Cyan = NebAccent(Color(0xFF0E7490), Color(0xFF5CC8E0))
    val Rose = NebAccent(Color(0xFFB3261E), Color(0xFFFF9186))
    val Pink = NebAccent(Color(0xFF9D174D), Color(0xFFF79CC0))
}

@Composable
fun NebAccent.resolve(): Color =
    if (MaterialTheme.colorScheme.surface.luminance() < 0.5f) dark else light
