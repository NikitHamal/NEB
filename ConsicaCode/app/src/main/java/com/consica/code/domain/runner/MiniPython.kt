package com.consica.code.domain.runner

/**
 * A small, dependency-free, fully-offline interpreter for the Python subset used by Consica Code
 * lessons: print, variables, int/float/str/bool, arithmetic, comparisons, string concatenation,
 * if/elif/else, for-in-range, while, lists, dicts, indexing, def/return, and the builtins
 * print, len, str, int, float, range, sum, max, min, input.
 *
 * It is intentionally conservative: unsupported syntax yields a friendly error rather than a
 * crash. For full CPython compatibility a Pyodide [CodeRunner] can be substituted (see
 * CodeRunner.kt) without touching the rest of the app.
 */
class MiniPython(
    private val maxOutputChars: Int = 20_000,
    private val maxLoopIterations: Int = 50_000,
) : CodeRunner {

    private sealed interface Value {
        data class Num(val v: Double) : Value
        data class Str(val v: String) : Value
        data class Bool(val v: Boolean) : Value
        data class Lst(val v: MutableList<Value>) : Value
        data class Dct(val v: LinkedHashMap<Value, Value>) : Value
        object None : Value
    }

    private class PyError(val line: Int?, override val message: String) : RuntimeException(message)
    private class ReturnSignal(val value: Value) : RuntimeException()

    private data class Func(val params: List<String>, val body: List<Line>, val defLine: Int)
    private data class Line(val indent: Int, val text: String, val number: Int)

    private val globals = HashMap<String, Value>()
    private val functions = HashMap<String, Func>()
    private val out = StringBuilder()
    private var iterations = 0

    override fun run(code: String): RunResult {
        globals.clear(); functions.clear(); out.clear(); iterations = 0
        val lines = lex(code)
        return try {
            execBlock(lines, globals)
            RunResult.ok(out.toString())
        } catch (e: PyError) {
            RunResult.fail(e.message, e.line, out.toString())
        } catch (e: ReturnSignal) {
            RunResult.ok(out.toString())
        } catch (e: StackOverflowError) {
            RunResult.fail("Too much recursion.", null, out.toString())
        } catch (e: Exception) {
            RunResult.fail(e.message ?: "Something went wrong while running.", null, out.toString())
        }
    }

    // ---- Lexing into indented logical lines ----
    private fun lex(code: String): List<Line> {
        val result = ArrayList<Line>()
        code.split("\n").forEachIndexed { idx, raw ->
            val noComment = stripComment(raw)
            if (noComment.isBlank()) return@forEachIndexed
            val indent = noComment.takeWhile { it == ' ' }.length +
                noComment.takeWhile { it == '\t' }.length * 4
            result.add(Line(indent, noComment.trim(), idx + 1))
        }
        return result
    }

    private fun stripComment(s: String): String {
        var inStr = false; var quote = ' '
        val sb = StringBuilder()
        for (c in s) {
            if (inStr) {
                sb.append(c); if (c == quote) inStr = false
            } else {
                if (c == '#') break
                if (c == '"' || c == '\'') { inStr = true; quote = c }
                sb.append(c)
            }
        }
        return sb.toString()
    }

    // ---- Statement execution ----
    private fun execBlock(lines: List<Line>, env: HashMap<String, Value>) {
        var i = 0
        while (i < lines.size) {
            val line = lines[i]
            val keyword = line.text.substringBefore('(').substringBefore(' ').trim()
            when {
                line.text.startsWith("def ") -> {
                    i = defineFunction(lines, i)
                }
                keyword == "if" || line.text.startsWith("if ") -> {
                    i = execIf(lines, i, env)
                }
                line.text.startsWith("for ") -> {
                    i = execFor(lines, i, env)
                }
                line.text.startsWith("while ") -> {
                    i = execWhile(lines, i, env)
                }
                line.text == "pass" -> i++
                line.text.startsWith("return") -> {
                    val expr = line.text.removePrefix("return").trim()
                    throw ReturnSignal(if (expr.isEmpty()) Value.None else eval(expr, env, line.number))
                }
                else -> {
                    execSimple(line, env)
                    i++
                }
            }
        }
    }

    private fun childBlock(lines: List<Line>, headerIndex: Int): Pair<List<Line>, Int> {
        val headerIndent = lines[headerIndex].indent
        val body = ArrayList<Line>()
        var j = headerIndex + 1
        while (j < lines.size && lines[j].indent > headerIndent) { body.add(lines[j]); j++ }
        if (body.isEmpty()) throw PyError(lines[headerIndex].number, "This block needs an indented line under it.")
        return body to j
    }

    private fun defineFunction(lines: List<Line>, index: Int): Int {
        val header = lines[index]
        val sig = header.text.removePrefix("def ").trim().removeSuffix(":").trim()
        val name = sig.substringBefore('(').trim()
        val params = sig.substringAfter('(').substringBeforeLast(')')
            .split(',').map { it.trim() }.filter { it.isNotEmpty() }
        val (body, nextIndex) = childBlock(lines, index)
        functions[name] = Func(params, body, header.number)
        return nextIndex
    }

    private fun execIf(lines: List<Line>, index: Int, env: HashMap<String, Value>): Int {
        var i = index
        var taken = false
        while (i < lines.size) {
            val line = lines[i]
            val t = line.text
            val isElse = t == "else:" || t.startsWith("else ")
            val isElif = t.startsWith("elif ")
            val isIf = t.startsWith("if ")
            if (!isIf && !isElif && !isElse) break
            if (i != index && lines[i].indent != lines[index].indent) break
            val (body, next) = childBlock(lines, i)
            val condTrue = when {
                isElse -> !taken
                else -> {
                    val cond = t.removePrefix("if ").removePrefix("elif ").trim().removeSuffix(":").trim()
                    !taken && truthy(eval(cond, env, line.number))
                }
            }
            if (condTrue) { execBlock(body, env); taken = true }
            i = next
            if (isElse) break
        }
        return i
    }

    private fun execFor(lines: List<Line>, index: Int, env: HashMap<String, Value>): Int {
        val header = lines[index]
        val spec = header.text.removePrefix("for ").trim().removeSuffix(":").trim()
        val varName = spec.substringBefore(" in ").trim()
        val iterableExpr = spec.substringAfter(" in ").trim()
        val (body, next) = childBlock(lines, index)
        val iterable = eval(iterableExpr, env, header.number)
        val items = when (iterable) {
            is Value.Lst -> iterable.v.toList()
            is Value.Str -> iterable.v.map { Value.Str(it.toString()) }
            else -> throw PyError(header.number, "You can only loop over a list, range, or text.")
        }
        for (item in items) {
            guardIterations(header.number)
            env[varName] = item
            try { execBlock(body, env) } catch (r: ReturnSignal) { throw r }
        }
        return next
    }

    private fun execWhile(lines: List<Line>, index: Int, env: HashMap<String, Value>): Int {
        val header = lines[index]
        val cond = header.text.removePrefix("while ").trim().removeSuffix(":").trim()
        val (body, next) = childBlock(lines, index)
        while (truthy(eval(cond, env, header.number))) {
            guardIterations(header.number)
            execBlock(body, env)
        }
        return next
    }

    private fun execSimple(line: Line, env: HashMap<String, Value>) {
        val t = line.text
        // Assignment (not ==, <=, >=, !=)
        val eq = findAssignment(t)
        if (eq >= 0) {
            val target = t.substring(0, eq).trim()
            val valueExpr = t.substring(eq + 1).trim()
            val value = eval(valueExpr, env, line.number)
            assign(target, value, env, line.number)
            return
        }
        // Bare expression / function call (e.g. print(...), grow())
        eval(t, env, line.number)
    }

    private fun findAssignment(t: String): Int {
        var depth = 0; var inStr = false; var quote = ' '
        var i = 0
        while (i < t.length) {
            val c = t[i]
            if (inStr) { if (c == quote) inStr = false }
            else when (c) {
                '"', '\'' -> { inStr = true; quote = c }
                '(', '[', '{' -> depth++
                ')', ']', '}' -> depth--
                '=' -> {
                    if (depth == 0) {
                        val prev = if (i > 0) t[i - 1] else ' '
                        val nxt = if (i + 1 < t.length) t[i + 1] else ' '
                        if (prev != '=' && prev != '!' && prev != '<' && prev != '>' && nxt != '=') return i
                    }
                }
            }
            i++
        }
        return -1
    }

    private fun assign(target: String, value: Value, env: HashMap<String, Value>, line: Int) {
        // Simple index assignment: name[expr] = value
        if (target.endsWith("]") && target.contains('[')) {
            val name = target.substringBefore('[').trim()
            val keyExpr = target.substring(target.indexOf('[') + 1, target.lastIndexOf(']'))
            val container = env[name] ?: throw PyError(line, "I don't know '$name' yet.")
            val key = eval(keyExpr, env, line)
            when (container) {
                is Value.Lst -> {
                    val idx = (key as? Value.Num)?.v?.toInt()
                        ?: throw PyError(line, "List positions must be numbers.")
                    if (idx !in container.v.indices) throw PyError(line, "That list position doesn't exist.")
                    container.v[idx] = value
                }
                is Value.Dct -> container.v[key] = value
                else -> throw PyError(line, "Can't index into that.")
            }
            return
        }
        env[target] = value
    }

    // ---- Expression evaluation (recursive descent) ----
    private fun eval(expr: String, env: HashMap<String, Value>, line: Int): Value {
        return Parser(expr, env, line).parseExpression()
    }

    private inner class Parser(
        private val src: String,
        private val env: HashMap<String, Value>,
        private val line: Int,
    ) {
        private var pos = 0

        fun parseExpression(): Value {
            val v = parseComparison()
            skipWs()
            if (pos < src.length) {
                // Trailing tokens we didn't consume — likely unsupported syntax.
                val rest = src.substring(pos).trim()
                if (rest.isNotEmpty()) throw PyError(line, "I couldn't understand: '$rest'.")
            }
            return v
        }

        private fun parseComparison(): Value {
            var left = parseAddSub()
            while (true) {
                skipWs()
                val op = matchAny("==", "!=", "<=", ">=", "<", ">", "and", "or") ?: break
                val right = parseAddSub()
                left = applyCompare(left, op, right)
            }
            return left
        }

        private fun parseAddSub(): Value {
            var left = parseMulDiv()
            while (true) {
                skipWs()
                val op = matchAny("+", "-") ?: break
                val right = parseMulDiv()
                left = applyArith(left, op, right)
            }
            return left
        }

        private fun parseMulDiv(): Value {
            var left = parseUnary()
            while (true) {
                skipWs()
                val op = matchAny("*", "//", "/", "%") ?: break
                val right = parseUnary()
                left = applyArith(left, op, right)
            }
            return left
        }

        private fun parseUnary(): Value {
            skipWs()
            if (match("-")) { val v = parseUnary(); return Value.Num(-asNum(v)) }
            if (match("not ")) { val v = parseUnary(); return Value.Bool(!truthy(v)) }
            return parsePostfix()
        }

        private fun parsePostfix(): Value {
            var v = parsePrimary()
            while (true) {
                skipWs()
                if (peek() == '[') {
                    expect('[')
                    val key = Parser(readBalanced(']'), env, line).parseExpression()
                    v = index(v, key)
                } else break
            }
            return v
        }

        private fun parsePrimary(): Value {
            skipWs()
            val c = peek() ?: throw PyError(line, "Unexpected end of expression.")
            // Parenthesised
            if (c == '(') { expect('('); return Parser(readBalanced(')'), env, line).parseExpression() }
            // String literal
            if (c == '"' || c == '\'') return Value.Str(readString(c))
            // List literal
            if (c == '[') { expect('['); return readList(readBalanced(']')) }
            // Dict literal
            if (c == '{') { expect('{'); return readDict(readBalanced('}')) }
            // Number
            if (c.isDigit() || (c == '.' && pos + 1 < src.length && src[pos + 1].isDigit())) {
                return Value.Num(readNumber())
            }
            // Identifier / keyword / call
            val name = readIdent()
            if (name.isEmpty()) throw PyError(line, "I couldn't read this expression.")
            when (name) {
                "True" -> return Value.Bool(true)
                "False" -> return Value.Bool(false)
                "None" -> return Value.None
            }
            skipWs()
            if (peek() == '(') {
                expect('(')
                val argsSrc = readBalanced(')')
                val args = splitArgs(argsSrc).map { Parser(it, env, line).parseExpression() }
                return callFunction(name, args)
            }
            return env[name] ?: throw PyError(line, "I don't know '$name' yet. Did you set it?")
        }

        // ---- low-level helpers ----
        private fun peek(): Char? = if (pos < src.length) src[pos] else null
        private fun skipWs() { while (pos < src.length && src[pos] == ' ') pos++ }
        private fun match(s: String): Boolean {
            skipWs()
            if (src.startsWith(s, pos)) { pos += s.length; return true }
            return false
        }
        private fun matchAny(vararg ops: String): String? {
            skipWs()
            for (op in ops) {
                if (src.startsWith(op, pos)) {
                    // word operators need a boundary
                    if (op[0].isLetter()) {
                        val after = pos + op.length
                        if (after < src.length && src[after].isLetterOrDigit()) continue
                    }
                    pos += op.length; return op
                }
            }
            return null
        }
        private fun expect(c: Char) { skipWs(); if (peek() != c) throw PyError(line, "Expected '$c'."); pos++ }

        private fun readBalanced(close: Char): String {
            val open = when (close) { ')' -> '('; ']' -> '['; '}' -> '{'; else -> ' ' }
            val sb = StringBuilder(); var depth = 1; var inStr = false; var q = ' '
            while (pos < src.length) {
                val ch = src[pos++]
                if (inStr) { sb.append(ch); if (ch == q) inStr = false; continue }
                when (ch) {
                    '"', '\'' -> { inStr = true; q = ch; sb.append(ch) }
                    open -> { depth++; sb.append(ch) }
                    close -> { depth--; if (depth == 0) return sb.toString(); sb.append(ch) }
                    else -> sb.append(ch)
                }
            }
            throw PyError(line, "Missing closing '$close'.")
        }

        private fun readString(quote: Char): String {
            expect(quote)
            val sb = StringBuilder()
            while (pos < src.length) {
                val ch = src[pos++]
                if (ch == '\\' && pos < src.length) {
                    when (val esc = src[pos++]) {
                        'n' -> sb.append('\n'); 't' -> sb.append('\t')
                        '\\' -> sb.append('\\'); '"' -> sb.append('"'); '\'' -> sb.append('\'')
                        else -> sb.append(esc)
                    }
                } else if (ch == quote) return sb.toString()
                else sb.append(ch)
            }
            throw PyError(line, "A piece of text is missing its closing quote.")
        }

        private fun readNumber(): Double {
            val start = pos
            while (pos < src.length && (src[pos].isDigit() || src[pos] == '.')) pos++
            return src.substring(start, pos).toDoubleOrNull()
                ?: throw PyError(line, "That number doesn't look right.")
        }

        private fun readIdent(): String {
            skipWs(); val start = pos
            while (pos < src.length && (src[pos].isLetterOrDigit() || src[pos] == '_')) pos++
            return src.substring(start, pos)
        }

        private fun readList(inner: String): Value {
            val items = splitArgs(inner).map { Parser(it, env, line).parseExpression() }
            return Value.Lst(items.toMutableList())
        }

        private fun readDict(inner: String): Value {
            val map = LinkedHashMap<Value, Value>()
            for (pair in splitArgs(inner)) {
                if (pair.isBlank()) continue
                val colon = topLevelColon(pair)
                if (colon < 0) throw PyError(line, "Dictionary items need a key: value.")
                val k = Parser(pair.substring(0, colon), env, line).parseExpression()
                val v = Parser(pair.substring(colon + 1), env, line).parseExpression()
                map[k] = v
            }
            return Value.Dct(map)
        }
    }

    private fun topLevelColon(s: String): Int {
        var depth = 0; var inStr = false; var q = ' '
        for (i in s.indices) {
            val c = s[i]
            if (inStr) { if (c == q) inStr = false; continue }
            when (c) {
                '"', '\'' -> { inStr = true; q = c }
                '(', '[', '{' -> depth++
                ')', ']', '}' -> depth--
                ':' -> if (depth == 0) return i
            }
        }
        return -1
    }

    private fun splitArgs(s: String): List<String> {
        if (s.isBlank()) return emptyList()
        val parts = ArrayList<String>(); val sb = StringBuilder()
        var depth = 0; var inStr = false; var q = ' '
        for (c in s) {
            if (inStr) { sb.append(c); if (c == q) inStr = false; continue }
            when (c) {
                '"', '\'' -> { inStr = true; q = c; sb.append(c) }
                '(', '[', '{' -> { depth++; sb.append(c) }
                ')', ']', '}' -> { depth--; sb.append(c) }
                ',' -> if (depth == 0) { parts.add(sb.toString()); sb.clear() } else sb.append(c)
                else -> sb.append(c)
            }
        }
        if (sb.isNotBlank() || parts.isNotEmpty()) parts.add(sb.toString())
        return parts.map { it.trim() }
    }

    // ---- operators / builtins ----
    private fun applyArith(l: Value, op: String, r: Value): Value {
        if (op == "+" && (l is Value.Str || r is Value.Str)) {
            return Value.Str(stringify(l) + stringify(r))
        }
        if (op == "+" && l is Value.Lst && r is Value.Lst) {
            return Value.Lst((l.v + r.v).toMutableList())
        }
        if (op == "*" && l is Value.Str && r is Value.Num) {
            return Value.Str(l.v.repeat(r.v.toInt().coerceAtLeast(0)))
        }
        val a = asNum(l); val b = asNum(r)
        val res = when (op) {
            "+" -> a + b; "-" -> a - b; "*" -> a * b
            "/" -> { if (b == 0.0) throw PyError(null, "You can't divide by zero."); a / b }
            "//" -> { if (b == 0.0) throw PyError(null, "You can't divide by zero."); kotlin.math.floor(a / b) }
            "%" -> { if (b == 0.0) throw PyError(null, "You can't divide by zero."); a % b }
            else -> throw PyError(null, "Unsupported operator '$op'.")
        }
        return Value.Num(res)
    }

    private fun applyCompare(l: Value, op: String, r: Value): Value {
        return when (op) {
            "and" -> Value.Bool(truthy(l) && truthy(r))
            "or" -> Value.Bool(truthy(l) || truthy(r))
            "==" -> Value.Bool(valueEquals(l, r))
            "!=" -> Value.Bool(!valueEquals(l, r))
            else -> {
                val a = asNum(l); val b = asNum(r)
                Value.Bool(when (op) { "<" -> a < b; ">" -> a > b; "<=" -> a <= b; ">=" -> a >= b; else -> false })
            }
        }
    }

    private fun callFunction(name: String, args: List<Value>): Value {
        when (name) {
            "print" -> {
                val text = args.joinToString(" ") { stringify(it) }
                appendOut(text + "\n"); return Value.None
            }
            "len" -> return Value.Num(when (val a = args.firstOrNull()) {
                is Value.Str -> a.v.length.toDouble()
                is Value.Lst -> a.v.size.toDouble()
                is Value.Dct -> a.v.size.toDouble()
                else -> throw PyError(null, "len() needs text or a list.")
            })
            "str" -> return Value.Str(stringify(args.firstOrNull() ?: Value.None))
            "int" -> return Value.Num((asNum(args.first())).toInt().toDouble())
            "float" -> return Value.Num(asNum(args.first()))
            "range" -> {
                val (start, end, step) = when (args.size) {
                    1 -> Triple(0, asNum(args[0]).toInt(), 1)
                    2 -> Triple(asNum(args[0]).toInt(), asNum(args[1]).toInt(), 1)
                    else -> Triple(asNum(args[0]).toInt(), asNum(args[1]).toInt(), asNum(args[2]).toInt())
                }
                val list = ArrayList<Value>()
                if (step == 0) throw PyError(null, "range() step can't be zero.")
                var i = start
                while ((step > 0 && i < end) || (step < 0 && i > end)) {
                    list.add(Value.Num(i.toDouble())); i += step
                    if (list.size > maxLoopIterations) throw PyError(null, "That range is too big.")
                }
                return Value.Lst(list)
            }
            "sum" -> return Value.Num(listArg(args).sumOf { asNum(it) })
            "max" -> return Value.Num(listArg(args).maxOf { asNum(it) })
            "min" -> return Value.Num(listArg(args).minOf { asNum(it) })
            "input" -> { return Value.Str("Friend") } // offline stub
        }
        val fn = functions[name] ?: throw PyError(null, "I don't know a function called '$name'.")
        if (args.size != fn.params.size) {
            throw PyError(fn.defLine, "'$name' expected ${fn.params.size} value(s) but got ${args.size}.")
        }
        val local = HashMap(globals)
        fn.params.forEachIndexed { i, p -> local[p] = args[i] }
        return try { execBlock(fn.body, local); Value.None } catch (r: ReturnSignal) { r.value }
    }

    private fun listArg(args: List<Value>): List<Value> {
        val a = args.firstOrNull()
        return when (a) {
            is Value.Lst -> a.v
            else -> if (args.size > 1) args else throw PyError(null, "This builtin needs a list.")
        }
    }

    private fun index(container: Value, key: Value): Value = when (container) {
        is Value.Str -> {
            val i = asNum(key).toInt()
            if (i !in container.v.indices) throw PyError(null, "That text position doesn't exist.")
            Value.Str(container.v[i].toString())
        }
        is Value.Lst -> {
            val i = asNum(key).toInt()
            if (i !in container.v.indices) throw PyError(null, "That list position doesn't exist.")
            container.v[i]
        }
        is Value.Dct -> container.v.entries.firstOrNull { valueEquals(it.key, key) }?.value
            ?: throw PyError(null, "That key isn't in the dictionary.")
        else -> throw PyError(null, "You can only index text, lists, or dictionaries.")
    }

    private fun valueEquals(a: Value, b: Value): Boolean = when {
        a is Value.Num && b is Value.Num -> a.v == b.v
        a is Value.Str && b is Value.Str -> a.v == b.v
        a is Value.Bool && b is Value.Bool -> a.v == b.v
        a is Value.None && b is Value.None -> true
        else -> false
    }

    private fun truthy(v: Value): Boolean = when (v) {
        is Value.Bool -> v.v
        is Value.Num -> v.v != 0.0
        is Value.Str -> v.v.isNotEmpty()
        is Value.Lst -> v.v.isNotEmpty()
        is Value.Dct -> v.v.isNotEmpty()
        is Value.None -> false
    }

    private fun asNum(v: Value): Double = when (v) {
        is Value.Num -> v.v
        is Value.Bool -> if (v.v) 1.0 else 0.0
        is Value.Str -> v.v.trim().toDoubleOrNull() ?: throw PyError(null, "'${v.v}' is not a number.")
        else -> throw PyError(null, "Expected a number here.")
    }

    private fun stringify(v: Value): String = when (v) {
        is Value.Num -> if (v.v == v.v.toLong().toDouble()) v.v.toLong().toString() else v.v.toString()
        is Value.Str -> v.v
        is Value.Bool -> if (v.v) "True" else "False"
        is Value.None -> "None"
        is Value.Lst -> v.v.joinToString(prefix = "[", postfix = "]") { reprify(it) }
        is Value.Dct -> v.v.entries.joinToString(prefix = "{", postfix = "}") { "${reprify(it.key)}: ${reprify(it.value)}" }
    }

    private fun reprify(v: Value): String = if (v is Value.Str) "'${v.v}'" else stringify(v)

    private fun appendOut(s: String) {
        if (out.length + s.length > maxOutputChars) {
            out.append(s.take(maxOutputChars - out.length))
            throw PyError(null, "Output got very long, so I stopped early.")
        }
        out.append(s)
    }

    private fun guardIterations(line: Int) {
        if (++iterations > maxLoopIterations) throw PyError(line, "This loop ran too many times. Check the condition.")
    }
}
