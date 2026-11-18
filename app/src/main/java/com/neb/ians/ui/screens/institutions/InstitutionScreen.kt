package com.neb.ians.ui.screens.institutions

import androidx.compose.animation.core.animateFloat
import androidx.compose.foundation.Canvas
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
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.AccountBalance
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.Link
import androidx.compose.material.icons.outlined.School
import androidx.compose.material.icons.outlined.Verified
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import com.neb.ians.data.api.ApiInstDetail
import com.neb.ians.ui.components.nebToast

private const val WEB = "https://nebians.consica.com.np"

@Composable
fun InstitutionScreen(slug: String, onBack: () -> Unit, onManage: (String) -> Unit, vm: InstitutionViewModel = hiltViewModel()) {
    val st by vm.state.collectAsState()
    LaunchedEffect(slug) { vm.load(slug) }
    val d = st.detail
    val clipboard = LocalClipboardManager.current
    val context = LocalContext.current
    Box(Modifier.fillMaxSize()) {
        if (d == null) {
            if (st.loading) HeadSkeleton(slug, onBack) else {
                Column(Modifier.align(Alignment.Center).padding(32.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(14.dp)) {
                    Text(st.error.orEmpty(), color = MaterialTheme.colorScheme.onSurfaceVariant, textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                    androidx.compose.material3.FilledTonalButton(onClick = { vm.load(slug) }) { Text("Try again") }
                }
                CoverBtn(Icons.AutoMirrored.Outlined.ArrowBack, "Back", onBack, Modifier.statusBarsPadding().padding(14.dp))
            }
        } else LazyColumn(contentPadding = PaddingValues(bottom = 40.dp)) {
            item(key = "head") {
                Head(d, onBack, onCopy = { clipboard.setText(AnnotatedString("$WEB/app/schools/${d.slug}/")); context.nebToast("Link copied") },
                    onEdit = if (d.canEdit) ({ onManage(slug) }) else null)
            }
            item(key = "body") { Box(Modifier.padding(16.dp, 12.dp)) { InstitutionPortfolioHost(slug, vm) } }
        }
    }
}

/** Portfolio plus the section editor sheet. The screen and the owner's profile tab both use it, so there is one behaviour. */
@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
@Composable
fun InstitutionPortfolioHost(slug: String, vm: InstitutionViewModel, load: Boolean = false) {
    val st by vm.state.collectAsState()
    if (load) LaunchedEffect(slug) { vm.load(slug) }
    val d = st.detail ?: return
    val uri = LocalUriHandler.current
    val claim = LocalClaimInstitution.current
    var open by remember { mutableStateOf<Sec?>(null) }
    InstitutionPortfolio(
        d, st.schema, d.canEdit, onEdit = { t -> open = SECTIONS.firstOrNull { it.title == t } },
        onWeb = { uri.openUri(it) }, onClaim = { claim?.invoke(d.slug) }
    )
    open?.let { sec ->
        SectionSheet(sec, st.schema, d.portfolio.details, st.saving, st.error, onSave = { vm.save(slug, it) }, onDismiss = { open = null })
        LaunchedEffect(st.saved) { if (st.saved) { open = null; vm.clearSaved() } }
    }
}

@Composable
private fun CoverBtn(icon: androidx.compose.ui.graphics.vector.ImageVector, label: String, onClick: () -> Unit, modifier: Modifier = Modifier) {
    Box(
        modifier.size(40.dp).clip(RoundedCornerShape(14.dp)).background(MaterialTheme.colorScheme.surface.copy(alpha = 0.72f)).clickable(onClick = onClick),
        contentAlignment = Alignment.Center
    ) { Icon(icon, label, Modifier.size(20.dp), tint = MaterialTheme.colorScheme.onSurface) }
}

/** Concept head: tonal cover to both edges, controls on it, squircle mark across its edge, name, kind and place. */
@Composable
private fun Head(d: ApiInstDetail, onBack: () -> Unit, onCopy: () -> Unit, onEdit: (() -> Unit)?) {
    val c = MaterialTheme.colorScheme
    val dark = c.surface.luminance() < 0.5f
    val cover = if (dark) Color(0xFF0F5223) else Color(0xFFC4EFCB)
    val ink = if (dark) Color(0xFFC4EFCB) else Color(0xFF00210C)
    Column(Modifier.fillMaxWidth()) {
        Box(Modifier.fillMaxWidth()) {
            Box(Modifier.fillMaxWidth().height(190.dp).clip(RoundedCornerShape(bottomStart = 28.dp, bottomEnd = 28.dp)).background(cover)) {
                Canvas(Modifier.fillMaxSize()) {
                    drawCircle(ink.copy(alpha = 0.16f), size.height * 0.5f, Offset(size.width * 0.85f, size.height * 0.2f))
                    drawCircle(ink.copy(alpha = 0.12f), size.height * 0.62f, Offset(size.width * 0.15f, size.height * 1.05f))
                    drawRoundRect(ink.copy(alpha = 0.1f), Offset(size.width * 0.45f, -size.height * 0.1f), Size(size.height * 0.5f, size.height * 0.5f), CornerRadius(32f))
                }
            }
            Row(Modifier.fillMaxWidth().statusBarsPadding().padding(14.dp, 10.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                CoverBtn(Icons.AutoMirrored.Outlined.ArrowBack, "Back", onBack)
                Spacer(Modifier.weight(1f))
                if (onEdit != null) CoverBtn(Icons.Outlined.Edit, "Edit portfolio", onEdit)
                CoverBtn(Icons.Outlined.Link, "Copy link", onCopy)
            }
            com.neb.ians.ui.components.InstitutionLogo(
                photoUrl = d.photoUrl, kind = d.kind, size = 92.dp, corner = 30.dp,
                modifier = Modifier.align(Alignment.BottomStart).padding(start = 16.dp).offset(y = 40.dp),
                container = c.primaryContainer, content = c.onPrimaryContainer
            )
        }
        Spacer(Modifier.height(48.dp))
        Column(Modifier.padding(horizontal = 16.dp), verticalArrangement = Arrangement.spacedBy(2.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(d.name, fontSize = 22.sp, fontWeight = FontWeight.SemiBold, letterSpacing = (-0.4).sp, modifier = Modifier.weight(1f, fill = false))
                if (d.verified) { Spacer(Modifier.width(6.dp)); Icon(Icons.Outlined.Verified, "Verified", Modifier.size(22.dp), tint = c.primary) }
            }
            Text(listOf(d.kindLabel, d.location).filter { it.isNotBlank() }.joinToString(" · "), fontSize = 13.sp, fontWeight = FontWeight.Medium, color = c.onSurfaceVariant)
            if (d.counts.total > 0) Text("${d.counts.students} students and ${d.counts.teachers} teachers on NEBians", fontSize = 12.5.sp, fontWeight = FontWeight.Medium, color = c.onSurfaceVariant)
        }
    }
}

/**
 * The page's own shape while it loads: tonal cover, mark, name bars and card blocks that breathe,
 * with the name filled in when the list the user came from already knew it.
 */
@Composable
private fun HeadSkeleton(slug: String, onBack: () -> Unit) {
    val c = MaterialTheme.colorScheme
    val peek = remember(slug) { InstitutionPeek.get(slug) }
    val pulse = androidx.compose.animation.core.rememberInfiniteTransition(label = "inst_skel")
    val alpha by pulse.animateFloat(
        initialValue = 0.55f, targetValue = 1f,
        animationSpec = androidx.compose.animation.core.infiniteRepeatable(
            androidx.compose.animation.core.tween(800, easing = androidx.compose.animation.core.FastOutSlowInEasing),
            androidx.compose.animation.core.RepeatMode.Reverse
        ),
        label = "inst_skel_a"
    )
    val block = c.surfaceContainerHigh
    Column(Modifier.fillMaxSize()) {
        Box(Modifier.fillMaxWidth()) {
            Box(Modifier.fillMaxWidth().height(190.dp).clip(RoundedCornerShape(bottomStart = 28.dp, bottomEnd = 28.dp)).background(c.primaryContainer.copy(alpha = 0.5f * alpha)))
            CoverBtn(Icons.AutoMirrored.Outlined.ArrowBack, "Back", onBack, Modifier.statusBarsPadding().padding(14.dp, 10.dp))
            Box(Modifier.align(Alignment.BottomStart).padding(start = 16.dp).offset(y = 40.dp).size(92.dp).clip(RoundedCornerShape(30.dp)).background(block.copy(alpha = alpha)))
        }
        Spacer(Modifier.height(48.dp))
        Column(Modifier.padding(horizontal = 16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            if (peek != null) {
                Text(peek.name, fontSize = 22.sp, fontWeight = FontWeight.SemiBold, letterSpacing = (-0.4).sp)
                Text(peek.kindLabel, fontSize = 13.sp, fontWeight = FontWeight.Medium, color = c.onSurfaceVariant)
            } else {
                Box(Modifier.fillMaxWidth(0.6f).height(24.dp).clip(RoundedCornerShape(12.dp)).background(block.copy(alpha = alpha)))
                Box(Modifier.fillMaxWidth(0.35f).height(14.dp).clip(RoundedCornerShape(8.dp)).background(block.copy(alpha = alpha)))
            }
            Spacer(Modifier.height(10.dp))
            repeat(3) {
                Box(Modifier.fillMaxWidth().height(if (it == 0) 72.dp else 120.dp).clip(RoundedCornerShape(24.dp)).background(c.surfaceContainerLow.copy(alpha = alpha)))
            }
        }
    }
}
