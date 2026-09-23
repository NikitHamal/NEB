package com.neb.ians.ui.components

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.background
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.InlineTextContent
import androidx.compose.foundation.text.appendInlineContent
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.text.ClickableText

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material3.Surface

/**
 * Lightweight markdown & LaTeX math renderer matching web formatting
 * (headings, bold, italic, inline code, code blocks, lists, blockquotes,
 * links, @mentions, LaTeX formulas \(...\), \[...\], $$...$$).
 *
 * Inline image tokens (`[[img:ID]]`) render as small tappable thumbnails
 * flowing with the text (Meta-style chips) via [rememberInlineImageContents].
 */
@Composable
fun MarkdownText(
    markdown: String,
    modifier: Modifier = Modifier,
    style: TextStyle = MaterialTheme.typography.bodyMedium,
    color: Color = MaterialTheme.colorScheme.onSurface,
    onMentionClick: (String) -> Unit = {},
    onLinkClick: (String) -> Unit = {},
    onInlineImageClick: (String) -> Unit = {}
) {
    val blocks = remember(markdown) { parseMarkdownBlocks(markdown) }
    val primary = MaterialTheme.colorScheme.primary
    val codeBg = MaterialTheme.colorScheme.surfaceContainerHigh
    val onSurfaceVariant = MaterialTheme.colorScheme.onSurfaceVariant
    val inlineContents = rememberInlineImageContents(markdown, onInlineImageClick)

    Column(modifier = modifier) {
        blocks.forEachIndexed { index, block ->
            if (index > 0) Spacer(modifier = Modifier.height(4.dp))
            when (block) {
                is MdBlock.Heading -> {
                    val headingStyle = when (block.level) {
                        1 -> MaterialTheme.typography.titleLarge
                        2 -> MaterialTheme.typography.titleMedium
                        else -> MaterialTheme.typography.titleSmall
                    }
                    InlineMdText(
                        text = block.text,
                        style = headingStyle.copy(fontWeight = FontWeight.Bold),
                        color = color,
                        primary = primary,
                        codeBg = codeBg,
                        onMentionClick = onMentionClick,
                        onLinkClick = onLinkClick,
                        inlineContents = inlineContents
                    )
                }
                is MdBlock.Quote -> {
                    Row(modifier = Modifier.fillMaxWidth()) {
                        Spacer(
                            modifier = Modifier
                                .width(3.dp)
                                .height(20.dp)
                                .background(primary.copy(alpha = 0.5f), RoundedCornerShape(2.dp))
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        if (hasLatexMath(block.text)) {
                            KaTeXText(
                                text = block.text,
                                style = style.copy(fontStyle = FontStyle.Italic),
                                color = onSurfaceVariant,
                                onLinkClick = onLinkClick,
                                modifier = Modifier.weight(1f)
                            )
                        } else {
                            InlineMdText(
                                text = block.text,
                                style = style.copy(fontStyle = FontStyle.Italic),
                                color = onSurfaceVariant,
                                primary = primary,
                                codeBg = codeBg,
                                onMentionClick = onMentionClick,
                                onLinkClick = onLinkClick,
                                inlineContents = inlineContents
                            )
                        }
                    }
                }
                is MdBlock.ListItem -> {
                    Row(modifier = Modifier.fillMaxWidth()) {
                        Text(
                            text = if (block.ordered) "${block.number}." else "\u2022",
                            style = style,
                            color = onSurfaceVariant,
                            modifier = Modifier.padding(end = 8.dp)
                        )
                        if (hasLatexMath(block.text)) {
                            KaTeXText(
                                text = block.text,
                                style = style,
                                color = color,
                                onLinkClick = onLinkClick,
                                modifier = Modifier.weight(1f)
                            )
                        } else {
                            InlineMdText(
                                text = block.text,
                                style = style,
                                color = color,
                                primary = primary,
                                codeBg = codeBg,
                                onMentionClick = onMentionClick,
                                onLinkClick = onLinkClick,
                                inlineContents = inlineContents
                            )
                        }
                    }
                }
                is MdBlock.CodeBlock -> {
                    Surface(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 4.dp),
                        shape = RoundedCornerShape(8.dp),
                        color = MaterialTheme.colorScheme.surfaceContainerHigh,
                        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
                    ) {
                        Column(modifier = Modifier.padding(10.dp)) {
                            if (block.language.isNotBlank()) {
                                Text(
                                    text = block.language.uppercase(),
                                    style = MaterialTheme.typography.labelSmall,
                                    fontWeight = FontWeight.Bold,
                                    color = primary
                                )
                                Spacer(modifier = Modifier.height(4.dp))
                            }
                            Text(
                                text = block.code,
                                style = TextStyle(fontFamily = FontFamily.Monospace, fontSize = 13.sp),
                                color = color,
                                modifier = Modifier.horizontalScroll(rememberScrollState())
                            )
                        }
                    }
                }
                is MdBlock.MathBlock -> {
                    Surface(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 4.dp),
                        shape = RoundedCornerShape(10.dp),
                        color = primary.copy(alpha = 0.05f),
                        border = BorderStroke(1.dp, primary.copy(alpha = 0.2f))
                    ) {
                        KaTeXMathView(
                            content = block.formula,
                            displayMode = true,
                            center = true,
                            textColor = color,
                            primaryColor = primary,
                            fontSizeSp = 15f,
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(horizontal = 10.dp, vertical = 6.dp)
                        )
                    }
                }
                is MdBlock.Paragraph -> {
                    if (hasLatexMath(block.text)) {
                        KaTeXText(
                            text = block.text,
                            style = style,
                            color = color,
                            onLinkClick = onLinkClick,
                            modifier = Modifier.fillMaxWidth()
                        )
                    } else {
                        InlineMdText(
                            text = block.text,
                            style = style,
                            color = color,
                            primary = primary,
                            codeBg = codeBg,
                            onMentionClick = onMentionClick,
                            onLinkClick = onLinkClick,
                            inlineContents = inlineContents
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun InlineMdText(
    text: String,
    style: TextStyle,
    color: Color,
    primary: Color,
    codeBg: Color,
    onMentionClick: (String) -> Unit,
    onLinkClick: (String) -> Unit,
    inlineContents: Map<String, InlineTextContent> = emptyMap<String, InlineTextContent>()
) {
    val errorBg = MaterialTheme.colorScheme.errorContainer
    val errorFg = MaterialTheme.colorScheme.onErrorContainer
    val formatted = remember(text) { formatLatexMath(text) }
    val annotated = remember(formatted, color, primary, codeBg, errorBg, errorFg) {
        buildInlineAnnotatedString(formatted, color, primary, codeBg, errorBg, errorFg)
    }
    NebAnnotatedText(
        text = annotated,
        style = style.copy(color = color),
        inlineContent = inlineContents,
        onClick = { offset ->
            annotated.getStringAnnotations("mention", offset, offset).firstOrNull()?.let {
                onMentionClick(it.item)
                return@NebAnnotatedText
            }
            annotated.getStringAnnotations("url", offset, offset).firstOrNull()?.let {
                onLinkClick(it.item)
            }
        }
    )
}

sealed class MdBlock {
    data class Heading(val level: Int, val text: String) : MdBlock()
    data class Quote(val text: String) : MdBlock()
    data class ListItem(val text: String, val ordered: Boolean, val number: Int) : MdBlock()
    data class CodeBlock(val language: String, val code: String) : MdBlock()
    data class MathBlock(val formula: String) : MdBlock()
    data class Paragraph(val text: String) : MdBlock()
}

internal fun parseMarkdownBlocks(markdown: String): List<MdBlock> {
    val blocks = mutableListOf<MdBlock>()
    var orderedIndex = 1
    val lines = markdown.replace("\r\n", "\n").split("\n")
    var i = 0
    while (i < lines.size) {
        val rawLine = lines[i]
        val line = rawLine.trimEnd()
        val trimmed = line.trim()

        if (trimmed.startsWith("```")) {
            val lang = trimmed.removePrefix("```").trim()
            val codeLines = mutableListOf<String>()
            i++
            while (i < lines.size && !lines[i].trim().startsWith("```")) {
                codeLines.add(lines[i])
                i++
            }
            blocks.add(MdBlock.CodeBlock(lang, codeLines.joinToString("\n")))
            i++
            continue
        }

        if (trimmed.startsWith("\\[")) {
            if (trimmed.endsWith("\\]") && trimmed.length > 3) {
                val formula = trimmed.removePrefix("\\[").removeSuffix("\\]").trim()
                blocks.add(MdBlock.MathBlock(formula))
                i++
                continue
            } else {
                val mathLines = mutableListOf<String>()
                val first = trimmed.removePrefix("\\[").trim()
                if (first.isNotEmpty()) mathLines.add(first)
                i++
                while (i < lines.size && !lines[i].trim().endsWith("\\]")) {
                    mathLines.add(lines[i])
                    i++
                }
                if (i < lines.size) {
                    val last = lines[i].trim().removeSuffix("\\]").trim()
                    if (last.isNotEmpty()) mathLines.add(last)
                    i++
                }
                blocks.add(MdBlock.MathBlock(mathLines.joinToString("\n")))
                continue
            }
        }

        if (trimmed.startsWith("$$")) {
            if (trimmed.endsWith("$$") && trimmed.length > 2) {
                val formula = trimmed.removePrefix("$$").removeSuffix("$$").trim()
                blocks.add(MdBlock.MathBlock(formula))
                i++
                continue
            } else {
                val mathLines = mutableListOf<String>()
                val first = trimmed.removePrefix("$$").trim()
                if (first.isNotEmpty()) mathLines.add(first)
                i++
                while (i < lines.size && !lines[i].trim().endsWith("$$")) {
                    mathLines.add(lines[i])
                    i++
                }
                if (i < lines.size) {
                    val last = lines[i].trim().removeSuffix("$$").trim()
                    if (last.isNotEmpty()) mathLines.add(last)
                    i++
                }
                blocks.add(MdBlock.MathBlock(mathLines.joinToString("\n")))
                continue
            }
        }

        if (trimmed.startsWith("\\begin{")) {
            val envMatch = Regex("""^\\begin\{([a-zA-Z*]+)\}""").find(trimmed)
            val env = envMatch?.groupValues?.get(1) ?: "equation"
            val mathLines = mutableListOf<String>()
            mathLines.add(trimmed)
            i++
            val endTag = "\\end{$env}"
            while (i < lines.size && !lines[i].trim().contains(endTag)) {
                mathLines.add(lines[i])
                i++
            }
            if (i < lines.size) {
                mathLines.add(lines[i])
                i++
            }
            blocks.add(MdBlock.MathBlock(mathLines.joinToString("\n")))
            continue
        }

        when {
            line.isBlank() -> {
                orderedIndex = 1
                blocks.add(MdBlock.Paragraph(""))
            }
            line.startsWith("### ") -> { orderedIndex = 1; blocks.add(MdBlock.Heading(3, line.removePrefix("### "))) }
            line.startsWith("## ") -> { orderedIndex = 1; blocks.add(MdBlock.Heading(2, line.removePrefix("## "))) }
            line.startsWith("# ") -> { orderedIndex = 1; blocks.add(MdBlock.Heading(1, line.removePrefix("# "))) }
            line.startsWith("> ") -> { orderedIndex = 1; blocks.add(MdBlock.Quote(line.removePrefix("> "))) }
            line.startsWith("- ") || line.startsWith("* ") -> {
                blocks.add(MdBlock.ListItem(line.substring(2), ordered = false, number = 0))
            }
            OrderedListPrefixRegex.containsMatchIn(line) -> {
                val text = line.replaceFirst(OrderedListPrefixRegex, "")
                blocks.add(MdBlock.ListItem(text, ordered = true, number = orderedIndex))
                orderedIndex++
            }
            else -> { orderedIndex = 1; blocks.add(MdBlock.Paragraph(line)) }
        }
        i++
    }
    // Collapse consecutive blank paragraphs
    val result = mutableListOf<MdBlock>()
    var lastBlank = false
    blocks.forEach { b ->
        val isBlank = b is MdBlock.Paragraph && b.text.isBlank()
        if (!(isBlank && lastBlank)) result.add(b)
        lastBlank = isBlank
    }
    while (result.isNotEmpty() && result.last() is MdBlock.Paragraph && (result.last() as MdBlock.Paragraph).text.isBlank()) {
        result.removeAt(result.lastIndex)
    }
    return result
}

private val OrderedListPrefixRegex = Regex("^\\d+\\.\\s")
private val LatexEnvRegex = Regex("""\\begin\{(?:equation|align|gather)\*?\}([\s\S]*?)\\end\{(?:equation|align|gather)\*?\}""")
private val LatexBlock1Regex = Regex("""\\\[([\s\S]*?)\\\]""")
private val LatexBlock2Regex = Regex("""\$\$([\s\S]*?)\$\$""")
private val LatexInline1Regex = Regex("""\\\(([\s\S]*?)\\\)""")
private val LatexInline2Regex = Regex("""(?<!\\)\$([^$\n]+)\$""")
private val MathFracRegex = Regex("""\\(?:d|t)?frac\{([^{}]+)\}\{([^{}]+)\}""")
private val MathSqrtNthRegex = Regex("""\\sqrt\[([^\]]+)\]\{([^{}]+)\}""")
private val MathSqrtRegex = Regex("""\\sqrt\{([^{}]+)\}""")
private val MathTextRegex = Regex("""\\(?:text|mathrm|mathbf|mathit|textbf|textit|operatorname)\{([^{}]+)\}""")
private val MathVecRegex = Regex("""\\vec\{([^{}]+)\}""")
private val MathVecSingleRegex = Regex("""\\vec\s+([a-zA-Z])""")
private val MathHatRegex = Regex("""\\hat\{([a-zA-Z])\}""")
private val MathBarRegex = Regex("""\\(?:overline|bar)\{([^{}]+)\}""")
private val MathDotRegex = Regex("""\\dot\{([^{}]+)\}""")
private val MathDdotRegex = Regex("""\\ddot\{([^{}]+)\}""")
private val MathSuperBracedRegex = Regex("""\^\{([^{}]+)\}""")
private val MathSubBracedRegex = Regex("""\_\{([^{}]+)\}""")
private val MathSuperSingleRegex = Regex("""\^([0-9a-zA-Z\+\-\=])""")
private val MathSubSingleRegex = Regex("""\_([0-9a-zA-Z\+\-\=])""")
private val PlainPreviewImageRegex = Regex("!\\[[^\\]]*\\]\\([^)]*\\)")
private val PlainPreviewLinkRegex = Regex("\\[([^\\]]+)\\]\\([^)]*\\)")
private val PlainPreviewMarksRegex = Regex("[*_~`#>]+")
private val PlainPreviewNewlinesRegex = Regex("\\n{2,}")
private val InlinePreviewImageRegex = Regex("!\\[[^]]*]\\([^)]*\\)")
private val InlineWhitespaceNewlinesRegex = Regex("\\s*\n+\\s*")

private val SuperscriptChars = mapOf(
    '0' to "⁰", '1' to "¹", '2' to "²", '3' to "³", '4' to "⁴",
    '5' to "⁵", '6' to "⁶", '7' to "⁷", '8' to "⁸", '9' to "⁹",
    '+' to "⁺", '-' to "⁻", '=' to "⁼", '(' to "⁽", ')' to "⁾",
    'n' to "ⁿ", 'i' to "ⁱ", 'x' to "ˣ", 'y' to "ʸ", 'a' to "ᵃ",
    'b' to "ᵇ", 'c' to "ᶜ", 'd' to "ᵈ", 'e' to "ᵉ", 'm' to "ᵐ",
    't' to "ᵗ", 'r' to "ʳ", 'k' to "ᵏ", 'p' to "ᵖ", 's' to "ˢ",
    'v' to "ᵛ", 'w' to "ʷ", 'o' to "ᵒ", 'T' to "ᵀ"
)

private fun toSuperscript(s: String): String {
    val trimmed = s.trim()
    if (trimmed == "\\circ" || trimmed == "\\degree") return "°"
    val sb = StringBuilder()
    for (ch in trimmed) {
        sb.append(SuperscriptChars[ch] ?: ch)
    }
    return sb.toString()
}

private val SubscriptChars = mapOf(
    '0' to "₀", '1' to "₁", '2' to "₂", '3' to "₃", '4' to "₄",
    '5' to "₅", '6' to "₆", '7' to "₇", '8' to "₈", '9' to "₉",
    '+' to "₊", '-' to "₋", '=' to "₌", '(' to "₍", ')' to "₎",
    'a' to "ₐ", 'e' to "ₑ", 'h' to "ₕ", 'i' to "ᵢ", 'j' to "ⱼ",
    'k' to "ₖ", 'l' to "ₗ", 'm' to "ₘ", 'n' to "ₙ", 'o' to "ₒ",
    'p' to "ₚ", 'r' to "ᵣ", 's' to "ₛ", 't' to "ₜ", 'u' to "ᵤ",
    'v' to "ᵥ", 'x' to "ₓ"
)

private fun toSubscript(s: String): String {
    val sb = StringBuilder()
    for (ch in s.trim()) {
        sb.append(SubscriptChars[ch] ?: ch)
    }
    return sb.toString()
}

fun formatLatexMath(input: String): String {
    if (input.isBlank()) return ""
    return runCatching {
        var text = input
        text = text.replace(LatexEnvRegex) { m ->
            "\n«m:" + formatMathExpression(m.groupValues[1].trim()) + "»\n"
        }
        text = text.replace(LatexBlock1Regex) { m ->
            "\n«m:" + formatMathExpression(m.groupValues[1].trim()) + "»\n"
        }.replace(LatexBlock2Regex) { m ->
            "\n«m:" + formatMathExpression(m.groupValues[1].trim()) + "»\n"
        }
        text = text.replace(LatexInline1Regex) { m ->
            "«m:" + formatMathExpression(m.groupValues[1].trim()) + "»"
        }.replace(LatexInline2Regex) { m ->
            "«m:" + formatMathExpression(m.groupValues[1].trim()) + "»"
        }
        val rawFormulaRegex = Regex("""(\\(?:int|sum|prod|frac|sqrt|lim)\b[^\n\.\,]+=[^\n\.\,]+)""")
        text = text.replace(rawFormulaRegex) { m ->
            "«m:" + formatMathExpression(m.value.trim()) + "»"
        }
        val integralEqRegex = Regex("""(∫\s*[^=\n]+=\s*[^,\.\n]+)""")
        text = text.replace(integralEqRegex) { m ->
            if (!m.value.contains("«m:")) "«m:" + formatMathExpression(m.value.trim()) + "»" else m.value
        }
        if (text.contains("\\frac") || text.contains("\\sqrt") || text.contains("\\alpha") ||
            text.contains("\\beta") || text.contains("\\theta") || text.contains("\\pi") ||
            text.contains("\\pm") || text.contains("\\times") || text.contains("\\int") ||
            text.contains("\\sum") || text.contains("\\vec") || text.contains("^{") || text.contains("_{")) {
            text = formatMathExpression(text)
        }
        text
    }.getOrDefault(input)
}

fun formatMathExpression(expr: String): String {
    if (expr.isBlank()) return ""
    return runCatching {
        var s = expr

        var prev = ""
        while (prev != s) {
            prev = s
            s = s.replace(MathTextRegex, "$1")
        }

        prev = ""
        while (prev != s) {
            prev = s
            s = s.replace(MathFracRegex) { m ->
                val num = m.groupValues[1].trim()
                val den = m.groupValues[2].trim()
                when {
                    num == "1" && den == "2" -> "½"
                    num == "1" && den == "4" -> "¼"
                    num == "3" && den == "4" -> "¾"
                    num == "1" && den == "3" -> "⅓"
                    num == "2" && den == "3" -> "⅔"
                    num.length <= 3 && den.length <= 3 && !num.contains(" ") && !den.contains(" ") -> "$num/$den"
                    else -> "($num)/($den)"
                }
            }
        }

        s = s.replace(MathSqrtNthRegex) { m ->
            val root = toSuperscript(m.groupValues[1])
            when (root) {
                "³" -> "∛(${m.groupValues[2]})"
                "⁴" -> "∜(${m.groupValues[2]})"
                else -> "${root}√(${m.groupValues[2]})"
            }
        }
        s = s.replace(MathSqrtRegex, "√($1)")
        s = s.replace("\\sqrt", "√")

        s = s.replace(MathSuperBracedRegex) { m -> toSuperscript(m.groupValues[1]) }
        s = s.replace(MathSubBracedRegex) { m -> toSubscript(m.groupValues[1]) }
        s = s.replace(MathSuperSingleRegex) { m -> toSuperscript(m.groupValues[1]) }
        s = s.replace(MathSubSingleRegex) { m -> toSubscript(m.groupValues[1]) }

        s = s.replace(MathVecRegex, "$1⃗")
        s = s.replace(MathVecSingleRegex, "$1⃗")
        s = s.replace(MathHatRegex) { m ->
            when (m.groupValues[1]) {
                "i" -> "î"
                "j" -> "ĵ"
                "k" -> "k̂"
                else -> "${m.groupValues[1]}̂"
            }
        }
        s = s.replace(MathBarRegex, "$1̅")
        s = s.replace(MathDotRegex, "$1̇")
        s = s.replace(MathDdotRegex, "$1̈")

        s = s.replace("\\iint", "∬")
            .replace("\\iiint", "∭")
            .replace("\\oint", "∮")
            .replace("\\int", "∫")
            .replace("\\sum", "∑")
            .replace("\\prod", "∏")
            .replace("\\lim", "lim")
            .replace("\\partial", "∂")
            .replace("\\nabla", "∇")
            .replace("\\infty", "∞")

        s = s.replace("\\alpha", "α")
            .replace("\\beta", "β")
            .replace("\\gamma", "γ")
            .replace("\\delta", "δ")
            .replace("\\epsilon", "ε")
            .replace("\\varepsilon", "ε")
            .replace("\\zeta", "ζ")
            .replace("\\eta", "η")
            .replace("\\theta", "θ")
            .replace("\\vartheta", "θ")
            .replace("\\iota", "ι")
            .replace("\\kappa", "κ")
            .replace("\\lambda", "λ")
            .replace("\\mu", "μ")
            .replace("\\nu", "ν")
            .replace("\\xi", "ξ")
            .replace("\\pi", "π")
            .replace("\\varpi", "ϖ")
            .replace("\\rho", "ρ")
            .replace("\\varrho", "ϱ")
            .replace("\\sigma", "σ")
            .replace("\\varsigma", "ς")
            .replace("\\tau", "τ")
            .replace("\\upsilon", "υ")
            .replace("\\phi", "φ")
            .replace("\\varphi", "φ")
            .replace("\\chi", "χ")
            .replace("\\psi", "ψ")
            .replace("\\omega", "ω")

        s = s.replace("\\Gamma", "Γ")
            .replace("\\Delta", "Δ")
            .replace("\\Theta", "Θ")
            .replace("\\Lambda", "Λ")
            .replace("\\Xi", "Ξ")
            .replace("\\Pi", "Π")
            .replace("\\Sigma", "Σ")
            .replace("\\Upsilon", "Υ")
            .replace("\\Phi", "Φ")
            .replace("\\Psi", "Ψ")
            .replace("\\Omega", "Ω")

        s = s.replace("\\times", "×")
            .replace("\\cdot", "·")
            .replace("\\div", "÷")
            .replace("\\pm", "±")
            .replace("\\mp", "∓")
            .replace("\\bullet", "•")
            .replace("\\circ", "∘")
            .replace("\\degree", "°")
            .replace("\\approx", "≈")
            .replace("\\equiv", "≡")
            .replace("\\sim", "∼")
            .replace("\\propto", "∝")
            .replace("\\leq", "≤")
            .replace("\\le", "≤")
            .replace("\\geq", "≥")
            .replace("\\ge", "≥")
            .replace("\\neq", "≠")
            .replace("\\ne", "≠")
            .replace("\\ll", "≪")
            .replace("\\gg", "≫")

        s = s.replace("\\rightarrow", "→")
            .replace("\\to", "→")
            .replace("\\leftarrow", "←")
            .replace("\\gets", "←")
            .replace("\\Rightarrow", "⇒")
            .replace("\\implies", "⇒")
            .replace("\\Leftarrow", "⇐")
            .replace("\\Leftrightarrow", "⇔")
            .replace("\\iff", "⇔")
            .replace("\\leftrightarrow", "↔")
            .replace("\\uparrow", "↑")
            .replace("\\downarrow", "↓")
            .replace("\\rightleftharpoons", "⇌")

        s = s.replace("\\in", "∈")
            .replace("\\notin", "∉")
            .replace("\\subset", "⊂")
            .replace("\\subseteq", "⊆")
            .replace("\\supset", "⊃")
            .replace("\\supseteq", "⊇")
            .replace("\\cap", "∩")
            .replace("\\cup", "∪")
            .replace("\\setminus", "\\")
            .replace("\\forall", "∀")
            .replace("\\exists", "∃")
            .replace("\\emptyset", "∅")
            .replace("\\varnothing", "∅")

        s = s.replace("\\triangle", "△")
            .replace("\\angle", "∠")
            .replace("\\perp", "⊥")
            .replace("\\parallel", "∥")

        s = s.replace("\\left(", "(")
            .replace("\\right)", ")")
            .replace("\\left[", "[")
            .replace("\\right]", "]")
            .replace("\\left\\{", "{")
            .replace("\\right\\}", "}")
            .replace("\\left|", "|")
            .replace("\\right|", "|")
            .replace("\\{", "{")
            .replace("\\}", "}")

        s = s.replace(Regex("""\\(sin|cos|tan|cot|sec|csc|arcsin|arccos|arctan|ln|log|exp|det|max|min)"""), "$1")

        s = s.replace("\\quad", " ")
            .replace("\\qquad", " ")
            .replace(Regex("""\\[,;:!]\s*"""), " ")
            .replace("\\\\", " ")
            .replace(Regex("""[ \t]{2,}"""), " ")
            .trim()

        s
    }.getOrDefault(expr)
}

private val inlinePattern = Regex(
    "(\\*\\*([^*]+)\\*\\*)" +          // 1,2 bold
        "|(\\*([^*]+)\\*)" +            // 3,4 italic
        "|(`([^`]+)`)" +                // 5,6 code
        "|(~~([^~]+)~~)" +              // 7,8 strikethrough
        "|(\\[([^\\]]+)\\]\\(([^)]+)\\))" + // 9,10,11 link
        "|(@([A-Za-z0-9_]+))" +          // 12,13 mention
        "|((https?://[^\\s]+|www\\.[^\\s]+))" + // 14 bare url
        "|(«m:([^»]+)»)"                // 15,16 math formula
)

internal fun buildInlineAnnotatedString(
    text: String,
    baseColor: Color,
    primary: Color,
    codeBg: Color,
    errorBg: Color = Color(0xFFFFD8E4),
    errorFg: Color = Color(0xFF31111D)
): AnnotatedString {
    // Inline image tokens are emitted as inline-content placeholders; the
    // remaining markdown styling runs per text segment between tokens.
    if (!text.contains("[[img:")) {
        return buildAnnotatedString { appendStyledSegment(text, primary, codeBg, errorBg, errorFg) }
    }
    return buildAnnotatedString {
        var cursor = 0
        InlineImageTokens.REGEX.findAll(text).forEach { tokenMatch ->
            if (tokenMatch.range.first > cursor) {
                appendStyledSegment(
                    text.substring(cursor, tokenMatch.range.first),
                    primary, codeBg, errorBg, errorFg
                )
            }
            val id = tokenMatch.groupValues[1].toIntOrNull()
            if (id != null) appendInlineContent(INLINE_IMG_PREFIX + id, "[image]")
            cursor = tokenMatch.range.last + 1
        }
        if (cursor < text.length) {
            appendStyledSegment(text.substring(cursor), primary, codeBg, errorBg, errorFg)
        }
    }
}

private fun androidx.compose.ui.text.AnnotatedString.Builder.appendStyledSegment(
    segment: String,
    primary: Color,
    codeBg: Color,
    errorBg: Color,
    errorFg: Color
) {
    if (segment.isEmpty()) return
    var cursor = 0
    inlinePattern.findAll(segment).forEach { match ->
        if (match.range.first > cursor) {
            append(segment.substring(cursor, match.range.first))
        }
        val g = match.groups
        when {
            g[2] != null -> withStyleAppend(SpanStyle(fontWeight = FontWeight.Bold), g[2]!!.value)
            g[4] != null -> withStyleAppend(SpanStyle(fontStyle = FontStyle.Italic), g[4]!!.value)
            g[6] != null -> withStyleAppend(
                SpanStyle(fontFamily = FontFamily.Monospace, background = codeBg, fontSize = 13.sp),
                g[6]!!.value
            )
            g[8] != null -> withStyleAppend(SpanStyle(textDecoration = TextDecoration.LineThrough), g[8]!!.value)
            g[10] != null && g[11] != null -> {
                pushStringAnnotation("url", g[11]!!.value)
                withStyleAppend(SpanStyle(color = primary, textDecoration = TextDecoration.Underline), g[10]!!.value)
                pop()
            }
            g[13] != null -> {
                val isAll = g[13]!!.value.equals("all", ignoreCase = true)
                if (isAll) {
                    withStyleAppend(
                        SpanStyle(background = errorBg, color = errorFg, fontWeight = FontWeight.Bold),
                        "@all"
                    )
                } else {
                    pushStringAnnotation("mention", g[13]!!.value)
                    withStyleAppend(SpanStyle(color = primary, fontWeight = FontWeight.Medium), "@${g[13]!!.value}")
                    pop()
                }
            }
            g[14] != null -> {
                val raw = g[14]!!.value.trimEnd('.', ',', ';', ':', '!', '?', ')')
                if (raw.isNotEmpty()) {
                    val href = if (raw.startsWith("http", ignoreCase = true)) raw else "http://$raw"
                    pushStringAnnotation("url", href)
                    withStyleAppend(SpanStyle(color = primary, textDecoration = TextDecoration.Underline), raw)
                    pop()
                } else {
                    append(g[14]!!.value)
                }
            }
            g[16] != null -> {
                withStyleAppend(
                    SpanStyle(
                        fontFamily = androidx.compose.ui.text.font.FontFamily.Serif,
                        fontStyle = FontStyle.Italic,
                        fontWeight = FontWeight.Medium,
                        color = primary,
                        background = primary.copy(alpha = 0.08f)
                    ),
                    " " + g[16]!!.value.trim() + " "
                )
            }
        }
        cursor = match.range.last + 1
    }
    if (cursor < segment.length) append(segment.substring(cursor))
}

private fun androidx.compose.ui.text.AnnotatedString.Builder.withStyleAppend(style: SpanStyle, text: String) {
    pushStyle(style)
    append(text)
    pop()
}

/** Strip markdown markers for inline previews (post cards). Mirrors web render_content_inline. */
fun markdownToPlainPreview(markdown: String): String {
    return InlineImageTokens.plainText(markdown)
        .replace(PlainPreviewImageRegex, "")
        .replace(PlainPreviewLinkRegex, "$1")
        .replace(PlainPreviewMarksRegex, "")
        .replace(PlainPreviewNewlinesRegex, "\n")
        .trim()
}

@Composable
fun ExpandableMarkdownText(
    markdown: String,
    modifier: Modifier = Modifier,
    style: TextStyle = MaterialTheme.typography.bodyMedium,
    color: Color = MaterialTheme.colorScheme.onSurface,
    onMentionClick: (String) -> Unit = {},
    onLinkClick: (String) -> Unit = {},
    minimizedMaxLines: Int = 3,
    onInlineImageClick: (String) -> Unit = {}
) {
    var isExpanded by remember { mutableStateOf(false) }
    var hasOverflow by remember { mutableStateOf(false) }

    Column(modifier = modifier) {
        if (isExpanded) {
            MarkdownText(
                markdown = markdown,
                style = style,
                color = color,
                onMentionClick = onMentionClick,
                onLinkClick = onLinkClick,
                onInlineImageClick = onInlineImageClick
            )
        } else {
            // Collapsed preview stays fully formatted: block structure is
            // flattened but inline markdown (bold, italic, code, strike,
            // colored/links and highlighted @mentions) keeps rendering, so
            // the preview never looks like raw unprocessed text.
            val flatText = remember(markdown) { markdownToInlinePreview(markdown, stripTokens = false) }
            val primary = MaterialTheme.colorScheme.primary
            val codeBg = MaterialTheme.colorScheme.surfaceContainerHigh
            val errorBg = MaterialTheme.colorScheme.errorContainer
            val errorFg = MaterialTheme.colorScheme.onErrorContainer
            val annotated = remember(flatText, color, primary, codeBg, errorBg, errorFg) {
                buildInlineAnnotatedString(flatText, color, primary, codeBg, errorBg, errorFg)
            }
            val inlineContents = rememberInlineImageContents(flatText, onInlineImageClick)
            NebAnnotatedText(
                text = annotated,
                style = style.copy(color = color),
                inlineContent = inlineContents,
                maxLines = minimizedMaxLines,
                overflow = TextOverflow.Ellipsis,
                onTextLayout = { textLayoutResult ->
                    hasOverflow = textLayoutResult.hasVisualOverflow
                },
                onClick = { offset ->
                    annotated.getStringAnnotations("mention", offset, offset).firstOrNull()?.let {
                        onMentionClick(it.item)
                        return@NebAnnotatedText
                    }
                    annotated.getStringAnnotations("url", offset, offset).firstOrNull()?.let {
                        onLinkClick(it.item)
                    }
                }
            )
        }
        if (hasOverflow || isExpanded) {
            Spacer(modifier = Modifier.height(2.dp))
            Text(
                text = if (isExpanded) "See less" else "See more",
                style = style.copy(fontWeight = FontWeight.SemiBold),
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier.clickable(
                    interactionSource = remember { MutableInteractionSource() },
                    indication = null,
                    onClick = { isExpanded = !isExpanded }
                )
            )
        }
    }
}

/**
 * Flatten markdown blocks into a single flow of text for collapsed previews,
 * keeping inline markers so [buildInlineAnnotatedString] can still style
 * bold/italic/code/links/mentions. Block markers become readable bullets.
 */
private val inlinePreviewCache = android.util.LruCache<Pair<String, Boolean>, String>(256)

fun markdownToInlinePreview(markdown: String, stripTokens: Boolean = true): String {
    if (markdown.isBlank()) return ""
    val cacheKey = Pair(markdown, stripTokens)
    inlinePreviewCache.get(cacheKey)?.let { return it }
    val parsed = parseMarkdownBlocks(markdown).joinToString("\n") { block ->
        when (block) {
            is MdBlock.Heading -> formatLatexMath(block.text)
            is MdBlock.Quote -> formatLatexMath(block.text)
            is MdBlock.ListItem -> (if (block.ordered) "${block.number}. " else "• ") + formatLatexMath(block.text)
            is MdBlock.CodeBlock -> block.code
            is MdBlock.MathBlock -> "«m:" + formatMathExpression(block.formula) + "»"
            is MdBlock.Paragraph -> formatLatexMath(block.text)
        }
    }.replace(InlinePreviewImageRegex, "").let { if (stripTokens) InlineImageTokens.plainText(it) else it }.trim()
    val result = formatLatexMath(parsed)
    inlinePreviewCache.put(cacheKey, result)
    return result
}

/**
 * Compact single-flow inline markdown for cards (suggested feed, lists):
 * bold/italic/inline-code/strikethrough/links/@mentions rendered inline like
 * the full [MarkdownText], but collapsed to one ellipsizable Text with
 * newlines folded — perfect for 2-line excerpts.
 */
@Composable
fun MarkdownInlineText(
    markdown: String,
    style: TextStyle,
    color: Color,
    modifier: Modifier = Modifier,
    maxLines: Int = Int.MAX_VALUE,
    onMentionClick: (String) -> Unit = {},
    onLinkClick: (String) -> Unit = {},
    onInlineImageClick: (String) -> Unit = {}
) {
    val primary = MaterialTheme.colorScheme.primary
    val codeBg = MaterialTheme.colorScheme.surfaceContainerHigh
    val errorBg = MaterialTheme.colorScheme.errorContainer
    val errorFg = MaterialTheme.colorScheme.onErrorContainer
    val flattened = remember(markdown) {
        markdown.replace(InlineWhitespaceNewlinesRegex, " ").trim()
    }
    if (flattened.isEmpty()) return
    val annotated = remember(flattened, color, primary, codeBg, errorBg, errorFg) {
        buildInlineAnnotatedString(flattened, color, primary, codeBg, errorBg, errorFg)
    }
    val inlineContents = rememberInlineImageContents(flattened, onInlineImageClick)
    NebAnnotatedText(
        text = annotated,
        modifier = modifier,
        style = style.copy(color = color),
        inlineContent = inlineContents,
        overflow = TextOverflow.Ellipsis,
        maxLines = maxLines,
        onClick = { offset ->
            annotated.getStringAnnotations("mention", offset, offset).firstOrNull()?.let {
                onMentionClick(it.item)
                return@NebAnnotatedText
            }
            annotated.getStringAnnotations("url", offset, offset).firstOrNull()?.let {
                onLinkClick(it.item)
            }
        }
    )
}
