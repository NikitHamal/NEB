package com.consica.code.runtime.python

/**
 * MiniPython — a small, fully offline Python interpreter written in Kotlin.
 *
 * Supports the beginner-to-intermediate subset taught by Consica Code:
 *  - numbers (int/float), strings, booleans, None, lists
 *  - variables and augmented assignment (+=, -=, *=, /=)
 *  - arithmetic (+ - * / // % **), comparisons, and/or/not
 *  - if / elif / else, while, for-in (range, lists, strings)
 *  - functions with parameters and return values
 *  - built-ins: print, len, range, str, int, float, abs, min, max, sum, sorted, input
 *  - list methods: append, pop; string methods: upper, lower, strip
 *  - break / continue / pass, comments
 *
 * Execution is sandboxed: bounded step count, bounded output and no I/O —
 * everything runs on-device with no network or filesystem access.
 */
object MiniPython {

    private const val MAX_STEPS = 200_000
    private const val MAX_OUTPUT_CHARS = 20_000

    data class ExecResult(
        val output: String,
        val error: PyError? = null,
    ) {
        val success: Boolean get() = error == null
    }

    data class PyError(
        val kind: String,
        val message: String,
        val line: Int?,
    ) {
        fun describe(): String = if (line != null) "$kind (line $line): $message" else "$kind: $message"
    }

    fun run(source: String, stdinValue: String = ""): ExecResult {
        val out = StringBuilder()
        return try {
            val program = Parser(source).parseProgram()
            val interp = Interpreter(out, stdinValue)
            interp.execBlock(program, Scope(null))
            ExecResult(out.toString())
        } catch (e: PyException) {
            ExecResult(out.toString(), e.toError())
        } catch (e: Exception) {
            ExecResult(out.toString(), PyError("InternalError", e.message ?: "unexpected failure", null))
        }
    }

    // ------------------------------------------------------------------
    // Errors
    // ------------------------------------------------------------------

    private class PyException(
        val kind: String,
        message: String,
        val line: Int?,
    ) : Exception(message) {
        fun toError() = PyError(kind, message ?: "", line)
    }

    private fun err(kind: String, message: String, line: Int?): Nothing =
        throw PyException(kind, message, line)

    // Control-flow signals
    private class BreakSignal : Exception()
    private class ContinueSignal : Exception()
    private class ReturnSignal(val value: Any?) : Exception()

    // ------------------------------------------------------------------
    // AST
    // ------------------------------------------------------------------

    private sealed class Stmt { abstract val line: Int }
    private class SExpr(override val line: Int, val expr: Expr) : Stmt()
    private class SAssign(override val line: Int, val target: Expr, val op: String?, val value: Expr) : Stmt()
    private class SIf(
        override val line: Int,
        val branches: List<Pair<Expr, List<Stmt>>>,
        val elseBody: List<Stmt>?,
    ) : Stmt()
    private class SWhile(override val line: Int, val cond: Expr, val body: List<Stmt>) : Stmt()
    private class SFor(override val line: Int, val varName: String, val iterable: Expr, val body: List<Stmt>) : Stmt()
    private class SDef(override val line: Int, val name: String, val params: List<String>, val body: List<Stmt>) : Stmt()
    private class SReturn(override val line: Int, val value: Expr?) : Stmt()
    private class SBreak(override val line: Int) : Stmt()
    private class SContinue(override val line: Int) : Stmt()
    private class SPass(override val line: Int) : Stmt()

    private sealed class Expr { abstract val line: Int }
    private class ENum(override val line: Int, val value: Any) : Expr() // Long or Double
    private class EStr(override val line: Int, val value: String) : Expr()
    private class EBool(override val line: Int, val value: Boolean) : Expr()
    private class ENone(override val line: Int) : Expr()
    private class EName(override val line: Int, val name: String) : Expr()
    private class EList(override val line: Int, val items: List<Expr>) : Expr()
    private class EIndex(override val line: Int, val target: Expr, val index: Expr) : Expr()
    private class ECall(override val line: Int, val target: Expr, val args: List<Expr>) : Expr()
    private class EAttr(override val line: Int, val target: Expr, val name: String) : Expr()
    private class EBin(override val line: Int, val op: String, val left: Expr, val right: Expr) : Expr()
    private class EUnary(override val line: Int, val op: String, val operand: Expr) : Expr()

    // ------------------------------------------------------------------
    // Tokenizer (per logical line)
    // ------------------------------------------------------------------

    private data class Token(val type: TokType, val text: String, val line: Int)

    private enum class TokType { NUMBER, STRING, NAME, OP, EOF }

    private class Lexer(private val text: String, private val line: Int) {
        private var pos = 0
        private val tokens = mutableListOf<Token>()

