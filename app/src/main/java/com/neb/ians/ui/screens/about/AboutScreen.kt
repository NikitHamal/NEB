@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class, androidx.compose.material3.ExperimentalMaterial3Api::class)

package com.neb.ians.ui.screens.about

import android.content.Intent
import android.net.Uri
import androidx.compose.animation.core.Animatable
import androidx.compose.foundation.border
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.AutoAwesome
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.Forum
import androidx.compose.material.icons.outlined.LocalLibrary
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
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
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
import com.neb.ians.ui.screens.onboarding.Reveal
import com.neb.ians.ui.screens.onboarding.isDarkSurface
import com.neb.ians.ui.theme.nebAnimationsReduced
import com.neb.ians.ui.theme.nebSpatialSpec
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

/** Same copy as the web's /about/ (`web/about_data.py`), so the app and the site tell one story. */
private class Pillar(val tone: NebTone, val shape: RoundedPolygon, val icon: ImageVector, val title: String, val text: String)
private class Step(val n: String, val title: String, val text: String)
private class Promise(val title: String, val text: String)
private class Person(val name: String, val role: String, val tone: NebTone, val shape: RoundedPolygon)

private val Pillars = listOf(
    Pillar(NebTone.Azure, NebGlyphShapes.Cookie, Icons.Outlined.LocalLibrary, "The library", "Notes, past papers and solved study books for every class and level."),
    Pillar(NebTone.Sky, NebGlyphShapes.Sunny, Icons.Outlined.Forum, "The forum", "Ask a question and get answers that are marked correct, helpful or wrong."),
    Pillar(NebTone.Aqua, NebGlyphShapes.Flower, Icons.Outlined.AutoAwesome, "Ask Neby", "A study helper that opens beside the page you are reading."),
    Pillar(NebTone.Peri, NebGlyphShapes.Clover, Icons.Outlined.Smartphone, "The app", "The same library on Android, built for one-handed reading.")
)
private val Steps = listOf(
    Step("1", "Find", "Pick a level and a subject."),
    Step("2", "Read", "Open notes, papers and books in the reader."),
    Step("3", "Ask", "Post what you are stuck on."),
    Step("4", "Share", "Upload what helped you, so the next student finds it.")
)
private val Promises = listOf(
    Promise("Free to read", "No paywall in front of the library or the forum."),
    Promise("Checked before it goes public", "Moderators review every upload."),
    Promise("Every level", "School to Master's, entrance included."),
    Promise("Made for phones", "Fast on a small screen and a slow connection.")
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

private const val TEAM_ITEM = 4

@Composable
fun AboutScreen(onBack: () -> Unit, onOpenLibrary: () -> Unit) {
    val scheme = MaterialTheme.colorScheme
    val listState = rememberLazyListState()
    val scope = rememberCoroutineScope()
    val context = LocalContext.current
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
        LazyColumn(
            state = listState,
            modifier = Modifier.fillMaxSize().padding(padding),
            contentPadding = PaddingValues(horizontal = 20.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(36.dp)
        ) {
            item(key = "hero") {
                Hero(
                    onTeam = { scope.launch { listState.animateScrollToItem(TEAM_ITEM) } },
                    onLibrary = onOpenLibrary
                )
            }
            item(key = "pillars") {
                Section("Everything a student looks for.") {
                    Pillars.forEachIndexed { i, p -> Reveal(active = true, index = i, rise = 20.dp) { PillarCard(p) } }
                }
            }
            item(key = "steps") {
                Section("How it works.") {
                    Steps.forEachIndexed { i, s -> Reveal(active = true, index = i, rise = 20.dp) { StepRow(s) } }
                }
            }
            item(key = "promises") {
                Section("What you can count on.") {
                    Promises.forEachIndexed { i, p -> Reveal(active = true, index = i, rise = 16.dp) { PromiseRow(p) } }
                }
            }
            item(key = "team") {
                Section("The people behind NEBians.") {
                    Reveal(active = true, index = 0) { PersonCard(Lead, big = true) }
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        Devs.forEachIndexed { i, p ->
                            Reveal(active = true, index = i + 1, modifier = Modifier.weight(1f)) { PersonCard(p, big = false) }
                        }
                    }
                    Crew.chunked(2).forEachIndexed { row, pair ->
                        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                            pair.forEachIndexed { i, p ->
                                Reveal(active = true, index = row * 2 + i + 1, modifier = Modifier.weight(1f)) { PersonCard(p, big = false) }
                            }
                        }
                    }
                }
            }
            item(key = "company") {
                Reveal(active = true, index = 0) {
                    Company {
                        runCatching {
                            context.startActivity(
                                Intent(Intent.ACTION_SENDTO, Uri.parse("mailto:support@nebians.consica.com.np"))
                            )
                        }
                    }
                }
            }
            item(key = "end") { Spacer(Modifier.height(24.dp).navigationBarsPadding()) }
        }
    }
}

