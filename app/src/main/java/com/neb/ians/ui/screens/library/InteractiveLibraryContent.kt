package com.neb.ians.ui.screens.library

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Biotech
import androidx.compose.material.icons.filled.Code
import androidx.compose.material.icons.filled.Psychology
import androidx.compose.material.icons.filled.RocketLaunch
import androidx.compose.material.icons.filled.Science
import androidx.compose.material.icons.filled.SmartToy
import androidx.compose.material.icons.outlined.Schedule
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.WebChip
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPillShape

private enum class InteractivePreviewMode(val label: String) {
    TwoD("2D"),
    ThreeD("3D")
}

private enum class InteractiveSimType(val label: String) {
    TwoD("2D"),
    ThreeD("3D"),
    Lab("Lab"),
    Coding("Code")
}

private data class InteractiveLesson(
    val title: String,
    val minutes: Int,
    val type: InteractiveSimType
)

private data class InteractiveCourse(
    val title: String,
    val level: String,
    val tagline: String,
    val accent: Color,
    val lessons: List<InteractiveLesson>
) {
    val totalMinutes: Int = lessons.sumOf { it.minutes }
}

private data class InteractiveCategory(
    val key: String,
    val label: String,
    val blurb: String,
    val icon: ImageVector,
    val accent: Color,
    val courses: List<InteractiveCourse>
)

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun InteractiveLibraryContent() {
    val categories = remember { interactiveLibraryCatalog() }
    var mode by rememberSaveable { mutableStateOf(InteractivePreviewMode.TwoD) }
    var categoryFilter by rememberSaveable { mutableStateOf<String?>(null) }
    val visibleCategories = remember(categories, categoryFilter) {
        categoryFilter?.let { key -> categories.filter { it.key == key } } ?: categories
    }

    LazyColumn(
        contentPadding = PaddingValues(start = 16.dp, top = 14.dp, end = 16.dp, bottom = 110.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        item(key = "interactive_overview") {
            InteractiveOverview(
                courseCount = categories.sumOf { it.courses.size },
                lessonCount = categories.sumOf { category -> category.courses.sumOf { it.lessons.size } },
                mode = mode,
                onModeSelected = { mode = it },
                categories = categories,
                categoryFilter = categoryFilter,
                onCategorySelected = { categoryFilter = it }
            )
        }

        items(visibleCategories, key = { it.key }) { category ->
            InteractiveCategorySection(
                category = category,
                mode = mode
            )
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun InteractiveOverview(
    courseCount: Int,
    lessonCount: Int,
    mode: InteractivePreviewMode,
    onModeSelected: (InteractivePreviewMode) -> Unit,
    categories: List<InteractiveCategory>,
    categoryFilter: String?,
    onCategorySelected: (String?) -> Unit
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = "Interactive Learning",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.ExtraBold,
                    modifier = Modifier.weight(1f)
                )
                WebChip(text = "${mode.label} preview", selected = true)
            }
            Text(
                text = "Native course catalog with lightweight previews for virtual labs, 3D models, simulations, and coding games.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            FlowRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                WebChip(text = "$courseCount courses", selected = true)
                WebChip(text = "$lessonCount lessons")
                WebChip(text = "${categories.size} categories")
            }
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                InteractivePreviewMode.entries.forEach { option ->
                    WebChip(
                        text = option.label,
                        selected = mode == option,
                        onClick = { onModeSelected(option) }
                    )
                }
            }
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                WebChip(
                    text = "All",
                    selected = categoryFilter == null,
                    onClick = { onCategorySelected(null) }
                )
                categories.forEach { category ->
                    WebChip(
                        text = category.label,
                        selected = categoryFilter == category.key,
                        onClick = { onCategorySelected(category.key) }
                    )
                }
            }
        }
    }
}