        fun tokenize(): List<Token> {
            while (pos < text.length) {
                val c = text[pos]
                when {
                    c == ' ' || c == '\t' -> pos++
                    c == '#' -> break
                    c.isDigit() || (c == '.' && pos + 1 < text.length && text[pos + 1].isDigit()) -> number()
                    c == '"' || c == '\'' -> string(c)
                    c.isLetter() || c == '_' -> name()
                    else -> op()
                }
            }
            tokens += Token(TokType.EOF, "", line)
            return tokens
        }

        private fun number() {
            val start = pos
            var hasDot = false
            while (pos < text.length && (text[pos].isDigit() || (text[pos] == '.' && !hasDot))) {
                if (text[pos] == '.') hasDot = true
                pos++
            }
            tokens += Token(TokType.NUMBER, text.substring(start, pos), line)
        }

        private fun string(quote: Char) {
            pos++ // opening quote
            val sb = StringBuilder()
            while (pos < text.length && text[pos] != quote) {
                if (text[pos] == '\\' && pos + 1 < text.length) {
                    pos++
                    sb.append(
                        when (text[pos]) {
                            'n' -> '\n'
                            't' -> '\t'
                            '\\' -> '\\'
                            '\'' -> '\''
                            '"' -> '"'
                            else -> text[pos]
                        },
                    )
                } else {
                    sb.append(text[pos])
                }
                pos++
            }
            if (pos >= text.length) err("SyntaxError", "unterminated string", line)
            pos++ // closing quote
            tokens += Token(TokType.STRING, sb.toString(), line)
        }

        private fun name() {
            val start = pos
            while (pos < text.length && (text[pos].isLetterOrDigit() || text[pos] == '_')) pos++
            tokens += Token(TokType.NAME, text.substring(start, pos), line)
        }

        private fun op() {
            val two = if (pos + 1 < text.length) text.substring(pos, pos + 2) else ""
            val twoOps = setOf("==", "!=", "<=", ">=", "//", "**", "+=", "-=", "*=", "/=")
            if (two in twoOps) {
                tokens += Token(TokType.OP, two, line)
                pos += 2
                return
            }
            val c = text[pos]
            val singles = "+-*/%<>=()[]{},.:"
            if (singles.indexOf(c) >= 0) {
                tokens += Token(TokType.OP, c.toString(), line)
                pos++
            } else {
                err("SyntaxError", "unexpected character '$c'", line)
            }
        }
    }

    // ------------------------------------------------------------------
    // Parser
    // ------------------------------------------------------------------

    private class LogicalLine(val indent: Int, val tokens: List<Token>, val line: Int)

    private class Parser(source: String) {
        private val lines: List<LogicalLine>
        private var index = 0

        init {
            val result = mutableListOf<LogicalLine>()
            val raw = source.replace("\r\n", "\n").replace('\r', '\n').split('\n')
            raw.forEachIndexed { i, rawLine ->
                val lineNo = i + 1
                val stripped = rawLine.trimEnd()
                val contentStart = stripped.indexOfFirst { it != ' ' && it != '\t' }
                if (contentStart == -1) return@forEachIndexed // blank
                val content = stripped.substring(contentStart)
                if (content.startsWith("#")) return@forEachIndexed
                var indent = 0
                for (ch in stripped.substring(0, contentStart)) {
                    indent += if (ch == '\t') 4 else 1
                }
                val toks = Lexer(content, lineNo).tokenize()
                if (toks.size > 1) result += LogicalLine(indent, toks, lineNo)
            }
            lines = result
        }

        fun parseProgram(): List<Stmt> = parseBlock(0)

        private fun parseBlock(minIndent: Int): List<Stmt> {
            val stmts = mutableListOf<Stmt>()
            val blockIndent = if (index < lines.size) lines[index].indent else return stmts
            if (blockIndent < minIndent) return stmts
            while (index < lines.size && lines[index].indent == blockIndent) {
                stmts += parseStatement(blockIndent)
            }
            if (index < lines.size && lines[index].indent > blockIndent) {
                err("IndentationError", "unexpected indent", lines[index].line)
            }
            return stmts
        }