/** Three lines that land one after another beside a mark that keeps changing shape. */
@Composable
private fun Hero(onTeam: () -> Unit, onLibrary: () -> Unit) {
    val scheme = MaterialTheme.colorScheme
    val dark = isDarkSurface()
    val reduced = nebAnimationsReduced()
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
                delay(1500)
                position.animateTo(i.toFloat(), spec)
                spin.animateTo(spin.value + 40f, spec)
            }
            position.snapTo(0f)
        }
    }
    var tapped by remember { mutableIntStateOf(0) }
    val squeeze = remember { Animatable(1f) }
    LaunchedEffect(tapped) {
        if (tapped == 0) return@LaunchedEffect
        squeeze.snapTo(0.86f)
        squeeze.animateTo(1f, spec)
    }
    Column(Modifier.fillMaxWidth().padding(top = 8.dp), verticalArrangement = Arrangement.spacedBy(20.dp)) {
        Reveal(active = true, index = 0, rise = 0.dp) {
            Box(
                Modifier
                    .size(168.dp)
                    .nebPressable(scale = 0.94f) { tapped++ }
                    .graphicsLayer { scaleX = squeeze.value; scaleY = squeeze.value },
                contentAlignment = Alignment.Center
            ) {
                NebMorphBlob(
                    shapes = shapes,
                    color = NebTone.Azure.container(dark),
                    modifier = Modifier.fillMaxSize(),
                    rotation = { spin.value },
                    position = { position.value }
                )
                Image(
                    painter = painterResource(R.drawable.ic_launcher_foreground),
                    contentDescription = "NEBians",
                    modifier = Modifier.size(104.dp)
                )
            }
        }
        Column {
            Reveal(active = true, index = 1) { Text("Made in Nepal.", style = MaterialTheme.typography.displaySmall, fontWeight = FontWeight.SemiBold, color = scheme.onSurface) }
            Reveal(active = true, index = 2) { Text("Free to read.", style = MaterialTheme.typography.displaySmall, fontWeight = FontWeight.SemiBold, color = scheme.onSurface) }
            Reveal(active = true, index = 3) { Text("Built together.", style = MaterialTheme.typography.displaySmall, fontWeight = FontWeight.SemiBold, color = scheme.primary) }
        }
        Reveal(active = true, index = 4, rise = 12.dp) {
            Text("NEBians, by Consica Labs.", style = MaterialTheme.typography.titleMedium, color = scheme.onSurfaceVariant)
        }
        Reveal(active = true, index = 5, rise = 12.dp) {
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                NebButton("Meet the team", onTeam, size = NebButtonSize.Standard)
                NebButton("Open the library", onLibrary, tone = NebButtonTone.Tonal, size = NebButtonSize.Standard)
            }
        }
    }
}

@Composable
private fun Section(title: String, content: @Composable () -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        Reveal(active = true, index = 0, rise = 14.dp) {
            Text(title, style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.onSurface)
        }
        content()
    }
}

