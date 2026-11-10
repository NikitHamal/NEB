@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class, androidx.compose.material3.ExperimentalMaterial3Api::class)

package com.neb.ians.ui.screens.about

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Build
import androidx.compose.animation.core.Animatable
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.AutoAwesome
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.Code
import androidx.compose.material.icons.outlined.Forum
import androidx.compose.material.icons.outlined.LocalLibrary
import androidx.compose.material.icons.outlined.Memory
import androidx.compose.material.icons.outlined.Mic
import androidx.compose.material.icons.outlined.RecordVoiceOver
import androidx.compose.material.icons.outlined.Smartphone
import androidx.compose.material3.ExperimentalMaterial3ExpressiveApi
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.layout.positionInRoot
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.core.content.pm.PackageInfoCompat
import androidx.graphics.shapes.RoundedPolygon
import com.neb.ians.R
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebGlyphShapes
import com.neb.ians.ui.components.NebIconButton
import com.neb.ians.ui.components.NebMorphBlob
import com.neb.ians.ui.components.NebTone
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.components.nebShape
import com.neb.ians.ui.components.nebToast
import com.neb.ians.ui.screens.onboarding.isDarkSurface
import com.neb.ians.ui.theme.nebAnimationsReduced
import com.neb.ians.ui.theme.nebSpatialSpec
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

/**
 * About: a poster, not a document.
 *
 * One scroll of plain content, no entrance or scroll-driven motion (a phone screen is small and a
 * list that animates while you flick it feels slow). The first screen is the poster: a big tonal
 * panel whose shape keeps changing behind the mark. Under it a bento of tiles, the version first,
 * then what NEBians is, who made it, and the open source work and on-device models it stands on.
 *
 * The story is the same as the web's /about/ (`web/about_data.py`).
 */
private class Pillar(val tone: NebTone, val shape: RoundedPolygon, val icon: ImageVector, val title: String, val text: String)
private class Step(val n: String, val title: String, val text: String)
private class Person(val name: String, val role: String, val tone: NebTone, val shape: RoundedPolygon)
private class Credit(val tone: NebTone, val shape: RoundedPolygon, val icon: ImageVector, val name: String, val by: String, val text: String)
private class Library(val name: String, val by: String, val license: String)

private val Pillars = listOf(
    Pillar(NebTone.Azure, NebGlyphShapes.Cookie, Icons.Outlined.LocalLibrary, "Library", "Notes, past papers and solved study books for every level."),
    Pillar(NebTone.Sky, NebGlyphShapes.Sunny, Icons.Outlined.Forum, "Forum", "Ask, and get answers marked correct, helpful or wrong."),
    Pillar(NebTone.Aqua, NebGlyphShapes.Flower, Icons.Outlined.AutoAwesome, "Neby", "A study helper that opens beside the page you read."),
    Pillar(NebTone.Peri, NebGlyphShapes.Clover, Icons.Outlined.Smartphone, "The app", "The same library, built for one-handed reading.")
)
private val Steps = listOf(
    Step("1", "Find", "Pick a level and a subject."),
    Step("2", "Read", "Open notes, papers and books in the reader."),
    Step("3", "Ask", "Post what you are stuck on."),
    Step("4", "Share", "Upload what helped you, so the next student finds it.")
)
private val Promises = listOf(
    "Free to read" to "No paywall in front of the library or the forum.",
    "Checked first" to "Moderators review every upload before it goes public.",
    "Every level" to "School to Master's, entrance included.",
    "Made for phones" to "Fast on a small screen and a slow connection."
)
private val Lead = Person("Nikit Hamal", "Lead developer", NebTone.Azure, NebGlyphShapes.Cookie)
private val Devs = listOf(
    Person("Prashant Chataut", "Developer", NebTone.Sky, NebGlyphShapes.Sunny),
    Person("Bikram Adhikari", "Developer", NebTone.Aqua, NebGlyphShapes.Flower)
)
private val Crew = listOf(
    Person("Utsab Kafle", "", NebTone.Peri, NebGlyphShapes.Clover),
    Person("Laxmi Nepal", "", NebTone.Sky, NebGlyphShapes.Gem),
    Person("Manisha Kafle", "", NebTone.Aqua, NebGlyphShapes.Burst),
    Person("Gaurav Rajbanshi", "", NebTone.Azure, NebGlyphShapes.Pentagon)
)