        private fun parseStatement(currentIndent: Int): Stmt {
            val ll = lines[index]
            val toks = ll.tokens
            val first = toks[0]
            return when {
                first.type == TokType.NAME && first.text == "if" -> parseIf(currentIndent)
                first.type == TokType.NAME && first.text == "while" -> parseWhile(currentIndent)
                first.type == TokType.NAME && first.text == "for" -> parseFor(currentIndent)
                first.type == TokType.NAME && first.text == "def" -> parseDef(currentIndent)
                first.type == TokType.NAME && first.text == "return" -> {
                    index++
                    val tp = TokenParser(toks, 1)
                    val value = if (tp.peek().type == TokType.EOF) null else tp.parseExpression()
                    tp.expectEof()
                    SReturn(ll.line, value)
                }
                first.type == TokType.NAME && first.text == "break" -> { index++; SBreak(ll.line) }
                first.type == TokType.NAME && first.text == "continue" -> { index++; SContinue(ll.line) }
                first.type == TokType.NAME && first.text == "pass" -> { index++; SPass(ll.line) }
                first.type == TokType.NAME && (first.text == "elif" || first.text == "else") ->
                    err("SyntaxError", "'${first.text}' without a matching 'if'", ll.line)
                else -> parseSimple(ll)
            }
        }

        private fun parseSimple(ll: LogicalLine): Stmt {
            index++
            val tp = TokenParser(ll.tokens, 0)
            val target = tp.parseExpression()
            val next = tp.peek()
            if (next.type == TokType.OP && next.text in setOf("=", "+=", "-=", "*=", "/=")) {
                tp.advance()
                val value = tp.parseExpression()
                tp.expectEof()
                if (target !is EName && target !is EIndex) {
                    err("SyntaxError", "cannot assign to this expression", ll.line)
                }
                val op = if (next.text == "=") null else next.text.substring(0, 1)
                return SAssign(ll.line, target, op, value)
            }
            tp.expectEof()
            return SExpr(ll.line, target)
        }

        private fun headerExpr(toks: List<Token>, from: Int, line: Int): Expr {
            // Expression up to trailing ':'
            val colonIdx = toks.indexOfLast { it.type == TokType.OP && it.text == ":" }
            if (colonIdx == -1) err("SyntaxError", "expected ':' at end of line", line)
            val sub = toks.subList(from, colonIdx) + Token(TokType.EOF, "", line)
            val tp = TokenParser(sub, 0)
            val e = tp.parseExpression()
            tp.expectEof()
            return e
        }

        private fun parseChildBlock(parentIndent: Int, line: Int): List<Stmt> {
            if (index >= lines.size || lines[index].indent <= parentIndent) {
                err("IndentationError", "expected an indented block", line)
            }
            return parseBlock(lines[index].indent)
        }

        private fun parseIf(currentIndent: Int): Stmt {
            val branches = mutableListOf<Pair<Expr, List<Stmt>>>()
            var elseBody: List<Stmt>? = null
            val startLine = lines[index].line

            var ll = lines[index]
            val cond = headerExpr(ll.tokens, 1, ll.line)
            index++
            branches += cond to parseChildBlock(currentIndent, ll.line)

            while (index < lines.size && lines[index].indent == currentIndent) {
                val t = lines[index].tokens[0]
                if (t.type != TokType.NAME) break
                when (t.text) {
                    "elif" -> {
                        ll = lines[index]
                        val c = headerExpr(ll.tokens, 1, ll.line)
                        index++
                        branches += c to parseChildBlock(currentIndent, ll.line)
                    }
                    "else" -> {
                        ll = lines[index]
                        index++
                        elseBody = parseChildBlock(currentIndent, ll.line)
                        break
                    }
                    else -> break
                }
            }
            return SIf(startLine, branches, elseBody)
        }

        private fun parseWhile(currentIndent: Int): Stmt {
            val ll = lines[index]
            val cond = headerExpr(ll.tokens, 1, ll.line)
            index++
            return SWhile(ll.line, cond, parseChildBlock(currentIndent, ll.line))
        }

        private fun parseFor(currentIndent: Int): Stmt {
            val ll = lines[index]
            val toks = ll.tokens
            if (toks.size < 5 || toks[1].type != TokType.NAME) {
                err("SyntaxError", "invalid for loop — expected: for name in …:", ll.line)
            }
            val varName = toks[1].text
            if (toks[2].type != TokType.NAME || toks[2].text != "in") {
                err("SyntaxError", "expected 'in' in for loop", ll.line)
            }
            val iterable = headerExpr(toks, 3, ll.line)
            index++
            return SFor(ll.line, varName, iterable, parseChildBlock(currentIndent, ll.line))
        }

        private fun parseDef(currentIndent: Int): Stmt {
            val ll = lines[index]
            val toks = ll.tokens
            if (toks.size < 5 || toks[1].type != TokType.NAME) {
                err("SyntaxError", "invalid function definition", ll.line)
            }
            val name = toks[1].text
            var i = 2
            if (!(toks[i].type == TokType.OP && toks[i].text == "(")) {
                err("SyntaxError", "expected '(' after function name", ll.line)
            }
            i++
            val params = mutableListOf<String>()
            while (!(toks[i].type == TokType.OP && toks[i].text == ")")) {
                if (toks[i].type == TokType.NAME) {
                    params += toks[i].text
                    i++
                    if (toks[i].type == TokType.OP && toks[i].text == ",") i++
                } else {
                    err("SyntaxError", "invalid parameter list", ll.line)
                }
                if (toks[i].type == TokType.EOF) err("SyntaxError", "expected ')'", ll.line)
            }
            index++
            return SDef(ll.line, name, params, parseChildBlock(currentIndent, ll.line))
        }
    }