/** A glyph tile: a flat tonal expressive shape with its icon, the landing page's pillar mark. */
@Composable
private fun ShapeTile(tone: NebTone, shape: RoundedPolygon, size: Dp, content: @Composable () -> Unit) {
    val dark = isDarkSurface()
    Box(
        Modifier.size(size).clip(nebShape(shape)).background(tone.container(dark)),
        contentAlignment = Alignment.Center
    ) { content() }
}

@Composable
private fun PillarCard(p: Pillar) {
    val scheme = MaterialTheme.colorScheme
    val dark = isDarkSurface()
    Row(
        Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(28.dp))
            .background(scheme.surface)
            .border(1.dp, scheme.outlineVariant, RoundedCornerShape(28.dp))
            .padding(18.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        ShapeTile(p.tone, p.shape, 60.dp) { Icon(p.icon, null, tint = p.tone.deep(dark), modifier = Modifier.size(28.dp)) }
        Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(2.dp)) {
            Text(p.title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold, color = scheme.onSurface)
            Text(p.text, style = MaterialTheme.typography.bodyMedium, color = scheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun StepRow(s: Step) {
    val scheme = MaterialTheme.colorScheme
    Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(16.dp)) {
        Box(
            Modifier.size(48.dp).clip(RoundedCornerShape(16.dp)).background(scheme.primaryContainer),
            contentAlignment = Alignment.Center
        ) { Text(s.n, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = scheme.onPrimaryContainer) }
        Column(Modifier.weight(1f)) {
            Text(s.title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold, color = scheme.onSurface)
            Text(s.text, style = MaterialTheme.typography.bodyMedium, color = scheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun PromiseRow(p: Promise) {
    val scheme = MaterialTheme.colorScheme
    Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.Top, horizontalArrangement = Arrangement.spacedBy(14.dp)) {
        Box(
            Modifier.size(32.dp).clip(nebShape(NebGlyphShapes.Cookie)).background(scheme.tertiaryContainer),
            contentAlignment = Alignment.Center
        ) { Icon(Icons.Outlined.Check, null, tint = scheme.onTertiaryContainer, modifier = Modifier.size(18.dp)) }
        Column(Modifier.weight(1f)) {
            Text(p.title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, color = scheme.onSurface)
            Text(p.text, style = MaterialTheme.typography.bodyMedium, color = scheme.onSurfaceVariant)
        }
    }
}

/** A person in their own expressive shape. A tap turns the shape a quarter and lets it settle. */
@Composable
private fun PersonCard(p: Person, big: Boolean) {
    val scheme = MaterialTheme.colorScheme
    val dark = isDarkSurface()
    val turn = remember { Animatable(0f) }
    val scope = rememberCoroutineScope()
    val spec = nebSpatialSpec<Float>()
    val side = if (big) 120.dp else 88.dp
    Column(
        Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(28.dp))
            .background(scheme.surfaceContainerLow)
            .nebPressable(scale = 0.97f) { scope.launch { turn.animateTo(turn.value + 90f, spec) } }
            .padding(vertical = if (big) 24.dp else 18.dp, horizontal = 12.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
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
        Text(p.name, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold, color = scheme.onSurface, textAlign = TextAlign.Center)
        if (p.role.isNotBlank()) {
            Text(p.role, style = MaterialTheme.typography.bodyMedium, color = scheme.onSurfaceVariant, textAlign = TextAlign.Center)
        }
    }
}

@Composable
private fun Company(onContact: () -> Unit) {
    val scheme = MaterialTheme.colorScheme
    Column(
        Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(32.dp))
            .background(scheme.primaryContainer)
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        Text("Consica Labs.", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.SemiBold, color = scheme.onPrimaryContainer)
        Text("The company behind NEBians.", style = MaterialTheme.typography.bodyLarge, color = scheme.onPrimaryContainer)
        Spacer(Modifier.height(10.dp))
        NebButton("Contact us", onContact, size = NebButtonSize.Standard)
    }
}