@Composable
private fun InteractiveCategorySection(
    category: InteractiveCategory,
    mode: InteractivePreviewMode
) {
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.Top,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(42.dp)
                    .clip(RoundedCornerShape(8.dp))
                    .background(category.accent.copy(alpha = 0.14f))
                    .border(1.dp, category.accent.copy(alpha = 0.3f), RoundedCornerShape(8.dp)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = category.icon,
                    contentDescription = null,
                    tint = category.accent,
                    modifier = Modifier.size(24.dp)
                )
            }
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = category.label,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = category.blurb,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 3,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }

        if (category.courses.isEmpty()) {
            Surface(
                modifier = Modifier.fillMaxWidth(),
                shape = WebPanelShape,
                color = MaterialTheme.colorScheme.surfaceContainerLowest,
                border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
            ) {
                Text(
                    text = "Interactive courses are on the way.",
                    modifier = Modifier.padding(16.dp),
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        } else {
            category.courses.forEach { course ->
                InteractiveCourseCard(
                    categoryKey = category.key,
                    course = course,
                    mode = mode
                )
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun InteractiveCourseCard(
    categoryKey: String,
    course: InteractiveCourse,
    mode: InteractivePreviewMode
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(
            modifier = Modifier.padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                verticalAlignment = Alignment.Top
            ) {
                LightweightInteractivePreview(
                    categoryKey = categoryKey,
                    accent = course.accent,
                    mode = mode,
                    modifier = Modifier
                        .width(104.dp)
                        .aspectRatio(1.25f)
                )
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = course.title,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = course.tagline,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 3,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }
            FlowRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                WebChip(text = course.level, selected = true)
                WebChip(text = "${course.lessons.size} lessons")
                WebChip(text = "~${course.totalMinutes} min")
            }
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                course.lessons.forEach { lesson ->
                    InteractiveLessonRow(lesson = lesson, accent = course.accent)
                }
            }
        }
    }
}

@Composable
private fun InteractiveLessonRow(
    lesson: InteractiveLesson,
    accent: Color
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(8.dp))
            .background(MaterialTheme.colorScheme.surfaceContainerLow)
            .border(1.dp, MaterialTheme.colorScheme.outlineVariant, RoundedCornerShape(8.dp))
            .padding(horizontal = 10.dp, vertical = 9.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Surface(
            shape = WebPillShape,
            color = accent.copy(alpha = 0.14f)
        ) {
            Text(
                text = lesson.type.label,
                modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp),
                style = MaterialTheme.typography.labelSmall,
                fontWeight = FontWeight.Bold,
                color = accent,
                maxLines = 1
            )
        }
        Text(
            text = lesson.title,
            style = MaterialTheme.typography.bodyMedium,
            fontWeight = FontWeight.SemiBold,
            color = MaterialTheme.colorScheme.onSurface,
            maxLines = 2,
            overflow = TextOverflow.Ellipsis,
            modifier = Modifier.weight(1f)
        )
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(3.dp)
        ) {
            Icon(
                imageVector = Icons.Outlined.Schedule,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.size(15.dp)
            )
            Text(
                text = "${lesson.minutes}m",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1
            )
        }
    }
}