    /** Pratt-style expression parser over a token list. */
    private class TokenParser(private val tokens: List<Token>, start: Int) {
        private var pos = start

        fun peek(): Token = tokens[pos]
        fun advance(): Token = tokens[pos++]

        fun expectEof() {
            val t = peek()
            if (t.type != TokType.EOF) {
                err("SyntaxError", "unexpected '${t.text}'", t.line)
            }
        }

        fun parseExpression(): Expr = parseOr()

        private fun parseOr(): Expr {
            var left = parseAnd()
            while (peek().let { it.type == TokType.NAME && it.text == "or" }) {
                val t = advance()
                left = EBin(t.line, "or", left, parseAnd())
            }
            return left
        }

        private fun parseAnd(): Expr {
            var left = parseNot()
            while (peek().let { it.type == TokType.NAME && it.text == "and" }) {
                val t = advance()
                left = EBin(t.line, "and", left, parseNot())
            }
            return left
        }

        private fun parseNot(): Expr {
            val t = peek()
            if (t.type == TokType.NAME && t.text == "not") {
                advance()
                return EUnary(t.line, "not", parseNot())
            }
            return parseComparison()
        }

        private fun parseComparison(): Expr {
            var left = parseAdditive()
            while (true) {
                val t = peek()
                val isCmpOp = t.type == TokType.OP && t.text in setOf("==", "!=", "<", ">", "<=", ">=")
                val isIn = t.type == TokType.NAME && t.text == "in"
                if (isCmpOp) {
                    advance()
                    left = EBin(t.line, t.text, left, parseAdditive())
                } else if (isIn) {
                    advance()
                    left = EBin(t.line, "in", left, parseAdditive())
                } else {
                    break
                }
            }
            return left
        }

        private fun parseAdditive(): Expr {
            var left = parseMultiplicative()
            while (peek().let { it.type == TokType.OP && (it.text == "+" || it.text == "-") }) {
                val t = advance()
                left = EBin(t.line, t.text, left, parseMultiplicative())
            }
            return left
        }

        private fun parseMultiplicative(): Expr {
            var left = parseUnary()
            while (peek().let { it.type == TokType.OP && it.text in setOf("*", "/", "//", "%", "**") }) {
                val t = advance()
                left = EBin(t.line, t.text, left, parseUnary())
            }
            return left
        }

        private fun parseUnary(): Expr {
            val t = peek()
            if (t.type == TokType.OP && (t.text == "-" || t.text == "+")) {
                advance()
                return EUnary(t.line, t.text, parseUnary())
            }
            return parsePostfix()
        }

        private fun parsePostfix(): Expr {
            var e = parsePrimary()
            while (true) {
                val t = peek()
                if (t.type == TokType.OP && t.text == "(") {
                    advance()
                    val args = mutableListOf<Expr>()
                    if (!(peek().type == TokType.OP && peek().text == ")")) {
                        args += parseExpression()
                        while (peek().type == TokType.OP && peek().text == ",") {
                            advance()
                            args += parseExpression()
                        }
                    }
                    expectOp(")")
                    e = ECall(t.line, e, args)
                } else if (t.type == TokType.OP && t.text == "[") {
                    advance()
                    val idx = parseExpression()
                    expectOp("]")
                    e = EIndex(t.line, e, idx)
                } else if (t.type == TokType.OP && t.text == ".") {
                    advance()
                    val nameTok = advance()
                    if (nameTok.type != TokType.NAME) err("SyntaxError", "expected attribute name after '.'", nameTok.line)
                    e = EAttr(t.line, e, nameTok.text)
                } else {
                    break
                }
            }
            return e
        }

        private fun expectOp(op: String) {
            val t = advance()
            if (t.type != TokType.OP || t.text != op) {
                err("SyntaxError", "expected '$op'", t.line)
            }
        }

