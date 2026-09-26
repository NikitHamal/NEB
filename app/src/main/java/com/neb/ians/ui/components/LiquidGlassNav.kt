package com.neb.ians.ui.components

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.ripple
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.testTag
import com.neb.ians.util.rememberTactileFeedback
import com.neb.ians.util.TactileType
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.R
import com.neb.ians.ui.theme.nebFastSpatialSpec
import androidx.compose.material.icons.rounded.Close

// ---------------------------------------------------------------------------
// NEBians "N" logo as a Compose drawable.
// ---------------------------------------------------------------------------

@Composable
fun NebLogo(modifier: Modifier = Modifier, size: Dp = 32.dp) {
    androidx.compose.foundation.Image(
        painter = painterResource(id = R.drawable.n_logo),
        contentDescription = "NEBians",
        modifier = modifier.size(size)
    )
}

// ---------------------------------------------------------------------------
// Top app bar — mirrors the web .md-topbar (brand + actions).
// ---------------------------------------------------------------------------

@Composable
fun NebTopBar(
    modifier: Modifier = Modifier,
    showBrand: Boolean = true,
    title: String? = null,
    titleFontWeight: FontWeight = FontWeight.Bold,
    onBack: (() -> Unit)? = null,
    onSearch: (() -> Unit)? = null,
    isAuthenticated: Boolean = false,
    photoUrl: String? = null,
    username: String = "",
    unread: Int = 0,
    onProfile: (() -> Unit)? = null,
    actions: (@Composable () -> Unit)? = null,
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .background(MaterialTheme.colorScheme.surface)
            .statusBarsPadding()
            .padding(horizontal = 12.dp, vertical = 8.dp)
            .height(48.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        if (onBack != null) {
            NebIconButton(
                icon = Icons.AutoMirrored.Outlined.ArrowBack,
                contentDescription = "Back",
                onClick = onBack
            )
            Spacer(Modifier.width(4.dp))
        }
        if (showBrand) {
            NebLogo(size = 30.dp)
            Spacer(Modifier.width(8.dp))
            Text(
                "NEBians",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onSurface
            )
            Spacer(Modifier.weight(1f))
        } else if (title != null) {
            Text(
                title,
                modifier = Modifier.weight(1f),
                style = MaterialTheme.typography.titleLarge,
                fontWeight = titleFontWeight,
                color = MaterialTheme.colorScheme.onSurface,
                maxLines = 1,
                overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
            )
            Spacer(Modifier.width(8.dp))
        } else {
            Spacer(Modifier.weight(1f))
        }
        if (actions != null) {
            actions()
        }
        if (onSearch != null) {
            NebIconButton(Icons.Outlined.Search, "Search", onSearch)
        }
    }
}

// ---------------------------------------------------------------------------
// Liquid-glass floating bottom navigation (3 items, like the web nav pill).
// ---------------------------------------------------------------------------

data class NebNavItem(
    val route: String,
    val label: String,
    val selectedIcon: ImageVector,
    val unselectedIcon: ImageVector,
)