/** The models that run on the phone itself. Nothing is bundled: the user downloads them in Voice. */
private val Models = listOf(
    Credit(NebTone.Azure, NebGlyphShapes.Cookie, Icons.Outlined.Mic, "Whistle", "Cactus Compute", "Speech to text for dictation in Notes. Seven languages, runs offline."),
    Credit(NebTone.Sky, NebGlyphShapes.Sunny, Icons.Outlined.RecordVoiceOver, "Phonon 31m", "Gradium", "The voice that reads notes aloud, with the public Phonon voices. Apache-2.0."),
    Credit(NebTone.Aqua, NebGlyphShapes.Flower, Icons.Outlined.Memory, "Needle", "Cactus Compute", "The on-device engine Whistle runs on. Apache-2.0.")
)
private val Libraries = listOf(
    Library("Jetpack Compose, Material 3 Expressive", "Google", "Apache-2.0"),
    Library("Kotlin, Coroutines, Serialization", "JetBrains", "Apache-2.0"),
    Library("Room, Hilt, WorkManager, Media3", "Google", "Apache-2.0"),
    Library("Retrofit, OkHttp", "Square", "Apache-2.0"),
    Library("Coil", "Coil contributors", "Apache-2.0"),
    Library("Firebase Cloud Messaging, Google sign-in", "Google", "Terms apply"),
    Library("KaTeX", "Khan Academy and contributors", "MIT"),
    Library("Poppins", "Indian Type Foundry", "SIL OFL 1.1"),
    Library("Material Symbols and icons", "Google", "Apache-2.0")
)

@Composable
fun AboutScreen(onBack: () -> Unit, onOpenLibrary: () -> Unit) {
    val scheme = MaterialTheme.colorScheme
    val scroll = rememberScrollState()
    val scope = rememberCoroutineScope()
    val context = LocalContext.current
    var viewTop by remember { mutableFloatStateOf(0f) }
    var teamTop by remember { mutableFloatStateOf(0f) }
    val info = remember(context) { AppInfo.read(context) }

    Scaffold(
        containerColor = scheme.surface,
        topBar = {
            TopAppBar(
                title = { Text("About", fontWeight = FontWeight.SemiBold) },
                navigationIcon = { NebIconButton(Icons.AutoMirrored.Outlined.ArrowBack, "Back", onBack) },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = scheme.surface)
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .onGloballyPositioned { viewTop = it.positionInRoot().y }
                .verticalScroll(scroll)
                .padding(horizontal = 16.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Poster(
                onTeam = { scope.launch { scroll.animateScrollTo((scroll.value + teamTop - viewTop).toInt().coerceAtLeast(0)) } },
                onLibrary = onOpenLibrary
            )

            VersionRow(info) {
                copy(context, "NEBians ${info.name} (${info.build}), Android ${Build.VERSION.RELEASE} (API ${Build.VERSION.SDK_INT})")
                context.nebToast("Version copied")
            }

            Heading("What it is")
            Pillars.chunked(2).forEach { pair ->
                Row(Modifier.fillMaxWidth().height(IntrinsicSize.Min), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    pair.forEach { p -> PillarTile(p, Modifier.weight(1f).fillMaxHeight()) }
                }
            }

            Heading("How it works")
            Panel {
                Steps.forEachIndexed { i, s ->
                    StepRow(s)
                    if (i < Steps.lastIndex) Rule()
                }
            }
            Heading("What you can count on")
            Panel {
                Promises.forEachIndexed { i, (title, text) ->
                    PromiseRow(title, text)
                    if (i < Promises.lastIndex) Rule()
                }
            }

            Box(Modifier.onGloballyPositioned { teamTop = it.positionInRoot().y }) { Heading("The people behind it") }
            PersonTile(Lead, big = true)
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                Devs.forEach { p -> PersonTile(p, big = false, modifier = Modifier.weight(1f)) }
            }
            Crew.chunked(2).forEach { pair ->
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    pair.forEach { p -> PersonTile(p, big = false, modifier = Modifier.weight(1f)) }
                }
            }

            Heading("Runs on your phone")
            Models.forEach { CreditTile(it) }

            Heading("Built on open source")
            Panel {
                Libraries.forEachIndexed { i, l ->
                    LibraryRow(l)
                    if (i < Libraries.lastIndex) Rule()
                }
            }
            Text(
                "Thank you to everyone who built these and gave them away.",
                style = MaterialTheme.typography.bodyMedium,
                color = scheme.onSurfaceVariant,
                modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
            )

            Company {
                runCatching {
                    context.startActivity(Intent(Intent.ACTION_SENDTO, Uri.parse("mailto:support@nebians.consica.com.np")))
                }
            }
            Spacer(Modifier.height(24.dp).navigationBarsPadding())
        }
    }
}