        private fun parsePrimary(): Expr {
            val t = advance()
            return when {
                t.type == TokType.NUMBER ->
                    if (t.text.contains('.')) ENum(t.line, t.text.toDouble()) else ENum(t.line, t.text.toLong())
                t.type == TokType.STRING -> EStr(t.line, t.text)
                t.type == TokType.NAME -> when (t.text) {
                    "True" -> EBool(t.line, true)
                    "False" -> EBool(t.line, false)
                    "None" -> ENone(t.line)
                    else -> EName(t.line, t.text)
                }
                t.type == TokType.OP && t.text == "(" -> {
                    val e = parseExpression()
                    expectOp(")")
                    e
                }
                t.type == TokType.OP && t.text == "[" -> {
                    val items = mutableListOf<Expr>()
                    if (!(peek().type == TokType.OP && peek().text == "]")) {
                        items += parseExpression()
                        while (peek().type == TokType.OP && peek().text == ",") {
                            advance()
                            items += parseExpression()
                        }
                    }
                    expectOp("]")
                    EList(t.line, items)
                }
                t.type == TokType.EOF -> err("SyntaxError", "unexpected end of line", t.line)
                else -> err("SyntaxError", "unexpected '${t.text}'", t.line)
            }
        }
    }

    // ------------------------------------------------------------------
    // Runtime
    // ------------------------------------------------------------------

    private class Scope(val parent: Scope?) {
        val vars = HashMap<String, Any?>()

        fun lookup(name: String): Pair<Scope, Any?>? {
            var s: Scope? = this
            while (s != null) {
                if (s.vars.containsKey(name)) return s to s.vars[name]
                s = s.parent
            }
            return null
        }
    }

    private class PyFunction(val name: String, val params: List<String>, val body: List<Stmt>, val closure: Scope)
    private class PyRange(val count: LongRange)

    private class Interpreter(private val out: StringBuilder, private val stdinValue: String) {
        private var steps = 0

        private fun tick(line: Int?) {
            steps++
            if (steps > MAX_STEPS) {
                err("TimeoutError", "program ran too long — check for infinite loops", line)
            }
            if (out.length > MAX_OUTPUT_CHARS) {
                err("OutputLimitError", "too much output produced", line)
            }
        }

        fun execBlock(stmts: List<Stmt>, scope: Scope) {
            for (s in stmts) exec(s, scope)
        }

        private fun exec(stmt: Stmt, scope: Scope) {
            tick(stmt.line)
            when (stmt) {
                is SExpr -> eval(stmt.expr, scope)
                is SAssign -> {
                    val value = eval(stmt.value, scope)
                    val finalValue = if (stmt.op != null) {
                        val current = evalTarget(stmt.target, scope)
                        binaryOp(stmt.op, current, value, stmt.line)
                    } else {
                        value
                    }
                    assign(stmt.target, finalValue, scope)
                }
                is SIf -> {
                    var done = false
                    for ((cond, body) in stmt.branches) {
                        if (truthy(eval(cond, scope))) {
                            execBlock(body, scope)
                            done = true
                            break
                        }
                    }
                    if (!done) stmt.elseBody?.let { execBlock(it, scope) }
                }
                is SWhile -> {
                    while (truthy(eval(stmt.cond, scope))) {
                        tick(stmt.line)
                        try {
                            execBlock(stmt.body, scope)
                        } catch (b: BreakSignal) {
                            break
                        } catch (c: ContinueSignal) {
                            // continue loop
                        }
                    }
                }
                is SFor -> {
                    val iterable = eval(stmt.iterable, scope)
                    val items: List<Any?> = when (iterable) {
                        is PyRange -> iterable.count.map { it }
                        is MutableList<*> -> iterable.toList()
                        is String -> iterable.map { it.toString() }
                        else -> err("TypeError", "'${typeName(iterable)}' is not iterable", stmt.line)
                    }
                    for (item in items) {
                        tick(stmt.line)
                        scope.vars[stmt.varName] = item
                        try {
                            execBlock(stmt.body, scope)
                        } catch (b: BreakSignal) {
                            break
                        } catch (c: ContinueSignal) {
                            // continue loop
                        }
                    }
                }
                is SDef -> scope.vars[stmt.name] = PyFunction(stmt.name, stmt.params, stmt.body, scope)
                is SReturn -> throw ReturnSignal(stmt.value?.let { eval(it, scope) })
                is SBreak -> throw BreakSignal()
                is SContinue -> throw ContinueSignal()
                is SPass -> Unit
            }
        }

        private fun evalTarget(target: Expr, scope: Scope): Any? = when (target) {
            is EName -> scope.lookup(target.name)?.second
                ?: err("NameError", "name '${target.name}' is not defined", target.line)
            is EIndex -> eval(target, scope)
            else -> err("SyntaxError", "invalid assignment target", target.line)
        }

        private fun assign(target: Expr, value: Any?, scope: Scope) {
            when (target) {
                is EName -> {
                    val existing = scope.lookup(target.name)
                    if (existing != null) existing.first.vars[target.name] = value
                    else scope.vars[target.name] = value
                }
                is EIndex -> {
                    val container = eval(target.target, scope)
                    val idx = eval(target.index, scope)
                    if (container is MutableList<*>) {
                        val i = toIndex(idx, container.size, target.line)
                        @Suppress("UNCHECKED_CAST")
                        (container as MutableList<Any?>)[i] = value
                    } else {
                        err("TypeError", "'${typeName(container)}' does not support item assignment", target.line)
                    }
                }
                else -> err("SyntaxError", "invalid assignment target", target.line)
            }
        }

