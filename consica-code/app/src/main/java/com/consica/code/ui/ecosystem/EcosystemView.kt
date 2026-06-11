package com.consica.code.ui.ecosystem

import android.view.ViewGroup
import android.webkit.WebView
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import com.consica.code.core.designsystem.CodeTextStyle
import com.consica.code.core.designsystem.EditorBackground
import com.consica.code.core.designsystem.EditorText
import com.consica.code.core.designsystem.LocalEcoUiConfig
import com.consica.code.runtime.html.HtmlSupport

/**
 * Offline, sandboxed HTML preview. JavaScript is disabled and network loads
 * are blocked — rendering is purely local.
 */
@Composable
fun HtmlPreview(
    html: String,
    darkMode: Boolean,
    modifier: Modifier = Modifier,
) {
    val wrapped = remember(html, darkMode) { HtmlSupport.wrapForPreview(html, darkMode) }
    AndroidView(
        modifier = modifier.clip(RoundedCornerShape(20.dp)),
        factory = { context ->
            WebView(context).apply {
                layoutParams = ViewGroup.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT,
                    ViewGroup.LayoutParams.MATCH_PARENT,
                )
                settings.javaScriptEnabled = false
                settings.allowFileAccess = false
                settings.allowContentAccess = false
                settings.blockNetworkLoads = true
                settings.blockNetworkImage = true
            }
        },
        update = { webView ->
            webView.loadDataWithBaseURL(null, wrapped, "text/html", "utf-8", null)
        },
    )
}

/** Console output panel styled like the dark editor surface. */
@Composable
fun ConsolePanel(
    output: String,
    emptyLabel: String,
    modifier: Modifier = Modifier,
) {
    Box(
        modifier = modifier
            .clip(RoundedCornerShape(20.dp))
            .background(EditorBackground),
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
        ) {
            Text(
                text = output.ifEmpty { emptyLabel },
                style = CodeTextStyle,
                color = if (output.isEmpty()) EditorText.copy(alpha = 0.5f) else EditorText,
            )
        }
    }
}

/**
 * The growing-plant celebration: an animated sprout with an optional floating
 * label (e.g. the "Sprout" heading text from the first lesson).
 */
@Composable
fun GrowingPlant(
    label: String?,
    modifier: Modifier = Modifier,
) {
    val config = LocalEcoUiConfig.current
    var started by remember { mutableStateOf(false) }
    LaunchedEffect(Unit) { started = true }
    val growth by animateFloatAsState(
        targetValue = if (started || config.reducedMotion) 1f else 0f,
        animationSpec = tween(if (config.reducedMotion) 0 else 1200),
        label = "plantGrowth",
    )

    Column(
        modifier = modifier,
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        if (label != null && growth > 0.9f) {
            Text(
                text = label,
                style = MaterialTheme.typography.headlineSmall,
                color = MaterialTheme.colorScheme.primary,
            )
            Box(Modifier.height(4.dp))
        }
        Canvas(
            modifier = Modifier
                .fillMaxWidth()
                .height(160.dp),
        ) {
            drawPlant(growth)
        }
    }
}

/** A wilted plant for gentle error feedback. */
@Composable
fun DryPlant(modifier: Modifier = Modifier) {
    Canvas(
        modifier = modifier
            .fillMaxWidth()
            .height(140.dp),
    ) {
        val w = size.width
        val h = size.height
        val cx = w / 2f
        // soil mound
        drawOval(
            color = Color(0xFF8D6E63),
            topLeft = Offset(cx - 70f, h - 36f),
            size = Size(140f, 32f),
        )
        // drooping stem
        val stem = Path().apply {
            moveTo(cx, h - 30f)
            quadraticTo(cx + 6f, h - 90f, cx + 42f, h - 76f)
        }
        drawPath(stem, Color(0xFFBCAAA4), style = Stroke(width = 8f))
        // wilted leaf
        val leaf = Path().apply {
            moveTo(cx + 42f, h - 76f)
            quadraticTo(cx + 78f, h - 76f, cx + 86f, h - 48f)
            quadraticTo(cx + 56f, h - 56f, cx + 42f, h - 76f)
            close()
        }
        drawPath(leaf, Color(0xFFA1887F))
    }
}

private fun androidx.compose.ui.graphics.drawscope.DrawScope.drawPlant(growth: Float) {
    val w = size.width
    val h = size.height
    val cx = w / 2f
    val soil = Color(0xFF6D4C41)
    val stemColor = Color(0xFF388E3C)
    val leafColor = Color(0xFF66BB6A)
    val budColor = Color(0xFFFFD54F)

    // soil mound
    drawOval(
        color = soil,
        topLeft = Offset(cx - 80f, h - 40f),
        size = Size(160f, 36f),
    )

    val stemHeight = (h - 60f) * growth
    if (stemHeight > 4f) {
        drawLine(
            color = stemColor,
            start = Offset(cx, h - 34f),
            end = Offset(cx, h - 34f - stemHeight),
            strokeWidth = 10f,
        )
    }

    if (growth > 0.35f) {
        val leafProgress = ((growth - 0.35f) / 0.65f).coerceIn(0f, 1f)
        val leafY = h - 34f - stemHeight * 0.55f
        val leafSize = 56f * leafProgress
        // left leaf
        val left = Path().apply {
            moveTo(cx, leafY)
            quadraticTo(cx - leafSize, leafY - leafSize * 0.2f, cx - leafSize * 1.2f, leafY - leafSize)
            quadraticTo(cx - leafSize * 0.3f, leafY - leafSize * 0.5f, cx, leafY)
            close()
        }
        drawPath(left, leafColor)
        // right leaf
        val right = Path().apply {
            moveTo(cx, leafY + 16f)
            quadraticTo(cx + leafSize, leafY + 16f - leafSize * 0.2f, cx + leafSize * 1.2f, leafY + 16f - leafSize)
            quadraticTo(cx + leafSize * 0.3f, leafY + 16f - leafSize * 0.5f, cx, leafY + 16f)
            close()
        }
        drawPath(right, leafColor.copy(alpha = 0.9f))
    }

    if (growth > 0.8f) {
        val budProgress = ((growth - 0.8f) / 0.2f).coerceIn(0f, 1f)
        drawCircle(
            color = budColor,
            radius = 18f * budProgress,
            center = Offset(cx, h - 40f - stemHeight),
        )
    }
}