@Composable
private fun LightweightInteractivePreview(
    categoryKey: String,
    accent: Color,
    mode: InteractivePreviewMode,
    modifier: Modifier = Modifier
) {
    val gridColor = MaterialTheme.colorScheme.outlineVariant
    val surfaceColor = MaterialTheme.colorScheme.surfaceContainerHigh
    val secondary = MaterialTheme.colorScheme.primary
    Canvas(
        modifier = modifier
            .clip(RoundedCornerShape(8.dp))
            .background(surfaceColor)
            .border(1.dp, gridColor, RoundedCornerShape(8.dp))
    ) {
        val w = size.width
        val h = size.height
        val stroke = Stroke(width = 2.dp.toPx(), cap = StrokeCap.Round)
        val softAccent = accent.copy(alpha = 0.18f)
        drawRoundRect(
            color = softAccent,
            topLeft = Offset(w * 0.08f, h * 0.12f),
            size = Size(w * 0.84f, h * 0.72f),
            cornerRadius = CornerRadius(10.dp.toPx())
        )

        when (categoryKey) {
            "robotics" -> {
                if (mode == InteractivePreviewMode.ThreeD) {
                    drawLine(accent, Offset(w * 0.18f, h * 0.72f), Offset(w * 0.45f, h * 0.42f), strokeWidth = 4.dp.toPx(), cap = StrokeCap.Round)
                    drawLine(accent, Offset(w * 0.45f, h * 0.42f), Offset(w * 0.76f, h * 0.3f), strokeWidth = 4.dp.toPx(), cap = StrokeCap.Round)
                    drawCircle(secondary, 7.dp.toPx(), Offset(w * 0.18f, h * 0.72f))
                    drawCircle(secondary, 6.dp.toPx(), Offset(w * 0.45f, h * 0.42f))
                    drawCircle(secondary, 5.dp.toPx(), Offset(w * 0.76f, h * 0.3f))
                } else {
                    drawRoundRect(accent, Offset(w * 0.22f, h * 0.36f), Size(w * 0.44f, h * 0.24f), CornerRadius(8.dp.toPx()))
                    drawCircle(secondary, 5.dp.toPx(), Offset(w * 0.32f, h * 0.64f))
                    drawCircle(secondary, 5.dp.toPx(), Offset(w * 0.58f, h * 0.64f))
                    drawLine(gridColor, Offset(w * 0.14f, h * 0.78f), Offset(w * 0.86f, h * 0.78f), strokeWidth = 3.dp.toPx(), cap = StrokeCap.Round)
                }
            }
            "space" -> {
                drawCircle(accent, 8.dp.toPx(), Offset(w * 0.5f, h * 0.48f))
                listOf(0.22f, 0.34f, 0.46f).forEachIndexed { index, radius ->
                    drawOval(
                        color = if (index == 1) secondary else gridColor,
                        topLeft = Offset(w * (0.5f - radius), h * (0.48f - radius * 0.56f)),
                        size = Size(w * radius * 2f, h * radius * 1.12f),
                        style = Stroke(width = 1.5.dp.toPx())
                    )
                }
                val planetOffset = if (mode == InteractivePreviewMode.ThreeD) Offset(w * 0.74f, h * 0.34f) else Offset(w * 0.28f, h * 0.55f)
                drawCircle(secondary, 5.dp.toPx(), planetOffset)
            }
            "physics" -> {
                val path = Path().apply {
                    moveTo(w * 0.14f, h * 0.7f)
                    quadraticBezierTo(w * 0.38f, h * 0.22f, w * 0.82f, h * 0.58f)
                }
                drawPath(path, accent, style = stroke)
                drawCircle(secondary, 7.dp.toPx(), Offset(w * 0.34f, h * 0.36f))
                drawLine(gridColor, Offset(w * 0.18f, h * 0.76f), Offset(w * 0.84f, h * 0.76f), strokeWidth = 2.dp.toPx())
                if (mode == InteractivePreviewMode.ThreeD) {
                    drawLine(gridColor, Offset(w * 0.2f, h * 0.76f), Offset(w * 0.34f, h * 0.88f), strokeWidth = 1.5.dp.toPx())
                    drawLine(gridColor, Offset(w * 0.84f, h * 0.76f), Offset(w * 0.94f, h * 0.88f), strokeWidth = 1.5.dp.toPx())
                }
            }
            "chemistry" -> {
                drawRoundRect(
                    color = accent.copy(alpha = 0.28f),
                    topLeft = Offset(w * 0.18f, h * 0.48f),
                    size = Size(w * 0.28f, h * 0.24f),
                    cornerRadius = CornerRadius(5.dp.toPx())
                )
                drawLine(accent, Offset(w * 0.2f, h * 0.48f), Offset(w * 0.44f, h * 0.48f), strokeWidth = 2.dp.toPx())
                val molecule = listOf(
                    Offset(w * 0.68f, h * 0.38f),
                    Offset(w * 0.58f, h * 0.58f),
                    Offset(w * 0.78f, h * 0.6f)
                )
                drawLine(gridColor, molecule[0], molecule[1], strokeWidth = 2.dp.toPx())
                drawLine(gridColor, molecule[0], molecule[2], strokeWidth = 2.dp.toPx())
                molecule.forEachIndexed { index, point ->
                    drawCircle(if (index == 0) accent else secondary, 6.dp.toPx(), point)
                }
            }
            "biology" -> {
                drawOval(
                    color = accent.copy(alpha = 0.24f),
                    topLeft = Offset(w * 0.18f, h * 0.22f),
                    size = Size(w * 0.58f, h * 0.46f)
                )
                drawCircle(accent, 9.dp.toPx(), Offset(w * 0.48f, h * 0.44f))
                drawCircle(secondary, 4.dp.toPx(), Offset(w * 0.62f, h * 0.35f))
                drawLine(gridColor, Offset(w * 0.62f, h * 0.7f), Offset(w * 0.78f, h * 0.84f), strokeWidth = 3.dp.toPx(), cap = StrokeCap.Round)
            }
            "ai" -> {
                val nodes = listOf(
                    Offset(w * 0.24f, h * 0.34f),
                    Offset(w * 0.24f, h * 0.64f),
                    Offset(w * 0.5f, h * 0.48f),
                    Offset(w * 0.76f, h * 0.34f),
                    Offset(w * 0.76f, h * 0.64f)
                )
                listOf(0 to 2, 1 to 2, 2 to 3, 2 to 4).forEach { (a, b) ->
                    drawLine(gridColor, nodes[a], nodes[b], strokeWidth = 2.dp.toPx())
                }
                nodes.forEachIndexed { index, point ->
                    drawCircle(if (index == 2) accent else secondary, 5.dp.toPx(), point)
                }
            }
            else -> {
                repeat(3) { index ->
                    val top = h * (0.28f + index * 0.16f)
                    drawRoundRect(
                        color = if (index == 1) accent else secondary.copy(alpha = 0.75f),
                        topLeft = Offset(w * 0.18f, top),
                        size = Size(w * (0.34f + index * 0.12f), h * 0.08f),
                        cornerRadius = CornerRadius(4.dp.toPx())
                    )
                }
                if (mode == InteractivePreviewMode.ThreeD) {
                    drawLine(gridColor, Offset(w * 0.58f, h * 0.28f), Offset(w * 0.76f, h * 0.44f), strokeWidth = 2.dp.toPx())
                    drawLine(gridColor, Offset(w * 0.76f, h * 0.44f), Offset(w * 0.58f, h * 0.6f), strokeWidth = 2.dp.toPx())
                }
            }
        }
    }
}