        private fun toIndex(idx: Any?, size: Int, line: Int): Int {
            val i = (idx as? Long)?.toInt()
                ?: err("TypeError", "list index must be an integer", line)
            val real = if (i < 0) size + i else i
            if (real < 0 || real >= size) err("IndexError", "list index out of range", line)
            return real
        }

        fun eval(expr: Expr, scope: Scope): Any? {
            tick(expr.line)
            return when (expr) {
                is ENum -> expr.value
                is EStr -> expr.value
                is EBool -> expr.value
                is ENone -> null
                is EName -> scope.lookup(expr.name)?.second
                    ?: err("NameError", "name '${expr.name}' is not defined", expr.line)
                is EList -> expr.items.map { eval(it, scope) }.toMutableList()
                is EIndex -> {
                    val container = eval(expr.target, scope)
                    val idx = eval(expr.index, scope)
                    when (container) {
                        is MutableList<*> -> container[toIndex(idx, container.size, expr.line)]
                        is String -> {
                            val i = toIndex(idx, container.length, expr.line)
                            container[i].toString()
                        }
                        else -> err("TypeError", "'${typeName(container)}' is not subscriptable", expr.line)
                    }
                }
                is EAttr -> BoundMethod(eval(expr.target, scope), expr.name, expr.line)
                is ECall -> evalCall(expr, scope)
                is EUnary -> {
                    val v = eval(expr.operand, scope)
                    when (expr.op) {
                        "-" -> when (v) {
                            is Long -> -v
                            is Double -> -v
                            else -> err("TypeError", "bad operand for unary -: '${typeName(v)}'", expr.line)
                        }
                        "+" -> v
                        "not" -> !truthy(v)
                        else -> err("SyntaxError", "unknown unary operator", expr.line)
                    }
                }
                is EBin -> {
                    when (expr.op) {
                        "and" -> {
                            val l = eval(expr.left, scope)
                            if (!truthy(l)) l else eval(expr.right, scope)
                        }
                        "or" -> {
                            val l = eval(expr.left, scope)
                            if (truthy(l)) l else eval(expr.right, scope)
                        }
                        else -> binaryOp(expr.op, eval(expr.left, scope), eval(expr.right, scope), expr.line)
                    }
                }
            }
        }

        private class BoundMethod(val receiver: Any?, val name: String, val line: Int)

        /** Sentinel distinguishing "not a builtin" from a builtin returning None. */
        private object NotABuiltin

        private fun evalCall(expr: ECall, scope: Scope): Any? {
            // Built-in or user function by name
            val callee = expr.target
            if (callee is EName && scope.lookup(callee.name) == null) {
                val result = callBuiltin(callee.name, expr.args.map { eval(it, scope) }, expr.line)
                if (result === NotABuiltin) {
                    err("NameError", "name '${callee.name}' is not defined", expr.line)
                }
                return result
            }
            val target = eval(callee, scope)
            val args = expr.args.map { eval(it, scope) }
            return when (target) {
                is PyFunction -> callFunction(target, args, expr.line)
                is BoundMethod -> callMethod(target, args)
                else -> err("TypeError", "'${typeName(target)}' object is not callable", expr.line)
            }
        }

        private fun callFunction(fn: PyFunction, args: List<Any?>, line: Int): Any? {
            if (args.size != fn.params.size) {
                err("TypeError", "${fn.name}() takes ${fn.params.size} arguments but ${args.size} were given", line)
            }
            val local = Scope(fn.closure)
            fn.params.forEachIndexed { i, p -> local.vars[p] = args[i] }
            return try {
                execBlock(fn.body, local)
                null
            } catch (r: ReturnSignal) {
                r.value
            }
        }

        private fun callMethod(m: BoundMethod, args: List<Any?>): Any? {
            val r = m.receiver
            return when {
                r is MutableList<*> && m.name == "append" -> {
                    @Suppress("UNCHECKED_CAST")
                    (r as MutableList<Any?>).add(args.firstOrNull())
                    null
                }
                r is MutableList<*> && m.name == "pop" -> {
                    @Suppress("UNCHECKED_CAST")
                    val list = r as MutableList<Any?>
                    if (list.isEmpty()) err("IndexError", "pop from empty list", m.line)
                    val idx = (args.firstOrNull() as? Long)?.toInt() ?: (list.size - 1)
                    list.removeAt(if (idx < 0) list.size + idx else idx)
                }
                r is String && m.name == "upper" -> r.uppercase()
                r is String && m.name == "lower" -> r.lowercase()
                r is String && m.name == "strip" -> r.trim()
                else -> err("AttributeError", "'${typeName(r)}' object has no method '${m.name}'", m.line)
            }
        }