private class AppInfo(val name: String, val build: Long) {
    companion object {
        fun read(context: Context): AppInfo = runCatching {
            val p = context.packageManager.getPackageInfo(context.packageName, 0)
            AppInfo(p.versionName ?: "", PackageInfoCompat.getLongVersionCode(p))
        }.getOrDefault(AppInfo("", 0L))
    }
}

private fun copy(context: Context, text: String) {
    val cm = context.getSystemService(Context.CLIPBOARD_SERVICE) as? ClipboardManager ?: return
    cm.setPrimaryClip(ClipData.newPlainText("NEBians", text))
}

/**
 * The first screen. A tonal panel as tall as half the display, a shape that keeps morphing
 * behind the mark, the three lines big, and the two ways onward. A tap squeezes the mark.
 */
@Composable
private fun Poster(onTeam: () -> Unit, onLibrary: () -> Unit) {
    val scheme = MaterialTheme.colorScheme
    val dark = isDarkSurface()
    val reduced = nebAnimationsReduced()
    val screenH = LocalConfiguration.current.screenHeightDp
    val height = (screenH * 0.5f).coerceIn(380f, 560f).dp
    val shapes = remember {
        listOf(NebGlyphShapes.Cookie, NebGlyphShapes.Sunny, NebGlyphShapes.Flower, NebGlyphShapes.Clover, NebGlyphShapes.Cookie)
    }
    val position = remember { Animatable(0f) }
    val spin = remember { Animatable(0f) }
    val spec = nebSpatialSpec<Float>()
    LaunchedEffect(reduced) {
        if (reduced) return@LaunchedEffect
        while (true) {
            for (i in 1..shapes.lastIndex) {
                delay(1600)
                position.animateTo(i.toFloat(), spec)
                spin.animateTo(spin.value + 45f, spec)
            }
            position.snapTo(0f)
        }
    }
    var tapped by remember { mutableIntStateOf(0) }
    val squeeze = remember { Animatable(1f) }
    LaunchedEffect(tapped) {
        if (tapped == 0) return@LaunchedEffect
        squeeze.snapTo(0.84f)
        squeeze.animateTo(1f, spec)
    }
    val ink = NebTone.Azure.deep(dark)
    Box(
        Modifier
            .fillMaxWidth()
            .height(height)
            .clip(RoundedCornerShape(40.dp))
            .background(NebTone.Azure.container(dark))
            .clipToBounds()
    ) {
        NebMorphBlob(
            shapes = shapes,
            color = NebTone.Sky.container(dark),
            modifier = Modifier.size(360.dp).align(Alignment.TopEnd).offset(x = 110.dp, y = (-70).dp),
            rotation = { spin.value },
            position = { position.value }
        )
        Box(
            Modifier
                .align(Alignment.TopStart)
                .padding(start = 20.dp, top = 20.dp)
                .size(124.dp)
                .nebPressable(scale = 0.94f) { tapped++ }
                .graphicsLayer { scaleX = squeeze.value; scaleY = squeeze.value },
            contentAlignment = Alignment.Center
        ) {
            Image(
                painter = painterResource(R.drawable.ic_launcher_foreground),
                contentDescription = "NEBians",
                modifier = Modifier.fillMaxSize()
            )
        }
        Column(
            Modifier.align(Alignment.BottomStart).padding(24.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Column {
                Text("Made in Nepal.", style = MaterialTheme.typography.displaySmall, fontWeight = FontWeight.Bold, color = ink)
                Text("Free to read.", style = MaterialTheme.typography.displaySmall, fontWeight = FontWeight.Bold, color = ink)
                Text("Built together.", style = MaterialTheme.typography.displaySmall, fontWeight = FontWeight.Bold, color = scheme.primary)
            }
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                NebButton("Meet the team", onTeam, size = NebButtonSize.Standard)
                NebButton("Library", onLibrary, tone = NebButtonTone.Tonal, size = NebButtonSize.Standard)
            }
        }
    }
}

/** Version and the phone it runs on. Tapping the version copies both for a bug report. */
@Composable
private fun VersionRow(info: AppInfo, onCopy: () -> Unit) {
    val dark = isDarkSurface()
    Row(Modifier.fillMaxWidth().height(IntrinsicSize.Min), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
        StatTile(
            tone = NebTone.Sky,
            label = "Version",
            value = info.name.ifBlank { "-" },
            sub = if (info.build > 0) "Build ${info.build}. Tap to copy." else "Tap to copy.",
            modifier = Modifier.weight(1.15f).fillMaxHeight(),
            dark = dark,
            onClick = onCopy
        )
        StatTile(
            tone = NebTone.Aqua,
            label = "Your phone",
            value = "Android ${Build.VERSION.RELEASE}",
            sub = "API ${Build.VERSION.SDK_INT}",
            modifier = Modifier.weight(1f).fillMaxHeight(),
            dark = dark,
            onClick = null
        )
    }
}