private fun interactiveLibraryCatalog(): List<InteractiveCategory> = listOf(
    InteractiveCategory(
        key = "robotics",
        label = "Robotics",
        icon = Icons.Filled.SmartToy,
        accent = Color(0xFF0EA5E9),
        blurb = "Build, wire and program virtual robots from your first motor to inverse kinematics.",
        courses = listOf(
            InteractiveCourse(
                title = "Robotics Explorer",
                level = "Beginner",
                accent = Color(0xFF0EA5E9),
                tagline = "Meet your first robot and discover what makes it tick.",
                lessons = listOf(
                    InteractiveLesson("Meet the Robot", 12, InteractiveSimType.ThreeD),
                    InteractiveLesson("Robot Power!", 12, InteractiveSimType.Lab),
                    InteractiveLesson("Gears in Motion", 14, InteractiveSimType.ThreeD),
                    InteractiveLesson("Robot Senses", 14, InteractiveSimType.ThreeD)
                )
            ),
            InteractiveCourse(
                title = "Robot Builder Workshop",
                level = "Intermediate",
                accent = Color(0xFF0284C7),
                tagline = "Drive, steer, grab and dodge with real robot behaviors.",
                lessons = listOf(
                    InteractiveLesson("Motors & Wheels", 15, InteractiveSimType.ThreeD),
                    InteractiveLesson("Line Follower", 15, InteractiveSimType.TwoD),
                    InteractiveLesson("The Robotic Arm", 16, InteractiveSimType.ThreeD),
                    InteractiveLesson("Obstacle Avoider", 15, InteractiveSimType.ThreeD)
                )
            ),
            InteractiveCourse(
                title = "Robotics Engineer Lab",
                level = "Advanced",
                accent = Color(0xFF0369A1),
                tagline = "IK solvers, PID loops, state machines and a Mars rover.",
                lessons = listOf(
                    InteractiveLesson("Inverse Kinematics", 18, InteractiveSimType.ThreeD),
                    InteractiveLesson("The PID Controller", 20, InteractiveSimType.TwoD),
                    InteractiveLesson("Logic & State Machines", 18, InteractiveSimType.TwoD),
                    InteractiveLesson("Mars Rover Sandbox", 20, InteractiveSimType.ThreeD)
                )
            )
        )
    ),
    InteractiveCategory(
        key = "space",
        label = "Space & Astronomy",
        icon = Icons.Filled.RocketLaunch,
        accent = Color(0xFF8B5CF6),
        blurb = "Fly through the solar system, bend orbits with gravity and explore our galaxy in 3D.",
        courses = listOf(
            InteractiveCourse(
                title = "Solar System Journey",
                level = "Beginner",
                accent = Color(0xFF8B5CF6),
                tagline = "Fly past the Sun, eight planets, the Moon and an eclipse.",
                lessons = listOf(
                    InteractiveLesson("Tour the Solar System", 15, InteractiveSimType.ThreeD),
                    InteractiveLesson("Earth, Moon and Sun", 15, InteractiveSimType.ThreeD),
                    InteractiveLesson("Phases of the Moon", 12, InteractiveSimType.ThreeD),
                    InteractiveLesson("Eclipses", 14, InteractiveSimType.ThreeD)
                )
            ),
            InteractiveCourse(
                title = "Gravity & Orbits",
                level = "Intermediate",
                accent = Color(0xFF7C3AED),
                tagline = "Launch planets, fly rockets and bend space around a star.",
                lessons = listOf(
                    InteractiveLesson("Orbital Sandbox", 18, InteractiveSimType.TwoD),
                    InteractiveLesson("Rocket Launch", 16, InteractiveSimType.TwoD),
                    InteractiveLesson("Kepler's Laws", 15, InteractiveSimType.TwoD),
                    InteractiveLesson("Weight on Other Worlds", 12, InteractiveSimType.TwoD)
                )
            ),
            InteractiveCourse(
                title = "Galaxies & the Universe",
                level = "Intermediate",
                accent = Color(0xFF6D28D9),
                tagline = "Zoom from Everest to the edge of the observable universe.",
                lessons = listOf(
                    InteractiveLesson("The Milky Way Galaxy", 14, InteractiveSimType.ThreeD),
                    InteractiveLesson("Lifecycle of Stars", 16, InteractiveSimType.TwoD),
                    InteractiveLesson("Scale of the Universe", 15, InteractiveSimType.TwoD)
                )
            )
        )
    ),
    InteractiveCategory(
        key = "physics",
        label = "Physics Lab",
        icon = Icons.Filled.Science,
        accent = Color(0xFFF59E0B),
        blurb = "A virtual physics lab with pendulums, projectiles, waves, optics and circuits.",
        courses = listOf(
            InteractiveCourse(
                title = "Playground Physics",
                level = "Beginner",
                accent = Color(0xFFF59E0B),
                tagline = "Push boxes, race balls down ramps, bounce and play with magnets.",
                lessons = listOf(
                    InteractiveLesson("Pushes and Pulls", 10, InteractiveSimType.Lab),
                    InteractiveLesson("Ramps and Rolling", 10, InteractiveSimType.Lab),
                    InteractiveLesson("Bouncing Balls", 10, InteractiveSimType.Lab),
                    InteractiveLesson("Magnet Magic", 10, InteractiveSimType.Lab)
                )
            ),
            InteractiveCourse(
                title = "Virtual Physics Lab",
                level = "Intermediate",
                accent = Color(0xFFD97706),
                tagline = "Swing pendulums, fire projectiles, bend light and wire circuits.",
                lessons = listOf(
                    InteractiveLesson("Pendulum Lab", 15, InteractiveSimType.Lab),
                    InteractiveLesson("Projectile Motion", 15, InteractiveSimType.Lab),
                    InteractiveLesson("Waves & Sound", 16, InteractiveSimType.Lab),
                    InteractiveLesson("Optics Bench", 18, InteractiveSimType.Lab),
                    InteractiveLesson("Circuit Builder", 16, InteractiveSimType.Lab)
                )
            ),
            InteractiveCourse(
                title = "NEB Physics Practicals - Class 11",
                level = "Intermediate",
                accent = Color(0xFFD97706),
                tagline = "Class 11 NEB practicals as realistic virtual instruments.",
                lessons = listOf(
                    InteractiveLesson("Vernier Calipers", 15, InteractiveSimType.Lab),
                    InteractiveLesson("Micrometer Screw Gauge", 14, InteractiveSimType.Lab),
                    InteractiveLesson("Spherometer: Radius of Curvature", 15, InteractiveSimType.Lab),
                    InteractiveLesson("Simple Pendulum: Measuring g", 18, InteractiveSimType.Lab),
                    InteractiveLesson("Parallelogram Law of Forces", 15, InteractiveSimType.Lab),
                    InteractiveLesson("Coefficient of Friction", 14, InteractiveSimType.Lab),
                    InteractiveLesson("Hooke's Law & Spring Constant", 15, InteractiveSimType.Lab),
                    InteractiveLesson("Specific Heat by Method of Mixtures", 18, InteractiveSimType.Lab)
                )
            ),
            InteractiveCourse(
                title = "NEB Physics Practicals - Class 12",
                level = "Advanced",
                accent = Color(0xFFB45309),
                tagline = "Sound, electricity and optics for the Class 12 practical set.",
                lessons = listOf(
                    InteractiveLesson("Resonance Tube: Speed of Sound", 16, InteractiveSimType.Lab),
                    InteractiveLesson("Sonometer: Laws of Vibrating Strings", 16, InteractiveSimType.Lab),
                    InteractiveLesson("Ohm's Law & Resistivity", 16, InteractiveSimType.Lab),
                    InteractiveLesson("Meter Bridge: Unknown Resistance", 15, InteractiveSimType.Lab),
                    InteractiveLesson("Potentiometer: Comparing EMFs", 16, InteractiveSimType.Lab),
                    InteractiveLesson("Galvanometer: Figure of Merit", 14, InteractiveSimType.Lab),
                    InteractiveLesson("Focal Length of Mirrors & Lenses", 17, InteractiveSimType.Lab),
                    InteractiveLesson("Prism: Angle of Minimum Deviation", 17, InteractiveSimType.Lab)
                )
            )
        )
    ),
    InteractiveCategory(
        key = "chemistry",
        label = "Chemistry Lab",
        icon = Icons.Filled.Biotech,
        accent = Color(0xFF10B981),
        blurb = "Build atoms, spin molecules and run safe virtual experiments.",
        courses = listOf(
            InteractiveCourse(
                title = "Kitchen Chemistry",
                level = "Beginner",
                accent = Color(0xFF10B981),
                tagline = "Your kitchen is secretly a science lab.",
                lessons = listOf(
                    InteractiveLesson("Mix It Up!", 10, InteractiveSimType.Lab),
                    InteractiveLesson("Density Tower", 12, InteractiveSimType.Lab),
                    InteractiveLesson("Solids, Liquids... Fizz!", 10, InteractiveSimType.Lab),
                    InteractiveLesson("Hot and Cold", 10, InteractiveSimType.Lab)
                )
            ),
            InteractiveCourse(
                title = "Virtual Chemistry Lab",
                level = "Intermediate",
                accent = Color(0xFF059669),
                tagline = "Build atoms, spin real molecules and titrate acids safely.",
                lessons = listOf(
                    InteractiveLesson("Atom Builder", 16, InteractiveSimType.ThreeD),
                    InteractiveLesson("Molecule Gallery", 15, InteractiveSimType.ThreeD),
                    InteractiveLesson("States of Matter", 15, InteractiveSimType.Lab),
                    InteractiveLesson("Acid-Base Lab", 17, InteractiveSimType.Lab),
                    InteractiveLesson("Reaction Balancer", 14, InteractiveSimType.Lab)
                )
            ),
            InteractiveCourse(
                title = "NEB Chemistry Practicals - Class 11",
                level = "Intermediate",
                accent = Color(0xFF059669),
                tagline = "The complete Class 11 practical book as virtual experiments.",
                lessons = listOf(
                    InteractiveLesson("Lab Apparatus & Safety", 14, InteractiveSimType.Lab),
                    InteractiveLesson("Separation Techniques", 16, InteractiveSimType.Lab),
                    InteractiveLesson("Acid-Base Titration", 20, InteractiveSimType.Lab),
                    InteractiveLesson("Flame Tests & Cation Detection", 14, InteractiveSimType.Lab),
                    InteractiveLesson("Salt Analysis: Anion Tests", 16, InteractiveSimType.Lab),
                    InteractiveLesson("Preparation of Gases", 16, InteractiveSimType.Lab),
                    InteractiveLesson("Water of Crystallization", 18, InteractiveSimType.Lab)
                )
            ),
            InteractiveCourse(
                title = "NEB Chemistry Practicals - Class 12",
                level = "Advanced",
                accent = Color(0xFF047857),
                tagline = "Redox titration, salt analysis, electrolysis and organic tests.",
                lessons = listOf(
                    InteractiveLesson("Redox Titration with KMnO4", 20, InteractiveSimType.Lab),
                    InteractiveLesson("Full Salt Analysis Scheme", 20, InteractiveSimType.Lab),
                    InteractiveLesson("Electrolysis of CuSO4", 16, InteractiveSimType.Lab),
                    InteractiveLesson("pH & Indicators", 15, InteractiveSimType.Lab),
                    InteractiveLesson("Organic Functional Group Tests", 18, InteractiveSimType.Lab),
                    InteractiveLesson("Heat of Neutralization", 16, InteractiveSimType.Lab),
                    InteractiveLesson("Lassaigne's Test: N, S & Halogens", 18, InteractiveSimType.Lab)
                )
            )
        )
    ),
    InteractiveCategory(
        key = "biology",
        label = "Biology Lab",
        icon = Icons.Filled.Biotech,
        accent = Color(0xFF84CC16),
        blurb = "Peer through a virtual microscope, watch cells divide and explore living systems.",
        courses = listOf(
            InteractiveCourse(
                title = "NEB Biology Practicals - Class 11",
                level = "Intermediate",
                accent = Color(0xFF65A30D),
                tagline = "Botany and zoology practicals with microscope, wet lab, field notebook, and specimen bench.",
                lessons = listOf(
                    InteractiveLesson("Compound Microscope Handling", 14, InteractiveSimType.Lab),
                    InteractiveLesson("Temporary Mount of Onion Epidermis", 15, InteractiveSimType.Lab),
                    InteractiveLesson("Stomata in Leaf Epidermis", 15, InteractiveSimType.Lab),
                    InteractiveLesson("Osmosis and Plasmolysis", 16, InteractiveSimType.Lab),
                    InteractiveLesson("Biomolecule Food Tests", 16, InteractiveSimType.Lab),
                    InteractiveLesson("Photosynthesis Rate in Aquatic Plant", 16, InteractiveSimType.Lab),
                    InteractiveLesson("Flower Dissection and Floral Formula", 17, InteractiveSimType.Lab),
                    InteractiveLesson("Zoology Specimen Identification", 17, InteractiveSimType.Lab)
                )
            ),
            InteractiveCourse(
                title = "NEB Biology Practicals - Class 12",
                level = "Advanced",
                accent = Color(0xFF15803D),
                tagline = "Plant anatomy, physiology, genetics, biotechnology, histology, and blood grouping.",
                lessons = listOf(
                    InteractiveLesson("Dicot and Monocot Anatomy", 17, InteractiveSimType.Lab),
                    InteractiveLesson("Transpiration With Potometer", 17, InteractiveSimType.Lab),
                    InteractiveLesson("Pollen Germination", 16, InteractiveSimType.Lab),
                    InteractiveLesson("Mitosis in Onion Root Tip", 18, InteractiveSimType.Lab),
                    InteractiveLesson("Mendelian Genetics Simulator", 17, InteractiveSimType.Lab),
                    InteractiveLesson("DNA Isolation From Plant Tissue", 18, InteractiveSimType.Lab),
                    InteractiveLesson("Animal Tissue Histology", 17, InteractiveSimType.Lab),
                    InteractiveLesson("ABO and Rh Blood Grouping", 18, InteractiveSimType.Lab)
                )
            )
        )
    ),
    InteractiveCategory(
        key = "ai",
        label = "AI & Machine Learning",
        icon = Icons.Filled.Psychology,
        accent = Color(0xFF6366F1),
        blurb = "Train neurons, teach machines to see and discover how modern AI works.",
        courses = listOf(
            InteractiveCourse(
                title = "AI From Scratch to Advanced",
                level = "Beginner to Advanced",
                accent = Color(0xFF4F46E5),
                tagline = "Rules, data, training, neural networks, vision, language models, transformers, safety, and deployment.",
                lessons = listOf(
                    InteractiveLesson("What AI Really Is", 12, InteractiveSimType.Lab),
                    InteractiveLesson("Data Is the Teacher", 14, InteractiveSimType.Lab),
                    InteractiveLesson("Classification and Decision Boundaries", 14, InteractiveSimType.Lab),
                    InteractiveLesson("Neurons, Weights and Layers", 15, InteractiveSimType.Lab),
                    InteractiveLesson("Training With Gradient Descent", 16, InteractiveSimType.Lab),
                    InteractiveLesson("Computer Vision: Pixels to Meaning", 15, InteractiveSimType.Lab),
                    InteractiveLesson("Language AI: Tokens and Embeddings", 15, InteractiveSimType.Lab),
                    InteractiveLesson("Attention and Transformers", 18, InteractiveSimType.Lab),
                    InteractiveLesson("Generative AI and Hallucinations", 16, InteractiveSimType.Lab),
                    InteractiveLesson("Responsible AI Deployment", 18, InteractiveSimType.Lab)
                )
            )
        )
    ),
    InteractiveCategory(
        key = "coding",
        label = "Coding Adventures",
        icon = Icons.Filled.Code,
        accent = Color(0xFFEC4899),
        blurb = "Learn HTML, CSS, JavaScript and Python through games and friendly guides.",
        courses = listOf(
            InteractiveCourse(
                title = "Block Coding Adventure",
                level = "Beginner",
                accent = Color(0xFFEC4899),
                tagline = "Guide a robot through mazes by snapping code blocks together.",
                lessons = listOf(
                    InteractiveLesson("First Steps: Robot on a Mission", 15, InteractiveSimType.Coding),
                    InteractiveLesson("Loop the Loop", 20, InteractiveSimType.Coding),
                    InteractiveLesson("Smart Choices", 20, InteractiveSimType.Coding)
                )
            ),
            InteractiveCourse(
                title = "Web Wizard: HTML & CSS",
                level = "Beginner",
                accent = Color(0xFFDB2777),
                tagline = "Write HTML and CSS in a live editor.",
                lessons = listOf(
                    InteractiveLesson("HTML Building Blocks", 20, InteractiveSimType.Coding),
                    InteractiveLesson("CSS Magic", 20, InteractiveSimType.Coding),
                    InteractiveLesson("My First Webpage", 25, InteractiveSimType.Coding)
                )
            ),
            InteractiveCourse(
                title = "JavaScript Quest",
                level = "Intermediate",
                accent = Color(0xFFC026D3),
                tagline = "Learn variables, functions and DOM interactivity with live tests.",
                lessons = listOf(
                    InteractiveLesson("Variables & Numbers", 20, InteractiveSimType.Coding),
                    InteractiveLesson("Functions in Action", 20, InteractiveSimType.Coding),
                    InteractiveLesson("Make It Interactive", 25, InteractiveSimType.Coding)
                )
            ),
            InteractiveCourse(
                title = "Python Playground",
                level = "Beginner",
                accent = Color(0xFFBE185D),
                tagline = "Write real Python from print() to a grade calculator.",
                lessons = listOf(
                    InteractiveLesson("Hello, Python!", 15, InteractiveSimType.Coding),
                    InteractiveLesson("Loops & Logic", 20, InteractiveSimType.Coding),
                    InteractiveLesson("Lists & Functions", 20, InteractiveSimType.Coding),
                    InteractiveLesson("Final Quest: Grade Calculator", 25, InteractiveSimType.Coding)
                )
            ),
            InteractiveCourse(
                title = "Code Master Challenges",
                level = "Advanced",
                accent = Color(0xFFA21CAF),
                tagline = "Build a stopwatch, generative art, a data analyser and a word game.",
                lessons = listOf(
                    InteractiveLesson("Build a Stopwatch", 15, InteractiveSimType.Coding),
                    InteractiveLesson("Paint with Code", 15, InteractiveSimType.Coding),
                    InteractiveLesson("Python Data Detective", 15, InteractiveSimType.Coding),
                    InteractiveLesson("Python Word Game", 18, InteractiveSimType.Coding)
                )
            )
        )
    )
)
