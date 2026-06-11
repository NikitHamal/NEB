package com.consica.code.domain.python

import com.consica.code.domain.execution.ExecutionError
import com.consica.code.domain.execution.ExecutionResult
import com.consica.code.domain.execution.FriendlyErrorKind
import java.math.BigDecimal
import java.math.RoundingMode
import kotlin.math.abs
import kotlin.math.floor
import kotlin.math.pow

/** Singleton representing Python's None value. */
internal object PyNone {
    override fun toString(): String = "None"
}

/** Lazy range object matching Python's range() semantics. */
internal class PyRange(val start: Long, val stop: Long, val step: Long) {
    val size: Long
        get() = if (step > 0) {
            if (stop <= start) 0L else (stop - start + step - 1) / step
        } else {
            if (start <= stop) 0L else (start - stop - step - 1) / (-step)
        }

    fun elementAt(i: Long): Long = start + i * step

    fun containsValue(v: Long): Boolean {
        if (step > 0) {
            if (v < start || v >= stop) return false
        } else {
            if (v > start || v <= stop) return false
        }
        return (v - start) % step == 0L
    }
}

/** A user-defined function created by a `def` statement. */
internal class PyFunction(val def: FuncDef)

/** A reference to one of the interpreter built-in functions. */
internal class BuiltinFunc(val name: String)

/** A method bound to a receiver object (e.g. `myList.append`). */
internal class BoundMethod(val recv: Any, val name: String)

/** Result of calling type(x). */
internal class PyType(val name: String) {
    override fun equals(other: Any?): Boolean = other is PyType && other.name == name
    override fun hashCode(): Int = name.hashCode()
}

// Control-flow signals (stackless exceptions).
private class BreakSignal : RuntimeException(null, null, false, false)
private class ContinueSignal : RuntimeException(null, null, false, false)
private class ReturnSignal(val value: Any) : RuntimeException(null, null, false, false)

private val BUILTIN_NAMES = setOf(
    "print", "input", "len", "range", "str", "int", "float", "bool",
    "abs", "min", "max", "sum", "round", "type", "sorted", "list",
)

private val LIST_METHODS = setOf(
    "append", "pop", "remove", "insert", "index", "count", "sort", "reverse",
)

private val STR_METHODS = setOf(
    "upper", "lower", "strip", "split", "replace", "startswith", "endswith",
    "count", "find", "join", "title", "isdigit",
)

private const val MAX_SEQUENCE_SIZE = 1_000_000
private const val MAX_CALL_DEPTH = 900

/**
 * Tree-walking interpreter for the educational Python 3 subset supported by
 * [Lexer] and [Parser]. The [run] method never throws: every failure is
 * converted into an [ExecutionResult] carrying an [ExecutionError].
 */
class PythonInterpreter {

    fun run(code: String, stdin: List<String> = emptyList(), maxSteps: Int = 200_000): ExecutionResult {
        val startedAt = System.nanoTime()
        val out = StringBuilder()
        fun elapsedMs() = (System.nanoTime() - startedAt) / 1_000_000
        return try {
            val tokens = Lexer(code).tokenize()
            val program = Parser(tokens).parseProgram()
            Evaluator(out, stdin, maxSteps).execProgram(program)
            ExecutionResult(out.toString(), null, elapsedMs())
        } catch (e: PyError) {
            ExecutionResult(out.toString(), ExecutionError(e.message, e.line, e.kind), elapsedMs())
        } catch (e: StackOverflowError) {
            ExecutionResult(
                out.toString(),
                ExecutionError("RecursionError: maximum recursion depth exceeded", null, FriendlyErrorKind.RUNTIME),
                elapsedMs(),
            )
        } catch (e: Throwable) {
            ExecutionResult(
                out.toString(),
                ExecutionError(
                    "RuntimeError: ${e.message ?: e::class.simpleName ?: "unexpected internal error"}",
                    null,
                    FriendlyErrorKind.RUNTIME,
                ),
                elapsedMs(),
            )
        }
    }
}