        private fun callBuiltin(name: String, args: List<Any?>, line: Int): Any? = when (name) {
            "print" -> {
                out.append(args.joinToString(" ") { pyStr(it) }).append('\n')
                null
            }
            "len" -> when (val a = args.firstOrNull()) {
                is String -> a.length.toLong()
                is MutableList<*> -> a.size.toLong()
                else -> err("TypeError", "object of type '${typeName(a)}' has no len()", line)
            }
            "range" -> when (args.size) {
                1 -> PyRange(0 until asLong(args[0], line))
                2 -> PyRange(asLong(args[0], line) until asLong(args[1], line))
                else -> err("TypeError", "range expected 1 or 2 arguments", line)
            }
            "str" -> pyStr(args.firstOrNull())
            "int" -> when (val a = args.firstOrNull()) {
                is Long -> a
                is Double -> a.toLong()
                is Boolean -> if (a) 1L else 0L
                is String -> a.trim().toLongOrNull() ?: err("ValueError", "invalid literal for int(): '$a'", line)
                else -> err("TypeError", "int() argument must be a string or a number", line)
            }
            "float" -> when (val a = args.firstOrNull()) {
                is Long -> a.toDouble()
                is Double -> a
                is String -> a.trim().toDoubleOrNull() ?: err("ValueError", "could not convert string to float: '$a'", line)
                else -> err("TypeError", "float() argument must be a string or a number", line)
            }
            "abs" -> when (val a = args.firstOrNull()) {
                is Long -> kotlin.math.abs(a)
                is Double -> kotlin.math.abs(a)
                else -> err("TypeError", "bad operand type for abs()", line)
            }
            "min" -> numericFold(args, line) { a, b -> if (compareValues2(a, b, line) <= 0) a else b }
            "max" -> numericFold(args, line) { a, b -> if (compareValues2(a, b, line) >= 0) a else b }
            "sum" -> {
                val list = args.firstOrNull() as? MutableList<*>
                    ?: err("TypeError", "sum() expects a list", line)
                var acc: Any? = 0L
                for (item in list) acc = binaryOp("+", acc, item, line)
                acc
            }
            "sorted" -> {
                val list = args.firstOrNull() as? MutableList<*>
                    ?: err("TypeError", "sorted() expects a list", line)
                list.sortedWith { a, b -> compareValues2(a, b, line) }.toMutableList()
            }
            "input" -> {
                args.firstOrNull()?.let { out.append(pyStr(it)) }
                out.append(stdinValue).append('\n')
                stdinValue
            }
            "bool" -> truthy(args.firstOrNull())
            else -> NotABuiltin
        }

        private fun numericFold(args: List<Any?>, line: Int, op: (Any?, Any?) -> Any?): Any? {
            val items: List<Any?> = if (args.size == 1 && args[0] is MutableList<*>) {
                (args[0] as MutableList<*>).toList()
            } else {
                args
            }
            if (items.isEmpty()) err("ValueError", "empty sequence", line)
            return items.reduce(op)
        }

        private fun asLong(v: Any?, line: Int): Long = when (v) {
            is Long -> v
            is Double -> v.toLong()
            is Boolean -> if (v) 1L else 0L
            else -> err("TypeError", "expected an integer, got '${typeName(v)}'", line)
        }

        private fun compareValues2(a: Any?, b: Any?, line: Int): Int = when {
            a is Long && b is Long -> a.compareTo(b)
            a is Double || b is Double -> toDouble(a, line).compareTo(toDouble(b, line))
            a is String && b is String -> a.compareTo(b)
            a is Boolean && b is Boolean -> a.compareTo(b)
            else -> err("TypeError", "'<' not supported between '${typeName(a)}' and '${typeName(b)}'", line)
        }

        private fun toDouble(v: Any?, line: Int): Double = when (v) {
            is Long -> v.toDouble()
            is Double -> v
            is Boolean -> if (v) 1.0 else 0.0
            else -> err("TypeError", "expected a number, got '${typeName(v)}'", line)
        }