@Composable
private fun StatTile(tone: NebTone, label: String, value: String, sub: String, modifier: Modifier, dark: Boolean, onClick: (() -> Unit)?) {
    val shape = RoundedCornerShape(32.dp)
    Column(
        modifier
            .clip(shape)
            .background(tone.container(dark))
            .then(if (onClick != null) Modifier.nebPressable(scale = 0.97f) { onClick() } else Modifier)
            .padding(20.dp),
        verticalArrangement = Arrangement.SpaceBetween
    ) {
        Text(label, style = MaterialTheme.typography.labelLarge, color = tone.deep(dark))
        Column {
            Text(value, style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold, color = tone.deep(dark))
            Text(sub, style = MaterialTheme.typography.bodySmall, color = tone.deep(dark))
        }
    }
}

@Composable
private fun Heading(title: String) {
    Text(
        title,
        style = MaterialTheme.typography.titleLarge,
        fontWeight = FontWeight.SemiBold,
        color = MaterialTheme.colorScheme.onSurface,
        modifier = Modifier.padding(start = 8.dp, top = 20.dp, bottom = 2.dp)
    )
}

/** A flat container with one hairline, like every raised surface on the site. */
@Composable
private fun Panel(content: @Composable () -> Unit) {
    val scheme = MaterialTheme.colorScheme
    val shape = RoundedCornerShape(28.dp)
    Column(
        Modifier
            .fillMaxWidth()
            .clip(shape)
            .background(scheme.surface)
            .border(1.dp, scheme.outlineVariant, shape)
            .padding(horizontal = 18.dp, vertical = 6.dp)
    ) { content() }
}

@Composable
private fun Rule() {
    Box(Modifier.fillMaxWidth().height(1.dp).background(MaterialTheme.colorScheme.outlineVariant))
}

@Composable
private fun ShapeTile(tone: NebTone, shape: RoundedPolygon, size: Dp, content: @Composable () -> Unit) {
    val dark = isDarkSurface()
    Box(
        Modifier.size(size).clip(nebShape(shape)).background(tone.container(dark)),
        contentAlignment = Alignment.Center
    ) { content() }
}