@Composable
fun LiquidGlassBottomNav(
    items: List<NebNavItem>,
    currentRoute: String?,
    onSelect: (NebNavItem) -> Unit,
    modifier: Modifier = Modifier,
    onCreateClick: (() -> Unit)? = null,
    menuActions: List<NebFabAction> = emptyList(),
    menuExpanded: Boolean = false,
    onMenuDismiss: () -> Unit = {},
    photoUrl: String? = null,
    username: String = "",
    onProfileClick: (() -> Unit)? = null,
    /**
     * The page underneath, if the caller recorded one. Given a backdrop the rail
     * becomes real glass: it samples what is actually behind it, blurs it, and
     * bends it at the rim. Without one — or on a device that cannot run the
     * shader — it stays the opaque surface described below.
     */
    backdrop: NebGlassBackdrop? = null,
) {
    val isDark = MaterialTheme.colorScheme.surface.luminanceIsDark()
    val isLowEnd = com.neb.ians.util.rememberIsLowEndDevice()
    val scheme = MaterialTheme.colorScheme

    // Glass if the caller gave us a page to refract and the device can do it.
    val glassTier = rememberNebGlassTier()
    val glassStyle = rememberNebGlassStyle(isDark)
    val glass = backdrop != null && glassTier != NebGlassTier.FLAT

    // The bar is opaque, and that is the point of this block.
    //
    // It used to be a 92%-alpha gradient over two hardcoded greys, which cost it
    // twice. The greys predate the colour revamp, so on a page built from the
    // blue-tinted neutral ramp the bar read as the one grey object on the
    // screen. And eight percent of a paragraph of body text showing through a
    // navigation bar is still legible enough to fight the labels sitting on it.
    // A bar you can read the page through is not a surface, it is a smudge.
    //
    // So: full alpha, scheme tokens, and the faintest vertical fall so it still
    // has a top edge to catch the light on.
    val barBrush = remember(isDark, scheme) {
        if (isDark) {
            Brush.verticalGradient(listOf(scheme.surfaceContainerHigh, scheme.surfaceContainer))
        } else {
            Brush.verticalGradient(listOf(scheme.surfaceContainerLowest, scheme.surfaceContainerLow))
        }
    }

    // One hairline, the same one every other card in the app uses. The old
    // white-to-grey gradient rim lit the bar from inside and made it look
    // inflated next to the create button.
    val barBorder = scheme.outlineVariant

    val primaryColor = scheme.primary
    val navHeight = 58.dp
    // The create button sits inside the bar's height rather than matching it.
    // The clover's lobes push past its own bounds more than a circle does, so at
    // equal sizes it measured level and read taller — which is what put it out
    // of step with the rail in the first place.
    val createSize = 52.dp
    val shadowElevation = if (isLowEnd) 4.dp else 14.dp
    val shadowAlpha = if (isLowEnd) 0.08f else 0.14f

    Box(
        modifier = modifier
            .fillMaxWidth()
            .navigationBarsPadding()
            .padding(horizontal = 20.dp, vertical = 14.dp),
        contentAlignment = Alignment.Center
    ) {
        NebFabMenu(
            actions = menuActions,
            expanded = menuExpanded,
            onDismissRequest = onMenuDismiss
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                Row(
                    modifier = Modifier
                        .height(navHeight)
                        .shadow(
                            shadowElevation,
                            CircleShape,
                            clip = false,
                            ambientColor = Color.Black.copy(alpha = shadowAlpha),
                            spotColor = Color.Black.copy(alpha = shadowAlpha)
                        )
                        // Glass clips and rims itself, so it does not get the
                        // outer .clip: a stroke centred on a clipped path loses
                        // its outer half, and the rim is the edge of the
                        // material. The opaque path keeps both, unchanged.
                        .then(
                            if (glass) {
                                Modifier.nebLiquidGlass(
                                    backdrop = backdrop!!,
                                    shape = CircleShape,
                                    style = glassStyle,
                                    tier = glassTier
                                )
                            } else {
                                Modifier
                                    .clip(CircleShape)
                                    .background(barBrush)
                                    .border(1.dp, barBorder, CircleShape)
                            }
                        )
                        .padding(horizontal = 6.dp),
                    horizontalArrangement = Arrangement.spacedBy(4.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    items.forEach { item ->
                        val selected = currentRoute == item.route
                        GlassNavItem(item = item, selected = selected, onClick = { onSelect(item) })
                    }
                }

                if (onCreateClick != null) {
                    val tactile = rememberTactileFeedback()
                    val createInteractionSource = remember { MutableInteractionSource() }
                    val isCreatePressed by createInteractionSource.collectIsPressedAsState()
                    val createScale by animateFloatAsState(
                        targetValue = if (isCreatePressed) 0.90f else 1.0f,
                        animationSpec = spring(stiffness = Spring.StiffnessMediumLow),
                        label = "createScale"
                    )
                    val morph by animateFloatAsState(
                        targetValue = if (menuExpanded) 1f else 0f,
                        animationSpec = nebFastSpatialSpec(),
                        label = "createMorph"
                    )

                    // The create button is the one control on the bar that is not
                    // a circle or a rounded rectangle. It is Expressive's
                    // four-lobed clover — a scalloped polygon, so it reads as a
                    // deliberate object next to the pill-shaped nav rail rather
                    // than as one more round button.
                    //
                    // Opening the menu spins it 40 degrees. Because the
                    // lobes are not rotationally symmetric at that angle, the
                    // silhouette visibly reshapes itself on the way round: the
                    // shape does the morphing, and the glyph underneath only has
                    // to cross-fade from plus to close.
                    val createShape = nebShape(NebShapes.Create)
                    val shapeSpin = morph * 40f

                    Box(
                        modifier = Modifier
                            .size(createSize)
                            .graphicsLayer {
                                scaleX = createScale
                                scaleY = createScale
                                rotationZ = shapeSpin
                            }
                            // A neutral shadow. The old one was tinted with the
                            // primary at 35% and spread fourteen dp, which put a
                            // blue halo around the lobes and turned a button
                            // into a bloom.
                            .shadow(
                                shadowElevation,
                                createShape,
                                clip = false,
                                ambientColor = Color.Black.copy(alpha = shadowAlpha),
                                spotColor = Color.Black.copy(alpha = shadowAlpha + 0.06f)
                            )
                            .clip(createShape)
                            // Flat, not a gradient. Fading the fill to 86% alpha
                            // let the page through the bottom of the button, so
                            // the one element on the bar that should read as
                            // solid was the one that did not.
                            .background(primaryColor)
                            .clickable(
                                interactionSource = createInteractionSource,
                                indication = ripple(bounded = true, color = Color.White),
                                onClick = {
                                    tactile.perform(TactileType.ButtonTap)
                                    onCreateClick()
                                }
                            )
                            .testTag("bottom_nav_create_button"),
                        contentAlignment = Alignment.Center
                    ) {
                        Box(
                            modifier = Modifier
                                .size(26.dp)
                                // Cancel the container's spin so the glyph stays
                                // upright while the silhouette turns under it.
                                .graphicsLayer { rotationZ = -shapeSpin },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                painter = painterResource(id = R.drawable.ic_rune_plus),
                                contentDescription = if (menuExpanded) null else "Create",
                                tint = MaterialTheme.colorScheme.onPrimary,
                                modifier = Modifier
                                    .size(24.dp)
                                    .graphicsLayer {
                                        rotationZ = morph * 135f
                                        alpha = 1f - morph
                                    }
                            )
                            Icon(
                                imageVector = Icons.Rounded.Close,
                                contentDescription = if (menuExpanded) "Close create menu" else null,
                                tint = MaterialTheme.colorScheme.onPrimary,
                                modifier = Modifier
                                    .size(26.dp)
                                    .graphicsLayer {
                                        rotationZ = (1f - morph) * -135f
                                        alpha = morph
                                    }
                            )
                        }
                    }
                } else if (onProfileClick != null) {
                    val tactile = rememberTactileFeedback()
                    val profileInteractionSource = remember { MutableInteractionSource() }
                    val isProfilePressed by profileInteractionSource.collectIsPressedAsState()
                    val profileScale by animateFloatAsState(
                        targetValue = if (isProfilePressed) 0.92f else 1.0f,
                        animationSpec = spring(stiffness = Spring.StiffnessMediumLow),
                        label = "profileScale"
                    )

                    Box(
                        modifier = Modifier
                            .size(navHeight)
                            .graphicsLayer {
                                scaleX = profileScale
                                scaleY = profileScale
                            }
                            .shadow(
                                shadowElevation,
                                CircleShape,
                                clip = false,
                                ambientColor = Color.Black.copy(alpha = shadowAlpha),
                                spotColor = Color.Black.copy(alpha = shadowAlpha)
                            )
                            .clip(CircleShape)
                            .clickable(
                                interactionSource = profileInteractionSource,
                                indication = ripple(bounded = true),
                                onClick = {
                                    tactile.perform(TactileType.LightTap)
                                    onProfileClick()
                                }
                            ),
                        contentAlignment = Alignment.Center
                    ) {
                        NebAvatar(
                            photoUrl = photoUrl,
                            name = username.ifBlank { "User" },
                            size = navHeight,
                            ring = false,
                            showBorder = false
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun GlassNavItem(item: NebNavItem, selected: Boolean, onClick: () -> Unit) {
    val tactile = rememberTactileFeedback()
    val interactionSource = remember { MutableInteractionSource() }
    val isPressed by interactionSource.collectIsPressedAsState()
    val pressScale by animateFloatAsState(
        targetValue = if (isPressed) 0.92f else 1.0f,
        animationSpec = spring(stiffness = Spring.StiffnessMediumLow),
        label = "itemPressScale"
    )

    // The selected pill is the brand's own container, not the secondary one.
    // Secondary is the desaturated steel ramp, so the indicator and the create
    // button next to it were two unrelated blues sitting an inch apart — close
    // enough to compare, far enough apart to look like a mistake. They are one
    // family now, and the create button is the saturated end of it.
    val indicator by animateColorAsState(
        targetValue = if (selected) MaterialTheme.colorScheme.primaryContainer else Color.Transparent,
        animationSpec = spring(stiffness = Spring.StiffnessMediumLow),
        label = "indicator"
    )
    val contentColor by animateColorAsState(
        targetValue = if (selected) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurfaceVariant,
        animationSpec = tween(180),
        label = "navContent"
    )
    val hPad by animateDpAsState(
        targetValue = if (selected) 18.dp else 15.dp,
        animationSpec = spring(dampingRatio = Spring.DampingRatioLowBouncy, stiffness = Spring.StiffnessMediumLow),
        label = "navPad"
    )

    Row(
        modifier = Modifier
            .graphicsLayer {
                scaleX = pressScale
                scaleY = pressScale
            }
            .clip(CircleShape)
            .background(indicator)
            .clickable(
                interactionSource = interactionSource,
                indication = ripple(bounded = true, color = MaterialTheme.colorScheme.primary),
                onClick = {
                    tactile.perform(TactileType.SelectionChange)
                    onClick()
                }
            )
            .padding(horizontal = hPad, vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Icon(
            imageVector = if (selected) item.selectedIcon else item.unselectedIcon,
            contentDescription = item.label,
            tint = contentColor,
            modifier = Modifier.size(24.dp)
        )
        if (selected) {
            Text(
                text = item.label,
                color = contentColor,
                fontWeight = FontWeight.Bold,
                fontSize = 13.sp
            )
        }
    }
}

private fun Color.luminanceIsDark(): Boolean {
    val l = 0.299f * red + 0.587f * green + 0.114f * blue
    return l < 0.5f
}