        fun binaryOp(op: String, left: Any?, right: Any?, line: Int): Any? = when (op) {
            "+" -> when {
                left is String && right is String -> left + right
                left is String || right is String -> {
                    if (left is String) {
                        err("TypeError", "can only concatenate str to str — use str() to convert numbers", line)
                    } else {
                        err("TypeError", "unsupported operand type(s) for +: number and str — use str() to convert", line)
                    }
                }
                left is MutableList<*> && right is MutableList<*> -> (left + right).toMutableList()
                else -> arith(op, left, right, line)
            }
            "-", "%", "//", "**" -> arith(op, left, right, line)
            "*" -> when {
                left is String && right is Long -> left.repeat(right.toInt().coerceAtLeast(0))
                left is Long && right is String -> right.repeat(left.toInt().coerceAtLeast(0))
                else -> arith(op, left, right, line)
            }
            "/" -> {
                val r = toDouble(right, line)
                if (r == 0.0) err("ZeroDivisionError", "division by zero", line)
                toDouble(left, line) / r
            }
            "==" -> pyEquals(left, right)
            "!=" -> !pyEquals(left, right)
            "<" -> compareValues2(left, right, line) < 0
            ">" -> compareValues2(left, right, line) > 0
            "<=" -> compareValues2(left, right, line) <= 0
            ">=" -> compareValues2(left, right, line) >= 0
            "in" -> when (right) {
                is MutableList<*> -> right.any { pyEquals(it, left) }
                is String -> left is String && right.contains(left)
                else -> err("TypeError", "argument of type '${typeName(right)}' is not iterable", line)
            }
            else -> err("SyntaxError", "unknown operator '$op'", line)
        }

        private fun arith(op: String, left: Any?, right: Any?, line: Int): Any {
            val bothInt = left is Long && right is Long
            if (left !is Long && left !is Double && left !is Boolean) {
                err("TypeError", "unsupported operand type(s) for $op: '${typeName(left)}' and '${typeName(right)}'", line)
            }
            if (right !is Long && right !is Double && right !is Boolean) {
                err("TypeError", "unsupported operand type(s) for $op: '${typeName(left)}' and '${typeName(right)}'", line)
            }
            if (bothInt) {
                val a = left as Long
                val b = right as Long
                return when (op) {
                    "+" -> a + b
                    "-" -> a - b
                    "*" -> a * b
                    "%" -> {
                        if (b == 0L) err("ZeroDivisionError", "integer modulo by zero", line)
                        ((a % b) + b) % b
                    }
                    "//" -> {
                        if (b == 0L) err("ZeroDivisionError", "integer division by zero", line)
                        Math.floorDiv(a, b)
                    }
                    "**" -> {
                        var result = 1L
                        var i = 0L
                        if (b < 0) return Math.pow(a.toDouble(), b.toDouble())
                        while (i < b) {
                            result *= a
                            i++
                        }
                        result
                    }
                    else -> err("SyntaxError", "unknown operator '$op'", line)
                }
            }
            val a = toDouble(left, line)
            val b = toDouble(right, line)
            return when (op) {
                "+" -> a + b
                "-" -> a - b
                "*" -> a * b
                "%" -> {
                    if (b == 0.0) err("ZeroDivisionError", "float modulo by zero", line)
                    ((a % b) + b) % b
                }
                "//" -> {
                    if (b == 0.0) err("ZeroDivisionError", "float floor division by zero", line)
                    kotlin.math.floor(a / b)
                }
                "**" -> Math.pow(a, b)
                else -> err("SyntaxError", "unknown operator '$op'", line)
            }
        }

        private fun pyEquals(a: Any?, b: Any?): Boolean = when {
            a is Long && b is Double -> a.toDouble() == b
            a is Double && b is Long -> a == b.toDouble()
            a is MutableList<*> && b is MutableList<*> ->
                a.size == b.size && a.indices.all { pyEquals(a[it], b[it]) }
            else -> a == b
        }

        private fun truthy(v: Any?): Boolean = when (v) {
            null -> false
            is Boolean -> v
            is Long -> v != 0L
            is Double -> v != 0.0
            is String -> v.isNotEmpty()
            is MutableList<*> -> v.isNotEmpty()
            else -> true
        }
    }

    private fun typeName(v: Any?): String = when (v) {
        null -> "NoneType"
        is Long -> "int"
        is Double -> "float"
        is Boolean -> "bool"
        is String -> "str"
        is MutableList<*> -> "list"
        is PyFunction -> "function"
        is PyRange -> "range"
        else -> v.javaClass.simpleName
    }

    /** Python-style str() conversion. */
    fun pyStr(v: Any?): String = when (v) {
        null -> "None"
        is Boolean -> if (v) "True" else "False"
        is Double -> {
            if (v == kotlin.math.floor(v) && !v.isInfinite() && kotlin.math.abs(v) < 1e15) {
                "${v.toLong()}.0"
            } else {
                v.toString()
            }
        }
        is MutableList<*> -> v.joinToString(", ", "[", "]") { pyRepr(it) }
        else -> v.toString()
    }

    private fun pyRepr(v: Any?): String = when (v) {
        is String -> "'${v}'"
        else -> pyStr(v)
    }
}