private class Evaluator(
    private val out: StringBuilder,
    private val stdin: List<String>,
    private val maxSteps: Int,
) {

    private val globals = HashMap<String, Any>()
    private val frames = ArrayDeque<HashMap<String, Any>>()
    private var steps = 0
    private var loopDepth = 0
    private var callDepth = 0
    private var stdinIndex = 0

    // ------------------------------------------------------------------ exec

    fun execProgram(program: List<Stmt>) {
        for (stmt in program) execStmt(stmt)
    }

    private fun step(line: Int) {
        if (++steps > maxSteps) {
            throw PyError(
                FriendlyErrorKind.TIMEOUT,
                "Timeout: program took too long (possible infinite loop)",
                line,
            )
        }
    }

    private fun execBlock(body: List<Stmt>) {
        for (stmt in body) execStmt(stmt)
    }

    private fun execStmt(stmt: Stmt) {
        step(stmt.line)
        try {
            execStmtInner(stmt)
        } catch (e: PyError) {
            throw if (e.line == null) PyError(e.kind, e.message, stmt.line) else e
        }
    }

    private fun execStmtInner(stmt: Stmt) {
        when (stmt) {
            is ExprStmt -> eval(stmt.expr)
            is Assign -> execAssign(stmt)
            is AugAssign -> execAugAssign(stmt)
            is If -> {
                for ((cond, body) in stmt.branches) {
                    if (truthy(eval(cond))) {
                        execBlock(body)
                        return
                    }
                }
                stmt.elseBody?.let { execBlock(it) }
            }
            is While -> execWhile(stmt)
            is For -> execFor(stmt)
            is FuncDef -> assignName(stmt.name, PyFunction(stmt))
            is Return -> {
                if (callDepth == 0) {
                    throw PyError(FriendlyErrorKind.SYNTAX, "SyntaxError: 'return' outside function", stmt.line)
                }
                throw ReturnSignal(stmt.value?.let { eval(it) } ?: PyNone)
            }
            is Break -> {
                if (loopDepth == 0) {
                    throw PyError(FriendlyErrorKind.SYNTAX, "SyntaxError: 'break' outside loop", stmt.line)
                }
                throw BreakSignal()
            }
            is Continue -> {
                if (loopDepth == 0) {
                    throw PyError(FriendlyErrorKind.SYNTAX, "SyntaxError: 'continue' not properly in loop", stmt.line)
                }
                throw ContinueSignal()
            }
            is Pass -> Unit
        }
    }

    private fun execAssign(stmt: Assign) {
        val value = eval(stmt.value)
        when (val target = stmt.target) {
            is NameExpr -> assignName(target.id, value)
            is IndexExpr -> setIndex(eval(target.obj), eval(target.index), value, target.line)
            else -> throw PyError(FriendlyErrorKind.SYNTAX, "SyntaxError: cannot assign to expression", stmt.line)
        }
    }

    private fun execAugAssign(stmt: AugAssign) {
        when (val target = stmt.target) {
            is NameExpr -> {
                val current = lookupName(target.id, target.line)
                val rhs = eval(stmt.value)
                if (stmt.op == "+" && current is ArrayList<*> && rhs is ArrayList<*>) {
                    @Suppress("UNCHECKED_CAST")
                    (current as ArrayList<Any>).addAll(rhs as ArrayList<Any>)
                } else {
                    assignName(target.id, binaryOp(stmt.op, current, rhs, stmt.line))
                }
            }
            is IndexExpr -> {
                val obj = eval(target.obj)
                val idx = eval(target.index)
                val current = getIndex(obj, idx, target.line)
                val rhs = eval(stmt.value)
                if (stmt.op == "+" && current is ArrayList<*> && rhs is ArrayList<*>) {
                    @Suppress("UNCHECKED_CAST")
                    (current as ArrayList<Any>).addAll(rhs as ArrayList<Any>)
                } else {
                    setIndex(obj, idx, binaryOp(stmt.op, current, rhs, stmt.line), target.line)
                }
            }
            else -> throw PyError(FriendlyErrorKind.SYNTAX, "SyntaxError: cannot assign to expression", stmt.line)
        }
    }

    private fun execWhile(stmt: While) {
        loopDepth++
        try {
            while (true) {
                step(stmt.line)
                if (!truthy(eval(stmt.cond))) break
                try {
                    execBlock(stmt.body)
                } catch (b: BreakSignal) {
                    break
                } catch (c: ContinueSignal) {
                    // next iteration
                }
            }
        } finally {
            loopDepth--
        }
    }

    private fun execFor(stmt: For) {
        val iterable = eval(stmt.iterable)
        loopDepth++
        try {
            when (iterable) {
                is ArrayList<*> -> {
                    var i = 0
                    loop@ while (i < iterable.size) {
                        step(stmt.line)
                        assignName(stmt.varName, iterable[i] as Any)
                        try {
                            execBlock(stmt.body)
                        } catch (b: BreakSignal) {
                            break@loop
                        } catch (c: ContinueSignal) {
                            // next iteration
                        }
                        i++
                    }
                }
                is String -> {
                    loop@ for (ch in iterable) {
                        step(stmt.line)
                        assignName(stmt.varName, ch.toString())
                        try {
                            execBlock(stmt.body)
                        } catch (b: BreakSignal) {
                            break@loop
                        } catch (c: ContinueSignal) {
                            // next iteration
                        }
                    }
                }
                is PyRange -> {
                    var i = 0L
                    val size = iterable.size
                    loop@ while (i < size) {
                        step(stmt.line)
                        assignName(stmt.varName, iterable.elementAt(i))
                        try {
                            execBlock(stmt.body)
                        } catch (b: BreakSignal) {
                            break@loop
                        } catch (c: ContinueSignal) {
                            // next iteration
                        }
                        i++
                    }
                }
                else -> throw typeError("'${typeName(iterable)}' object is not iterable", stmt.line)
            }
        } finally {
            loopDepth--
        }
    }

    // ----------------------------------------------------------------- names

    private fun assignName(name: String, value: Any) {
        (frames.lastOrNull() ?: globals)[name] = value
    }

    private fun lookupName(name: String, line: Int): Any {
        frames.lastOrNull()?.get(name)?.let { return it }
        globals[name]?.let { return it }
        if (name in BUILTIN_NAMES) return BuiltinFunc(name)
        throw PyError(FriendlyErrorKind.NAME, "NameError: name '$name' is not defined", line)
    }

    // ------------------------------------------------------------------ eval

    private fun eval(expr: Expr): Any {
        try {
            return evalInner(expr)
        } catch (e: PyError) {
            throw if (e.line == null) PyError(e.kind, e.message, expr.line) else e
        }
    }

    private fun evalInner(expr: Expr): Any = when (expr) {
        is Literal -> expr.value
        is NameExpr -> lookupName(expr.id, expr.line)
        is ListLit -> ArrayList<Any>(expr.items.size).apply { expr.items.forEach { add(eval(it)) } }
        is FStr -> buildString {
            for (part in expr.parts) {
                when (part) {
                    is String -> append(part)
                    is Expr -> append(pyStr(eval(part)))
                    else -> append(part.toString())
                }
            }
        }
        is Bin -> binaryOp(expr.op, eval(expr.left), eval(expr.right), expr.line)
        is BoolOp -> {
            val left = eval(expr.left)
            when (expr.op) {
                "and" -> if (!truthy(left)) left else eval(expr.right)
                else -> if (truthy(left)) left else eval(expr.right)
            }
        }
        is NotOp -> !truthy(eval(expr.operand))
        is Unary -> {
            val v = eval(expr.operand)
            val n = numOrNull(v)
                ?: throw typeError("bad operand type for unary ${expr.op}: '${typeName(v)}'", expr.line)
            if (expr.op == "-") {
                if (n is Long) -n else -(n as Double)
            } else {
                n
            }
        }
        is Compare -> evalCompare(expr)
        is Call -> evalCall(expr)
        is Attr -> evalAttr(expr)
        is IndexExpr -> getIndex(eval(expr.obj), eval(expr.index), expr.line)
        is SliceExpr -> evalSlice(expr)
    }

    private fun evalCompare(expr: Compare): Boolean {
        var left = eval(expr.first)
        for ((op, rightExpr) in expr.rest) {
            val right = eval(rightExpr)
            val ok = when (op) {
                "==" -> pyEquals(left, right)
                "!=" -> !pyEquals(left, right)
                "in" -> containsValue(right, left, expr.line)
                "not in" -> !containsValue(right, left, expr.line)
                "<" -> pyCompare(left, right, op, expr.line) < 0
                "<=" -> pyCompare(left, right, op, expr.line) <= 0
                ">" -> pyCompare(left, right, op, expr.line) > 0
                ">=" -> pyCompare(left, right, op, expr.line) >= 0
                else -> throw typeError("unsupported comparison '$op'", expr.line)
            }
            if (!ok) return false
            left = right
        }
        return true
    }

    private fun evalAttr(expr: Attr): Any {
        val obj = eval(expr.obj)
        val valid = when (obj) {
            is ArrayList<*> -> expr.name in LIST_METHODS
            is String -> expr.name in STR_METHODS
            else -> false
        }
        if (!valid) {
            throw PyError(
                FriendlyErrorKind.RUNTIME,
                "AttributeError: '${typeName(obj)}' object has no attribute '${expr.name}'",
                expr.line,
            )
        }
        return BoundMethod(obj, expr.name)
    }

    private fun evalCall(expr: Call): Any {
        val callee = eval(expr.func)
        val args = expr.args.map { eval(it) }
        val kwargs = expr.kwargs.map { it.first to eval(it.second) }
        return when (callee) {
            is PyFunction -> callFunction(callee, args, kwargs, expr.line)
            is BuiltinFunc -> callBuiltin(callee.name, args, kwargs, expr.line)
            is BoundMethod -> callMethod(callee.recv, callee.name, args, kwargs, expr.line)
            else -> throw typeError("'${typeName(callee)}' object is not callable", expr.line)
        }
    }

    // ------------------------------------------------------------- functions

    private fun callFunction(fn: PyFunction, args: List<Any>, kwargs: List<Pair<String, Any>>, line: Int): Any {
        if (callDepth >= MAX_CALL_DEPTH) {
            throw PyError(FriendlyErrorKind.RUNTIME, "RecursionError: maximum recursion depth exceeded", line)
        }
        val params = fn.def.params
        val name = fn.def.name
        if (args.size > params.size) {
            val expected = "${params.size} positional argument" + if (params.size == 1) "" else "s"
            throw typeError("$name() takes $expected but ${args.size} were given", line)
        }
        val locals = HashMap<String, Any>()
        for (i in args.indices) locals[params[i]] = args[i]
        for ((k, v) in kwargs) {
            if (k !in params) throw typeError("$name() got an unexpected keyword argument '$k'", line)
            if (locals.containsKey(k)) throw typeError("$name() got multiple values for argument '$k'", line)
            locals[k] = v
        }
        val missing = params.filter { it !in locals }
        if (missing.isNotEmpty()) {
            val word = if (missing.size == 1) "argument" else "arguments"
            val listed = when (missing.size) {
                1 -> "'${missing[0]}'"
                2 -> "'${missing[0]}' and '${missing[1]}'"
                else -> missing.dropLast(1).joinToString(", ") { "'$it'" } + ", and '${missing.last()}'"
            }
            throw typeError("$name() missing ${missing.size} required positional $word: $listed", line)
        }
        val savedLoopDepth = loopDepth
        loopDepth = 0
        frames.addLast(locals)
        callDepth++
        try {
            execBlock(fn.def.body)
            return PyNone
        } catch (r: ReturnSignal) {
            return r.value
        } finally {
            callDepth--
            frames.removeLast()
            loopDepth = savedLoopDepth
        }
    }

    // -------------------------------------------------------------- builtins

    private fun rejectKwargs(name: String, kwargs: List<Pair<String, Any>>, line: Int) {
        if (kwargs.isNotEmpty()) {
            throw typeError("'${kwargs.first().first}' is an invalid keyword argument for $name()", line)
        }
    }

    private fun requireArgCount(name: String, args: List<Any>, min: Int, max: Int, line: Int) {
        if (args.size < min || args.size > max) {
            val expected = if (min == max) {
                if (min == 1) "exactly one argument" else "exactly $min arguments"
            } else {
                "from $min to $max arguments"
            }
            throw typeError("$name() takes $expected (${args.size} given)", line)
        }
    }

    private fun callBuiltin(name: String, args: List<Any>, kwargs: List<Pair<String, Any>>, line: Int): Any {
        when (name) {
            "print" -> return builtinPrint(args, kwargs, line)
            "input" -> {
                rejectKwargs(name, kwargs, line)
                requireArgCount(name, args, 0, 1, line)
                return builtinInput(args.firstOrNull())
            }
            "len" -> {
                rejectKwargs(name, kwargs, line)
                requireArgCount(name, args, 1, 1, line)
                return when (val v = args[0]) {
                    is String -> v.length.toLong()
                    is ArrayList<*> -> v.size.toLong()
                    is PyRange -> v.size
                    else -> throw typeError("object of type '${typeName(v)}' has no len()", line)
                }
            }
            "range" -> {
                rejectKwargs(name, kwargs, line)
                requireArgCount(name, args, 1, 3, line)
                val parts = args.map {
                    asIndexLong(it)
                        ?: throw typeError("'${typeName(it)}' object cannot be interpreted as an integer", line)
                }
                return when (parts.size) {
                    1 -> PyRange(0, parts[0], 1)
                    2 -> PyRange(parts[0], parts[1], 1)
                    else -> {
                        if (parts[2] == 0L) throw valueError("range() arg 3 must not be zero", line)
                        PyRange(parts[0], parts[1], parts[2])
                    }
                }
            }
            "str" -> {
                rejectKwargs(name, kwargs, line)
                requireArgCount(name, args, 0, 1, line)
                return if (args.isEmpty()) "" else pyStr(args[0])
            }
            "int" -> {
                rejectKwargs(name, kwargs, line)
                requireArgCount(name, args, 0, 1, line)
                return if (args.isEmpty()) 0L else convertToInt(args[0], line)
            }
            "float" -> {
                rejectKwargs(name, kwargs, line)
                requireArgCount(name, args, 0, 1, line)
                return if (args.isEmpty()) 0.0 else convertToFloat(args[0], line)
            }
            "bool" -> {
                rejectKwargs(name, kwargs, line)
                requireArgCount(name, args, 0, 1, line)
                return if (args.isEmpty()) false else truthy(args[0])
            }
            "abs" -> {
                rejectKwargs(name, kwargs, line)
                requireArgCount(name, args, 1, 1, line)
                return when (val n = numOrNull(args[0])) {
                    is Long -> abs(n)
                    is Double -> abs(n)
                    else -> throw typeError("bad operand type for abs(): '${typeName(args[0])}'", line)
                }
            }
            "min", "max" -> return builtinMinMax(name, args, kwargs, line)
            "sum" -> {
                rejectKwargs(name, kwargs, line)
                requireArgCount(name, args, 1, 2, line)
                val items = iterToList(args[0])
                    ?: throw typeError("'${typeName(args[0])}' object is not iterable", line)
                var acc: Any = if (args.size == 2) args[1] else 0L
                for (item in items) acc = binaryOp("+", acc, item, line)
                return acc
            }
            "round" -> {
                rejectKwargs(name, kwargs, line)
                requireArgCount(name, args, 1, 2, line)
                return builtinRound(args, line)
            }
            "type" -> {
                rejectKwargs(name, kwargs, line)
                requireArgCount(name, args, 1, 1, line)
                return PyType(typeName(args[0]))
            }
            "sorted" -> {
                requireArgCount(name, args, 1, 1, line)
                var reverse = false
                for ((k, v) in kwargs) {
                    if (k != "reverse") throw typeError("'$k' is an invalid keyword argument for sorted()", line)
                    reverse = truthy(v)
                }
                val items = iterToList(args[0])
                    ?: throw typeError("'${typeName(args[0])}' object is not iterable", line)
                val result = ArrayList(items)
                sortInPlace(result, reverse, line)
                return result
            }
            "list" -> {
                rejectKwargs(name, kwargs, line)
                requireArgCount(name, args, 0, 1, line)
                if (args.isEmpty()) return ArrayList<Any>()
                return iterToList(args[0])
                    ?: throw typeError("'${typeName(args[0])}' object is not iterable", line)
            }
            else -> throw PyError(FriendlyErrorKind.NAME, "NameError: name '$name' is not defined", line)
        }
    }

    private fun builtinPrint(args: List<Any>, kwargs: List<Pair<String, Any>>, line: Int): Any {
        var sep = " "
        var end = "\n"
        for ((k, v) in kwargs) {
            when (k) {
                "sep" -> sep = if (v === PyNone) " " else v as? String
                    ?: throw typeError("sep must be None or a string, not ${typeName(v)}", line)
                "end" -> end = if (v === PyNone) "\n" else v as? String
                    ?: throw typeError("end must be None or a string, not ${typeName(v)}", line)
                else -> throw typeError("'$k' is an invalid keyword argument for print()", line)
            }
        }
        out.append(args.joinToString(sep) { pyStr(it) }).append(end)
        return PyNone
    }

    private fun builtinInput(prompt: Any?): String {
        if (prompt != null && prompt !== PyNone) out.append(pyStr(prompt))
        val lineValue = if (stdinIndex < stdin.size) stdin[stdinIndex++] else ""
        out.append(lineValue).append('\n')
        return lineValue
    }

    private fun builtinMinMax(name: String, args: List<Any>, kwargs: List<Pair<String, Any>>, line: Int): Any {
        rejectKwargs(name, kwargs, line)
        if (args.isEmpty()) throw typeError("$name expected at least 1 argument, got 0", line)
        val items: List<Any> = if (args.size == 1) {
            iterToList(args[0]) ?: throw typeError("'${typeName(args[0])}' object is not iterable", line)
        } else {
            args
        }
        if (items.isEmpty()) throw valueError("$name() arg is an empty sequence", line)
        var best = items[0]
        for (i in 1 until items.size) {
            val cmp = pyCompare(items[i], best, "<", line)
            if ((name == "min" && cmp < 0) || (name == "max" && cmp > 0)) best = items[i]
        }
        return best
    }

    private fun builtinRound(args: List<Any>, line: Int): Any {
        val v = args[0]
        val nDigits = if (args.size == 2) {
            if (args[1] === PyNone) null
            else asIndexLong(args[1])
                ?: throw typeError("'${typeName(args[1])}' object cannot be interpreted as an integer", line)
        } else null
        return when (val n = numOrNull(v)) {
            is Long -> n
            is Double -> {
                if (nDigits == null) {
                    val r = Math.rint(n)
                    if (r.isNaN() || r.isInfinite() || abs(r) > 9.0e18) {
                        throw valueError("cannot convert float ${formatDouble(n)} to integer", line)
                    }
                    r.toLong()
                } else {
                    if (n.isNaN() || n.isInfinite()) n
                    else BigDecimal(n).setScale(nDigits.toInt(), RoundingMode.HALF_EVEN).toDouble()
                }
            }
            else -> throw typeError("type ${typeName(v)} doesn't define __round__ method", line)
        }
    }

    private fun convertToInt(v: Any, line: Int): Long = when (v) {
        is Boolean -> if (v) 1L else 0L
        is Long -> v
        is Double -> {
            if (v.isNaN()) throw valueError("cannot convert float NaN to integer", line)
            if (v.isInfinite()) throw PyError(
                FriendlyErrorKind.RUNTIME, "OverflowError: cannot convert float infinity to integer", line,
            )
            v.toLong()
        }
        is String -> {
            val t = v.trim()
            t.toLongOrNull()
                ?: throw valueError("invalid literal for int() with base 10: ${reprString(v)}", line)
        }
        else -> throw typeError("int() argument must be a string or a number, not '${typeName(v)}'", line)
    }

    private val floatPattern = Regex("""[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?""")

    private fun convertToFloat(v: Any, line: Int): Double = when (v) {
        is Boolean -> if (v) 1.0 else 0.0
        is Long -> v.toDouble()
        is Double -> v
        is String -> {
            val t = v.trim()
            if (floatPattern.matches(t)) {
                t.toDoubleOrNull()
                    ?: throw valueError("could not convert string to float: ${reprString(v)}", line)
            } else {
                throw valueError("could not convert string to float: ${reprString(v)}", line)
            }
        }
        else -> throw typeError("float() argument must be a string or a number, not '${typeName(v)}'", line)
    }

    // --------------------------------------------------------------- methods

    private fun callMethod(recv: Any, name: String, args: List<Any>, kwargs: List<Pair<String, Any>>, line: Int): Any {
        return when (recv) {
            is ArrayList<*> -> {
                @Suppress("UNCHECKED_CAST")
                callListMethod(recv as ArrayList<Any>, name, args, kwargs, line)
            }
            is String -> callStrMethod(recv, name, args, kwargs, line)
            else -> throw PyError(
                FriendlyErrorKind.RUNTIME,
                "AttributeError: '${typeName(recv)}' object has no attribute '$name'",
                line,
            )
        }
    }

    private fun callListMethod(
        list: ArrayList<Any>,
        name: String,
        args: List<Any>,
        kwargs: List<Pair<String, Any>>,
        line: Int,
    ): Any {
        if (name != "sort") rejectKwargs("$name", kwargs, line)
        when (name) {
            "append" -> {
                requireArgCount("append", args, 1, 1, line)
                list.add(args[0])
                return PyNone
            }
            "pop" -> {
                requireArgCount("pop", args, 0, 1, line)
                if (list.isEmpty()) throw indexError("pop from empty list", line)
                var i = if (args.isEmpty()) {
                    (list.size - 1).toLong()
                } else {
                    asIndexLong(args[0])
                        ?: throw typeError("'${typeName(args[0])}' object cannot be interpreted as an integer", line)
                }
                if (i < 0) i += list.size
                if (i < 0 || i >= list.size) throw indexError("pop index out of range", line)
                return list.removeAt(i.toInt())
            }
            "remove" -> {
                requireArgCount("remove", args, 1, 1, line)
                val idx = list.indexOfFirst { pyEquals(it, args[0]) }
                if (idx < 0) throw valueError("list.remove(x): x not in list", line)
                list.removeAt(idx)
                return PyNone
            }
            "insert" -> {
                requireArgCount("insert", args, 2, 2, line)
                var i = asIndexLong(args[0])
                    ?: throw typeError("'${typeName(args[0])}' object cannot be interpreted as an integer", line)
                if (i < 0) i += list.size
                i = i.coerceIn(0L, list.size.toLong())
                list.add(i.toInt(), args[1])
                return PyNone
            }
            "index" -> {
                requireArgCount("index", args, 1, 1, line)
                val idx = list.indexOfFirst { pyEquals(it, args[0]) }
                if (idx < 0) throw valueError("${pyRepr(args[0])} is not in list", line)
                return idx.toLong()
            }
            "count" -> {
                requireArgCount("count", args, 1, 1, line)
                return list.count { pyEquals(it, args[0]) }.toLong()
            }
            "sort" -> {
                if (args.isNotEmpty()) throw typeError("sort() takes no positional arguments", line)
                var reverse = false
                for ((k, v) in kwargs) {
                    if (k != "reverse") throw typeError("'$k' is an invalid keyword argument for sort()", line)
                    reverse = truthy(v)
                }
                sortInPlace(list, reverse, line)
                return PyNone
            }
            "reverse" -> {
                requireArgCount("reverse", args, 0, 0, line)
                list.reverse()
                return PyNone
            }
            else -> throw PyError(
                FriendlyErrorKind.RUNTIME, "AttributeError: 'list' object has no attribute '$name'", line,
            )
        }
    }

    private fun requireStrArg(method: String, args: List<Any>, i: Int, line: Int): String =
        args[i] as? String ?: throw typeError(
            "$method() argument must be str, not ${typeName(args[i])}", line,
        )

    private fun callStrMethod(
        s: String,
        name: String,
        args: List<Any>,
        kwargs: List<Pair<String, Any>>,
        line: Int,
    ): Any {
        rejectKwargs(name, kwargs, line)
        when (name) {
            "upper" -> {
                requireArgCount("upper", args, 0, 0, line)
                return s.uppercase()
            }
            "lower" -> {
                requireArgCount("lower", args, 0, 0, line)
                return s.lowercase()
            }
            "strip" -> {
                requireArgCount("strip", args, 0, 1, line)
                return if (args.isEmpty()) {
                    s.trim()
                } else {
                    val chars = requireStrArg("strip", args, 0, line)
                    s.trim { it in chars }
                }
            }
            "split" -> {
                requireArgCount("split", args, 0, 1, line)
                return if (args.isEmpty()) {
                    ArrayList<Any>(s.split(Regex("\\s+")).filter { it.isNotEmpty() })
                } else {
                    val sep = requireStrArg("split", args, 0, line)
                    if (sep.isEmpty()) throw valueError("empty separator", line)
                    ArrayList<Any>(s.split(sep))
                }
            }
            "replace" -> {
                requireArgCount("replace", args, 2, 2, line)
                val old = requireStrArg("replace", args, 0, line)
                val new = requireStrArg("replace", args, 1, line)
                return if (old.isEmpty()) {
                    // Python inserts `new` between every character.
                    buildString {
                        append(new)
                        for (c in s) append(c).append(new)
                    }
                } else {
                    s.replace(old, new)
                }
            }
            "startswith" -> {
                requireArgCount("startswith", args, 1, 1, line)
                return s.startsWith(requireStrArg("startswith", args, 0, line))
            }
            "endswith" -> {
                requireArgCount("endswith", args, 1, 1, line)
                return s.endsWith(requireStrArg("endswith", args, 0, line))
            }
            "count" -> {
                requireArgCount("count", args, 1, 1, line)
                val sub = requireStrArg("count", args, 0, line)
                if (sub.isEmpty()) return (s.length + 1).toLong()
                var count = 0L
                var i = 0
                while (true) {
                    val j = s.indexOf(sub, i)
                    if (j < 0) break
                    count++
                    i = j + sub.length
                }
                return count
            }
            "find" -> {
                requireArgCount("find", args, 1, 1, line)
                return s.indexOf(requireStrArg("find", args, 0, line)).toLong()
            }
            "join" -> {
                requireArgCount("join", args, 1, 1, line)
                val items = iterToList(args[0])
                    ?: throw typeError("can only join an iterable", line)
                val parts = ArrayList<String>(items.size)
                for ((i, item) in items.withIndex()) {
                    if (item !is String) {
                        throw typeError("sequence item $i: expected str instance, ${typeName(item)} found", line)
                    }
                    parts.add(item)
                }
                return parts.joinToString(s)
            }
            "title" -> {
                requireArgCount("title", args, 0, 0, line)
                val sb = StringBuilder(s.length)
                var prevLetter = false
                for (c in s) {
                    if (c.isLetter()) {
                        sb.append(if (prevLetter) c.lowercaseChar() else c.uppercaseChar())
                        prevLetter = true
                    } else {
                        sb.append(c)
                        prevLetter = false
                    }
                }
                return sb.toString()
            }
            "isdigit" -> {
                requireArgCount("isdigit", args, 0, 0, line)
                return s.isNotEmpty() && s.all { it.isDigit() }
            }
            else -> throw PyError(
                FriendlyErrorKind.RUNTIME, "AttributeError: 'str' object has no attribute '$name'", line,
            )
        }
    }

    // ------------------------------------------------------------- operators

    private fun binaryOp(op: String, l: Any, r: Any, line: Int): Any {
        val ln = numOrNull(l)
        val rn = numOrNull(r)
        when (op) {
            "+" -> {
                if (ln != null && rn != null) {
                    return if (ln is Long && rn is Long) {
                        val sum = ln + rn
                        // Detect overflow; fall back to double like a "big" value.
                        if (((ln xor sum) and (rn xor sum)) < 0) ln.toDouble() + rn.toDouble() else sum
                    } else {
                        toD(ln) + toD(rn)
                    }
                }
                if (l is String && r is String) return l + r
                if (l is String) {
                    throw typeError("can only concatenate str (not \"${typeName(r)}\") to str", line)
                }
                if (l is ArrayList<*> && r is ArrayList<*>) {
                    val result = ArrayList<Any>(l.size + r.size)
                    @Suppress("UNCHECKED_CAST")
                    result.addAll(l as ArrayList<Any>)
                    @Suppress("UNCHECKED_CAST")
                    result.addAll(r as ArrayList<Any>)
                    return result
                }
                if (l is ArrayList<*>) {
                    throw typeError("can only concatenate list (not \"${typeName(r)}\") to list", line)
                }
                throw typeError("unsupported operand type(s) for +: '${typeName(l)}' and '${typeName(r)}'", line)
            }
            "-" -> {
                if (ln != null && rn != null) {
                    return if (ln is Long && rn is Long) ln - rn else toD(ln) - toD(rn)
                }
                throw typeError("unsupported operand type(s) for -: '${typeName(l)}' and '${typeName(r)}'", line)
            }
            "*" -> {
                if (ln != null && rn != null) {
                    return if (ln is Long && rn is Long) {
                        try {
                            Math.multiplyExact(ln, rn)
                        } catch (e: ArithmeticException) {
                            ln.toDouble() * rn.toDouble()
                        }
                    } else {
                        toD(ln) * toD(rn)
                    }
                }
                if (l is String || r is String) {
                    val str = (l as? String) ?: r as String
                    val other = if (l is String) r else l
                    val count = asIndexLong(other)
                        ?: throw typeError("can't multiply sequence by non-int of type '${typeName(other)}'", line)
                    return repeatString(str, count, line)
                }
                if (l is ArrayList<*> || r is ArrayList<*>) {
                    val listVal = (l as? ArrayList<*>) ?: r as ArrayList<*>
                    val other = if (l is ArrayList<*>) r else l
                    val count = asIndexLong(other)
                        ?: throw typeError("can't multiply sequence by non-int of type '${typeName(other)}'", line)
                    return repeatList(listVal, count, line)
                }
                throw typeError("unsupported operand type(s) for *: '${typeName(l)}' and '${typeName(r)}'", line)
            }
            "/" -> {
                if (ln != null && rn != null) {
                    val divisor = toD(rn)
                    if (divisor == 0.0) throw zeroDiv(line)
                    return toD(ln) / divisor
                }
                throw typeError("unsupported operand type(s) for /: '${typeName(l)}' and '${typeName(r)}'", line)
            }
            "//" -> {
                if (ln != null && rn != null) {
                    return if (ln is Long && rn is Long) {
                        if (rn == 0L) throw zeroDiv(line)
                        Math.floorDiv(ln, rn)
                    } else {
                        val divisor = toD(rn)
                        if (divisor == 0.0) throw zeroDiv(line)
                        floor(toD(ln) / divisor)
                    }
                }
                throw typeError("unsupported operand type(s) for //: '${typeName(l)}' and '${typeName(r)}'", line)
            }
            "%" -> {
                if (ln != null && rn != null) {
                    return if (ln is Long && rn is Long) {
                        if (rn == 0L) throw zeroDiv(line)
                        Math.floorMod(ln, rn)
                    } else {
                        val a = toD(ln)
                        val b = toD(rn)
                        if (b == 0.0) throw zeroDiv(line)
                        val m = a - floor(a / b) * b
                        m
                    }
                }
                throw typeError("unsupported operand type(s) for %: '${typeName(l)}' and '${typeName(r)}'", line)
            }
            "**" -> {
                if (ln != null && rn != null) {
                    if (ln is Long && rn is Long) return intPow(ln, rn, line)
                    val base = toD(ln)
                    val exp = toD(rn)
                    if (base == 0.0 && exp < 0) throw zeroDiv(line)
                    return base.pow(exp)
                }
                throw typeError("unsupported operand type(s) for ** or pow(): '${typeName(l)}' and '${typeName(r)}'", line)
            }
            else -> throw typeError("unsupported operator '$op'", line)
        }
    }

    private fun intPow(b: Long, e: Long, line: Int): Any {
        if (e < 0L) {
            if (b == 0L) throw zeroDiv(line)
            return b.toDouble().pow(e.toDouble())
        }
        return try {
            var result = 1L
            var base = b
            var exp = e
            while (exp > 0) {
                if (exp and 1L == 1L) result = Math.multiplyExact(result, base)
                exp = exp shr 1
                if (exp > 0) base = Math.multiplyExact(base, base)
            }
            result
        } catch (overflow: ArithmeticException) {
            b.toDouble().pow(e.toDouble())
        }
    }

    private fun repeatString(s: String, count: Long, line: Int): String {
        if (count <= 0) return ""
        if (s.length.toLong() * count > MAX_SEQUENCE_SIZE) {
            throw PyError(FriendlyErrorKind.RUNTIME, "MemoryError: repeated string is too large", line)
        }
        return s.repeat(count.toInt())
    }

    private fun repeatList(list: ArrayList<*>, count: Long, line: Int): ArrayList<Any> {
        if (count <= 0) return ArrayList()
        if (list.size.toLong() * count > MAX_SEQUENCE_SIZE) {
            throw PyError(FriendlyErrorKind.RUNTIME, "MemoryError: repeated list is too large", line)
        }
        val result = ArrayList<Any>((list.size * count).toInt())
        repeat(count.toInt()) {
            for (item in list) result.add(item as Any)
        }
        return result
    }

    // ----------------------------------------------------- indexing, slicing

    private fun getIndex(obj: Any, idxVal: Any, line: Int): Any {
        when (obj) {
            is ArrayList<*> -> {
                val i = asIndexLong(idxVal)
                    ?: throw typeError("list indices must be integers or slices, not ${typeName(idxVal)}", line)
                var ii = i
                if (ii < 0) ii += obj.size
                if (ii < 0 || ii >= obj.size) throw indexError("list index out of range", line)
                return obj[ii.toInt()] as Any
            }
            is String -> {
                val i = asIndexLong(idxVal)
                    ?: throw typeError("string indices must be integers, not '${typeName(idxVal)}'", line)
                var ii = i
                if (ii < 0) ii += obj.length
                if (ii < 0 || ii >= obj.length) throw indexError("string index out of range", line)
                return obj[ii.toInt()].toString()
            }
            is PyRange -> {
                val i = asIndexLong(idxVal)
                    ?: throw typeError("range indices must be integers or slices, not ${typeName(idxVal)}", line)
                var ii = i
                if (ii < 0) ii += obj.size
                if (ii < 0 || ii >= obj.size) throw indexError("range object index out of range", line)
                return obj.elementAt(ii)
            }
            else -> throw typeError("'${typeName(obj)}' object is not subscriptable", line)
        }
    }

    private fun setIndex(obj: Any, idxVal: Any, value: Any, line: Int) {
        when (obj) {
            is ArrayList<*> -> {
                val i = asIndexLong(idxVal)
                    ?: throw typeError("list indices must be integers or slices, not ${typeName(idxVal)}", line)
                var ii = i
                if (ii < 0) ii += obj.size
                if (ii < 0 || ii >= obj.size) throw indexError("list assignment index out of range", line)
                @Suppress("UNCHECKED_CAST")
                (obj as ArrayList<Any>)[ii.toInt()] = value
            }
            is String -> throw typeError("'str' object does not support item assignment", line)
            else -> throw typeError("'${typeName(obj)}' object does not support item assignment", line)
        }
    }

    private fun evalSlice(expr: SliceExpr): Any {
        val obj = eval(expr.obj)
        fun bound(e: Expr?): Long? = e?.let {
            val v = eval(it)
            asIndexLong(v)
                ?: throw typeError("slice indices must be integers or None", expr.line)
        }
        val lo = bound(expr.lo)
        val hi = bound(expr.hi)
        val stepValue = bound(expr.step) ?: 1L
        if (stepValue == 0L) throw valueError("slice step cannot be zero", expr.line)
        val length = when (obj) {
            is String -> obj.length.toLong()
            is ArrayList<*> -> obj.size.toLong()
            else -> throw typeError("'${typeName(obj)}' object is not subscriptable", expr.line)
        }
        val (start, stop) = sliceBounds(length, lo, hi, stepValue)
        return when (obj) {
            is String -> buildString {
                var i = start
                while (if (stepValue > 0) i < stop else i > stop) {
                    append(obj[i.toInt()])
                    i += stepValue
                }
            }
            is ArrayList<*> -> {
                val result = ArrayList<Any>()
                var i = start
                while (if (stepValue > 0) i < stop else i > stop) {
                    result.add(obj[i.toInt()] as Any)
                    i += stepValue
                }
                result
            }
            else -> throw typeError("'${typeName(obj)}' object is not subscriptable", expr.line)
        }
    }

    private fun sliceBounds(n: Long, loQ: Long?, hiQ: Long?, step: Long): Pair<Long, Long> {
        var start: Long
        var stop: Long
        if (step > 0) {
            start = loQ ?: 0L
            if (loQ != null) {
                if (start < 0) start += n
                start = start.coerceIn(0L, n)
            }
            stop = hiQ ?: n
            if (hiQ != null) {
                if (stop < 0) stop += n
                stop = stop.coerceIn(0L, n)
            }
        } else {
            start = loQ ?: (n - 1)
            if (loQ != null) {
                if (start < 0) start += n
                start = start.coerceIn(-1L, n - 1)
            }
            stop = hiQ ?: -1L
            if (hiQ != null) {
                if (stop < 0) stop += n
                stop = stop.coerceIn(-1L, n - 1)
            }
        }
        return start to stop
    }

    // ------------------------------------------------- comparisons, equality

    private fun pyEquals(a: Any, b: Any): Boolean {
        val an = numOrNull(a)
        val bn = numOrNull(b)
        if (an != null && bn != null) {
            return if (an is Long && bn is Long) an == bn else toD(an) == toD(bn)
        }
        if (a is String && b is String) return a == b
        if (a is ArrayList<*> && b is ArrayList<*>) {
            if (a.size != b.size) return false
            for (i in a.indices) {
                if (!pyEquals(a[i] as Any, b[i] as Any)) return false
            }
            return true
        }
        return a === b
    }

    private fun pyCompare(a: Any, b: Any, op: String, line: Int): Int {
        val an = numOrNull(a)
        val bn = numOrNull(b)
        if (an != null && bn != null) {
            return if (an is Long && bn is Long) an.compareTo(bn) else toD(an).compareTo(toD(bn))
        }
        if (a is String && b is String) return a.compareTo(b)
        if (a is ArrayList<*> && b is ArrayList<*>) {
            val n = minOf(a.size, b.size)
            for (i in 0 until n) {
                val x = a[i] as Any
                val y = b[i] as Any
                if (!pyEquals(x, y)) return pyCompare(x, y, op, line)
            }
            return a.size.compareTo(b.size)
        }
        throw typeError("'$op' not supported between instances of '${typeName(a)}' and '${typeName(b)}'", line)
    }

    private fun containsValue(container: Any, item: Any, line: Int): Boolean = when (container) {
        is String -> {
            if (item !is String) {
                throw typeError("'in <string>' requires string as left operand, not ${typeName(item)}", line)
            }
            container.contains(item)
        }
        is ArrayList<*> -> container.any { pyEquals(it as Any, item) }
        is PyRange -> when (val n = numOrNull(item)) {
            is Long -> container.containsValue(n)
            is Double -> n == floor(n) && !n.isInfinite() && container.containsValue(n.toLong())
            else -> false
        }
        else -> throw typeError("argument of type '${typeName(container)}' is not iterable", line)
    }

    private fun sortInPlace(list: ArrayList<Any>, reverse: Boolean, line: Int) {
        val comparator = Comparator<Any> { x, y -> if (pyEquals(x, y)) 0 else pyCompare(x, y, "<", line) }
        try {
            list.sortWith(if (reverse) comparator.reversed() else comparator)
        } catch (e: IllegalArgumentException) {
            // Comparator contract violation should not surface as a crash.
            throw typeError("'<' not supported between these instances", line)
        }
    }

    // --------------------------------------------------------------- helpers

    private fun iterToList(v: Any): ArrayList<Any>? = when (v) {
        is ArrayList<*> -> {
            val copy = ArrayList<Any>(v.size)
            for (item in v) copy.add(item as Any)
            copy
        }
        is String -> {
            val copy = ArrayList<Any>(v.length)
            for (c in v) copy.add(c.toString())
            copy
        }
        is PyRange -> {
            if (v.size > MAX_SEQUENCE_SIZE) {
                throw PyError(FriendlyErrorKind.RUNTIME, "MemoryError: range result is too large", null)
            }
            val copy = ArrayList<Any>(v.size.toInt())
            var i = 0L
            while (i < v.size) {
                copy.add(v.elementAt(i))
                i++
            }
            copy
        }
        else -> null
    }

    private fun numOrNull(v: Any): Any? = when (v) {
        is Boolean -> if (v) 1L else 0L
        is Long, is Double -> v
        else -> null
    }

    private fun toD(n: Any): Double = if (n is Long) n.toDouble() else n as Double

    private fun asIndexLong(v: Any): Long? = when (v) {
        is Boolean -> if (v) 1L else 0L
        is Long -> v
        else -> null
    }

    private fun truthy(v: Any): Boolean = when (v) {
        is Boolean -> v
        is Long -> v != 0L
        is Double -> v != 0.0
        is String -> v.isNotEmpty()
        is ArrayList<*> -> v.isNotEmpty()
        PyNone -> false
        is PyRange -> v.size > 0
        else -> true
    }

    private fun typeName(v: Any): String = when (v) {
        is Boolean -> "bool"
        is Long -> "int"
        is Double -> "float"
        is String -> "str"
        is ArrayList<*> -> "list"
        PyNone -> "NoneType"
        is PyRange -> "range"
        is PyFunction -> "function"
        is BuiltinFunc, is BoundMethod -> "builtin_function_or_method"
        is PyType -> "type"
        else -> v::class.simpleName ?: "object"
    }

    private fun pyStr(v: Any): String = when (v) {
        is String -> v
        else -> pyRepr(v)
    }

    private fun pyRepr(v: Any): String = when (v) {
        is Boolean -> if (v) "True" else "False"
        is Long -> v.toString()
        is Double -> formatDouble(v)
        is String -> reprString(v)
        is ArrayList<*> -> v.joinToString(", ", "[", "]") { pyRepr(it as Any) }
        PyNone -> "None"
        is PyRange -> if (v.step == 1L) "range(${v.start}, ${v.stop})" else "range(${v.start}, ${v.stop}, ${v.step})"
        is PyFunction -> "<function ${v.def.name}>"
        is BuiltinFunc -> "<built-in function ${v.name}>"
        is BoundMethod -> "<built-in method ${v.name}>"
        is PyType -> "<class '${v.name}'>"
        else -> v.toString()
    }

    private fun formatDouble(d: Double): String {
        if (d.isNaN()) return "nan"
        if (d.isInfinite()) return if (d > 0) "inf" else "-inf"
        val s = d.toString()
        val eIdx = s.indexOf('E')
        if (eIdx < 0) return s
        var mantissa = s.substring(0, eIdx)
        if (mantissa.endsWith(".0")) mantissa = mantissa.dropLast(2)
        val exp = s.substring(eIdx + 1).toInt()
        val sign = if (exp < 0) "-" else "+"
        val absExp = abs(exp)
        val expStr = if (absExp < 10) "0$absExp" else absExp.toString()
        return "${mantissa}e$sign$expStr"
    }

    private fun reprString(s: String): String {
        val useDouble = s.contains('\'') && !s.contains('"')
        val quote = if (useDouble) '"' else '\''
        val sb = StringBuilder(s.length + 2)
        sb.append(quote)
        for (c in s) {
            when (c) {
                '\\' -> sb.append("\\\\")
                '\n' -> sb.append("\\n")
                '\t' -> sb.append("\\t")
                '\r' -> sb.append("\\r")
                quote -> sb.append('\\').append(quote)
                else -> sb.append(c)
            }
        }
        sb.append(quote)
        return sb.toString()
    }

    private fun typeError(msg: String, line: Int? = null) =
        PyError(FriendlyErrorKind.TYPE, "TypeError: $msg", line)

    private fun valueError(msg: String, line: Int? = null) =
        PyError(FriendlyErrorKind.VALUE, "ValueError: $msg", line)

    private fun indexError(msg: String, line: Int? = null) =
        PyError(FriendlyErrorKind.INDEX, "IndexError: $msg", line)

    private fun zeroDiv(line: Int? = null) =
        PyError(FriendlyErrorKind.DIVISION_BY_ZERO, "ZeroDivisionError: division by zero", line)
}