@Composable
private fun PillarTile(p: Pillar, modifier: Modifier) {
    val scheme = MaterialTheme.colorScheme
    val dark = isDarkSurface()
    Column(
        modifier
            .clip(RoundedCornerShape(28.dp))
            .background(scheme.surfaceContainerLow)
            .padding(18.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        ShapeTile(p.tone, p.shape, 56.dp) { Icon(p.icon, null, tint = p.tone.deep(dark), modifier = Modifier.size(26.dp)) }
        Column(verticalArrangement = Arrangement.spacedBy(2.dp)) {
            Text(p.title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold, color = scheme.onSurface)
            Text(p.text, style = MaterialTheme.typography.bodyMedium, color = scheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun StepRow(s: Step) {
    val scheme = MaterialTheme.colorScheme
    Row(
        Modifier.fillMaxWidth().padding(vertical = 14.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Box(
            Modifier.size(44.dp).clip(RoundedCornerShape(16.dp)).background(scheme.primaryContainer),
            contentAlignment = Alignment.Center
        ) { Text(s.n, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = scheme.onPrimaryContainer) }
        Column(Modifier.weight(1f)) {
            Text(s.title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold, color = scheme.onSurface)
            Text(s.text, style = MaterialTheme.typography.bodyMedium, color = scheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun PromiseRow(title: String, text: String) {
    val scheme = MaterialTheme.colorScheme
    Row(
        Modifier.fillMaxWidth().padding(vertical = 14.dp),
        verticalAlignment = Alignment.Top,
        horizontalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        Box(
            Modifier.size(32.dp).clip(nebShape(NebGlyphShapes.Cookie)).background(scheme.tertiaryContainer),
            contentAlignment = Alignment.Center
        ) { Icon(Icons.Outlined.Check, null, tint = scheme.onTertiaryContainer, modifier = Modifier.size(18.dp)) }
        Column(Modifier.weight(1f)) {
            Text(title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, color = scheme.onSurface)
            Text(text, style = MaterialTheme.typography.bodyMedium, color = scheme.onSurfaceVariant)
        }
    }
}

/** A person in their own expressive shape. A tap turns the shape a quarter and lets it settle. */
@Composable
private fun PersonTile(p: Person, big: Boolean, modifier: Modifier = Modifier) {
    val scheme = MaterialTheme.colorScheme
    val dark = isDarkSurface()
    val turn = remember { Animatable(0f) }
    val scope = rememberCoroutineScope()
    val spec = nebSpatialSpec<Float>()
    val side = if (big) 112.dp else 84.dp
    val shape = RoundedCornerShape(28.dp)
    val inner: @Composable () -> Unit = {
        Box(
            Modifier
                .size(side)
                .graphicsLayer { rotationZ = turn.value }
                .clip(nebShape(p.shape))
                .background(p.tone.container(dark)),
            contentAlignment = Alignment.Center
        ) {
            Text(
                p.name.take(1),
                modifier = Modifier.graphicsLayer { rotationZ = -turn.value },
                style = if (big) MaterialTheme.typography.displaySmall else MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.SemiBold,
                color = p.tone.deep(dark)
            )
        }
        Column(horizontalAlignment = if (big) Alignment.Start else Alignment.CenterHorizontally) {
            Text(
                p.name,
                style = if (big) MaterialTheme.typography.titleLarge else MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.SemiBold,
                color = scheme.onSurface,
                textAlign = if (big) TextAlign.Start else TextAlign.Center
            )
            if (p.role.isNotBlank()) {
                Text(p.role, style = MaterialTheme.typography.bodyMedium, color = scheme.onSurfaceVariant)
            }
        }
    }
    if (big) {
        Row(
            modifier
                .fillMaxWidth()
                .clip(shape)
                .background(scheme.surfaceContainerLow)
                .nebPressable(scale = 0.98f) { scope.launch { turn.animateTo(turn.value + 90f, spec) } }
                .padding(20.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(18.dp)
        ) { inner() }
    } else {
        Column(
            modifier
                .clip(shape)
                .background(scheme.surfaceContainerLow)
                .nebPressable(scale = 0.97f) { scope.launch { turn.animateTo(turn.value + 90f, spec) } }
                .padding(vertical = 18.dp, horizontal = 10.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) { inner() }
    }
}

@Composable
private fun CreditTile(c: Credit) {
    val scheme = MaterialTheme.colorScheme
    val dark = isDarkSurface()
    Row(
        Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(28.dp))
            .background(c.tone.container(dark))
            .padding(18.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Box(
            Modifier.size(56.dp).clip(nebShape(c.shape)).background(scheme.surface),
            contentAlignment = Alignment.Center
        ) { Icon(c.icon, null, tint = c.tone.deep(dark), modifier = Modifier.size(26.dp)) }
        Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(2.dp)) {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.Bottom) {
                Text(c.name, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = c.tone.deep(dark))
                Text(c.by, style = MaterialTheme.typography.labelMedium, color = c.tone.deep(dark), modifier = Modifier.padding(bottom = 2.dp))
            }
            Text(c.text, style = MaterialTheme.typography.bodyMedium, color = c.tone.deep(dark))
        }
    }
}

@Composable
private fun LibraryRow(l: Library) {
    val scheme = MaterialTheme.colorScheme
    Row(
        Modifier.fillMaxWidth().padding(vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Icon(Icons.Outlined.Code, null, tint = scheme.onSurfaceVariant, modifier = Modifier.size(20.dp))
        Column(Modifier.weight(1f)) {
            Text(l.name, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Medium, color = scheme.onSurface)
            Text(l.by, style = MaterialTheme.typography.bodySmall, color = scheme.onSurfaceVariant)
        }
        Text(l.license, style = MaterialTheme.typography.labelMedium, color = scheme.onSurfaceVariant, textAlign = TextAlign.End)
    }
}

@Composable
private fun Company(onContact: () -> Unit) {
    val scheme = MaterialTheme.colorScheme
    Column(
        Modifier
            .fillMaxWidth()
            .padding(top = 12.dp)
            .clip(RoundedCornerShape(36.dp))
            .background(scheme.primary)
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        Text("Consica Labs", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold, color = scheme.onPrimary)
        Text("The company behind NEBians.", style = MaterialTheme.typography.bodyLarge, color = scheme.onPrimary)
        Spacer(Modifier.height(12.dp))
        NebButton("Contact us", onContact, tone = NebButtonTone.Tonal, size = NebButtonSize.Standard)
    }
}
