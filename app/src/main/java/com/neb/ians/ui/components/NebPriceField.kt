@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material.icons.outlined.Payments
import androidx.compose.material.icons.outlined.Public
import androidx.compose.material.icons.outlined.Sell
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebSpatialSpec
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.ui.draw.scale

private val pricePresets = listOf(99, 149, 199, 499, 999)

/**
 * The one price control: uploading a resource, editing one, and pricing a course
 * in the marketplace studio all show this.
 *
 * Free or paid is a two-answer choice with the consequence written under it, the
 * amount is a real field, and the presets are the prices Nepali students actually
 * pay for notes. The line under the field is the point of the component: it says
 * what the seller keeps, before they commit, instead of after.
 *
 * [commissionPercent] comes from the server's PaymentConfig so web and app can
 * never quote different fees.
 */
@Composable
fun NebPriceField(
    isPaid: Boolean,
    price: String,
    onIsPaidChange: (Boolean) -> Unit,
    onPriceChange: (String) -> Unit,
    modifier: Modifier = Modifier,
    commissionPercent: Double = 2.5,
    title: String = "Sell this resource",
    subtitle: String = "Buyers pay once by QR. You keep every sale after the platform fee, credited to your wallet once our team verifies the payment.",
    tone: NebPriceTone = NebPriceTone.Mono
) {
    val accent = when (tone) {
        NebPriceTone.Mono -> MaterialTheme.colorScheme.onSurface
        NebPriceTone.Brand -> MaterialTheme.colorScheme.primary
    }
    val shape = WebPanelShape
    val priceValue = price.toDoubleOrNull() ?: 0.0

    Column(
        modifier = modifier
            .fillMaxWidth()
            .clip(shape)
            .background(MaterialTheme.colorScheme.surfaceContainerLow)
            .border(1.dp, MaterialTheme.colorScheme.outlineVariant, shape)
            .padding(14.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Row(verticalAlignment = Alignment.Top, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            Icon(
                imageVector = Icons.Outlined.Sell,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.size(20.dp)
            )
            Column(modifier = Modifier.weight(1f)) {
                Text(title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
                Spacer(Modifier.height(2.dp))
                Text(
                    subtitle,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }

        Row(
            modifier = Modifier
                .fillMaxWidth()
                .clip(WebCardShape)
                .background(MaterialTheme.colorScheme.surfaceContainer)
                .padding(4.dp),
            horizontalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            PriceModeTile(
                label = "Free",
                detail = "Open to every Nebian",
                icon = Icons.Outlined.Public,
                selected = !isPaid,
                accent = accent,
                modifier = Modifier.weight(1f),
                onClick = { onIsPaidChange(false) }
            )
            PriceModeTile(
                label = "Paid",
                detail = "Earn from every unlock",
                icon = Icons.Outlined.Payments,
                selected = isPaid,
                accent = accent,
                modifier = Modifier.weight(1f),
                onClick = { onIsPaidChange(true) }
            )
        }

        AnimatedVisibility(visible = isPaid) {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                OutlinedTextField(
                    value = price,
                    onValueChange = { raw ->
                        onPriceChange(raw.filter { it.isDigit() || it == '.' }.take(9))
                    },
                    modifier = Modifier.fillMaxWidth(),
                    label = { Text("Price in NPR (Rs.)", maxLines = 1) },
                    placeholder = { Text("199", maxLines = 1) },
                    prefix = { Text("Rs.", fontWeight = FontWeight.SemiBold) },
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                    singleLine = true,
                    isError = priceValue <= 0.0
                )

                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    pricePresets.forEach { preset ->
                        val chosen = priceValue > 0 && priceValue == preset.toDouble()
                        NebChip(
                            label = "Rs. $preset",
                            selected = chosen,
                            onClick = { onPriceChange(preset.toString()) }
                        )
                    }
                }

                Surface(
                    shape = WebCardShape,
                    color = MaterialTheme.colorScheme.surfaceContainerLowest,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 8.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.Info,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.size(15.dp)
                        )
                        Text(
                            text = earningsLine(priceValue, commissionPercent),
                            style = MaterialTheme.typography.labelMedium,
                            fontWeight = FontWeight.SemiBold,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                    }
                }

                Text(
                    text = "Paid unlocks are verified by the NEBians team from the buyer's transaction reference or screenshot. Withdrawals open at Rs. 1,000.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}

/** Where the price control's accent comes from. Studio/pages may pass their own. */
enum class NebPriceTone { Mono, Brand }

@Composable
private fun PriceModeTile(
    label: String,
    detail: String,
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    selected: Boolean,
    accent: Color,
    modifier: Modifier = Modifier,
    onClick: () -> Unit
) {
    val container by animateColorAsState(
        targetValue = if (selected) MaterialTheme.colorScheme.surfaceContainerLowest else Color.Transparent,
        animationSpec = nebEffectsSpec(),
        label = "price_mode_bg"
    )
    val content by animateColorAsState(
        targetValue = if (selected) accent else MaterialTheme.colorScheme.onSurfaceVariant,
        animationSpec = nebEffectsSpec(),
        label = "price_mode_fg"
    )
    val scale by animateFloatAsState(
        targetValue = if (selected) 1f else 0.985f,
        animationSpec = nebSpatialSpec(),
        label = "price_mode_scale"
    )

    Row(
        modifier = modifier
            .scale(scale)
            .heightIn(min = 56.dp)
            .clip(WebCardShape)
            .background(container)
            .clickable(onClick = onClick)
            .padding(horizontal = 10.dp, vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Icon(icon, contentDescription = null, tint = content, modifier = Modifier.size(18.dp))
        Column {
            Text(
                text = label,
                style = MaterialTheme.typography.labelLarge,
                fontWeight = FontWeight.SemiBold,
                color = content
            )
            Text(
                text = detail,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1
            )
        }
    }
}

/** What the seller keeps on one sale, written the way a shop writes it. */
private fun earningsLine(price: Double, commissionPercent: Double): String {
    if (price <= 0.0) return "Enter a price above Rs. 0"
    val keeps = price - (price * commissionPercent) / 100.0
    val rounded = Math.round(keeps * 100.0) / 100.0
    val keepsText = if (rounded == Math.floor(rounded)) rounded.toLong().toString() else String.format("%.2f", rounded)
    val feeText = if (commissionPercent == Math.floor(commissionPercent)) {
        commissionPercent.toLong().toString()
    } else {
        commissionPercent.toString()
    }
    return "You receive Rs. $keepsText per sale after the $feeText% platform fee"
}

/** A compact read-only price badge, for cards and sheets that only display. */
@Composable
fun NebPriceBadge(price: String, isFree: Boolean, modifier: Modifier = Modifier) {
    val text = if (isFree) "Free" else "Rs. ${price.ifBlank { "0" }}"
    val container = if (isFree) MaterialTheme.colorScheme.surfaceContainerHighest else MaterialTheme.colorScheme.onSurface
    val content = if (isFree) MaterialTheme.colorScheme.onSurfaceVariant else MaterialTheme.colorScheme.surface

    Box(
        modifier = modifier
            .clip(CircleShape)
            .background(container)
            .padding(horizontal = 10.dp, vertical = 4.dp)
    ) {
        Text(
            text = text,
            style = MaterialTheme.typography.labelMedium,
            fontWeight = FontWeight.Bold,
            color = content
        )
    }
}

/** A section label with the studio's small grey voice, used by the editors. */
@Composable
fun NebFieldHint(text: String, modifier: Modifier = Modifier) {
    Text(
        text = text,
        style = MaterialTheme.typography.bodySmall,
        color = MaterialTheme.colorScheme.onSurfaceVariant,
        modifier = modifier
    )
}
