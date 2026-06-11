package com.consica.code.domain.python

import com.consica.code.domain.execution.FriendlyErrorKind

internal class Parser(private val tokens: List<Token>) {

    private var pos = 0

    private fun peek(offset: Int = 0): Token = tokens[minOf(pos + offset, tokens.size - 1)]
    private fun advance(): Token = tokens[pos++]

    private fun checkOp(op: String): Boolean = peek().type == TokType.OP && peek().text == op
    private fun checkKeyword(kw: String): Boolean = peek().type == TokType.KEYWORD && peek().text == kw

    private fun matchOp(op: String): Boolean {
        if (checkOp(op)) {
            pos++
            return true
        }
        return false
    }

    private fun matchKeyword(kw: String): Boolean {
        if (checkKeyword(kw)) {
            pos++
            return true
        }
        return false
    }

    private fun expectOp(op: String) {
        if (!matchOp(op)) throw syntaxError("SyntaxError: invalid syntax", peek().line)
    }

    private fun expectNewline() {
        if (peek().type == TokType.EOF) return
        if (peek().type != TokType.NEWLINE) throw syntaxError("SyntaxError: invalid syntax", peek().line)
        pos++
    }

    private fun syntaxError(message: String, line: Int) = PyError(FriendlyErrorKind.SYNTAX, message, line)

    private fun <T : Stmt> T.at(line: Int): T = apply { this.line = line }
    private fun <T : Expr> T.at(line: Int): T = apply { this.line = line }

    fun parseProgram(): List<Stmt> {
        val stmts = ArrayList<Stmt>()
        skipNewlines()
        while (peek().type != TokType.EOF) {
            if (peek().type == TokType.INDENT) {
                throw syntaxError("IndentationError: unexpected indent", peek().line)
            }
            if (peek().type == TokType.DEDENT) {
                pos++
                continue
            }
            stmts.addAll(parseStatement())
            skipNewlines()
        }
        return stmts
    }

    private fun skipNewlines() {
        while (peek().type == TokType.NEWLINE) pos++
    }

    private fun parseStatement(): List<Stmt> {
        val tok = peek()
        if (tok.type == TokType.KEYWORD) {
            when (tok.text) {
                "if" -> return listOf(parseIf())
                "while" -> return listOf(parseWhile())
                "for" -> return listOf(parseFor())
                "def" -> return listOf(parseDef())
                "elif", "else" -> throw syntaxError("SyntaxError: invalid syntax", tok.line)
            }
        }
        return parseSimpleLine()
    }

    private fun parseSimpleLine(): List<Stmt> {
        val stmts = ArrayList<Stmt>()
        while (true) {
            stmts.add(parseSmallStmt())
            if (matchOp(";")) {
                if (peek().type == TokType.NEWLINE || peek().type == TokType.EOF) break
                continue
            }
            break
        }
        expectNewline()
        return stmts
    }

    private fun parseSmallStmt(): Stmt {
        val tok = peek()
        if (tok.type == TokType.KEYWORD) {
            when (tok.text) {
                "return" -> {
                    advance()
                    val value = if (atStatementEnd()) null else parseExpr()
                    return Return(value).at(tok.line)
                }
                "break" -> {
                    advance()
                    return Break().at(tok.line)
                }
                "continue" -> {
                    advance()
                    return Continue().at(tok.line)
                }
                "pass" -> {
                    advance()
                    return Pass().at(tok.line)
                }
            }
        }
        val expr = parseExpr()
        if (checkOp("=")) {
            advance()
            validateTarget(expr)
            val value = parseExpr()
            return Assign(expr, value).at(tok.line)
        }
        val augOps = listOf("+=", "-=", "*=", "/=", "//=", "%=", "**=")
        for (op in augOps) {
            if (checkOp(op)) {
                advance()
                validateTarget(expr)
                val value = parseExpr()
                return AugAssign(expr, op.dropLast(1), value).at(tok.line)
            }
        }
        return ExprStmt(expr).at(tok.line)
    }

    private fun atStatementEnd(): Boolean =
        peek().type == TokType.NEWLINE || peek().type == TokType.EOF || checkOp(";")

    private fun validateTarget(target: Expr) {
        when (target) {
            is NameExpr, is IndexExpr -> Unit
            is Literal -> throw syntaxError("SyntaxError: cannot assign to literal", target.line)
            else -> throw syntaxError("SyntaxError: cannot assign to expression", target.line)
        }
    }

    private fun parseBlock(): List<Stmt> {
        expectOp(":")
        if (peek().type == TokType.NEWLINE) {
            pos++
            skipNewlines()
            if (peek().type != TokType.INDENT) {
                throw syntaxError("IndentationError: expected an indented block", peek().line)
            }
            pos++
            val stmts = ArrayList<Stmt>()
            while (peek().type != TokType.DEDENT && peek().type != TokType.EOF) {
                if (peek().type == TokType.NEWLINE) {
                    pos++
                    continue
                }
                if (peek().type == TokType.INDENT) {
                    throw syntaxError("IndentationError: unexpected indent", peek().line)
                }
                stmts.addAll(parseStatement())
            }
            if (peek().type == TokType.DEDENT) pos++
            if (stmts.isEmpty()) {
                throw syntaxError("IndentationError: expected an indented block", peek().line)
            }
            return stmts
        }
        return parseSimpleLine()
    }

    private fun parseIf(): Stmt {
        val line = advance().line
        val branches = ArrayList<Pair<Expr, List<Stmt>>>()
        branches.add(parseExpr() to parseBlock())
        var elseBody: List<Stmt>? = null
        while (true) {
            skipNewlines()
            if (checkKeyword("elif")) {
                advance()
                branches.add(parseExpr() to parseBlock())
            } else if (checkKeyword("else")) {
                advance()
                elseBody = parseBlock()
                break
            } else {
                break
            }
        }
        return If(branches, elseBody).at(line)
    }

    private fun parseWhile(): Stmt {
        val line = advance().line
        val cond = parseExpr()
        val body = parseBlock()
        return While(cond, body).at(line)
    }

    private fun parseFor(): Stmt {
        val line = advance().line
        if (peek().type != TokType.NAME) throw syntaxError("SyntaxError: invalid syntax", peek().line)
        val name = advance().text
        if (!matchKeyword("in")) throw syntaxError("SyntaxError: invalid syntax", peek().line)
        val iterable = parseExpr()
        val body = parseBlock()
        return For(name, iterable, body).at(line)
    }

    private fun parseDef(): Stmt {
        val line = advance().line
        if (peek().type != TokType.NAME) throw syntaxError("SyntaxError: invalid syntax", peek().line)
        val name = advance().text
        expectOp("(")
        val params = ArrayList<String>()
        if (!checkOp(")")) {
            while (true) {
                if (peek().type != TokType.NAME) throw syntaxError("SyntaxError: invalid syntax", peek().line)
                val param = advance().text
                if (param in params) {
                    throw syntaxError("SyntaxError: duplicate argument '$param' in function definition", line)
                }
                params.add(param)
                if (!matchOp(",")) break
                if (checkOp(")")) break
            }
        }
        expectOp(")")
        val body = parseBlock()
        return FuncDef(name, params, body).at(line)
    }

    fun parseExpr(): Expr = parseOr()

    private fun parseOr(): Expr {
        var left = parseAnd()
        while (checkKeyword("or")) {
            val line = advance().line
            left = BoolOp("or", left, parseAnd()).at(line)
        }
        return left
    }

    private fun parseAnd(): Expr {
        var left = parseNot()
        while (checkKeyword("and")) {
            val line = advance().line
            left = BoolOp("and", left, parseNot()).at(line)
        }
        return left
    }

    private fun parseNot(): Expr {
        if (checkKeyword("not")) {
            val line = advance().line
            return NotOp(parseNot()).at(line)
        }
        return parseComparison()
    }

    private fun parseComparison(): Expr {
        val first = parseArith()
        val rest = ArrayList<Pair<String, Expr>>()
        while (true) {
            val op = when {
                checkOp("==") || checkOp("!=") || checkOp("<") || checkOp("<=") || checkOp(">") || checkOp(">=") ->
                    advance().text
                checkKeyword("in") -> {
                    advance()
                    "in"
                }
                checkKeyword("not") && peek(1).type == TokType.KEYWORD && peek(1).text == "in" -> {
                    advance()
                    advance()
                    "not in"
                }
                else -> break
            }
            rest.add(op to parseArith())
        }
        if (rest.isEmpty()) return first
        return Compare(first, rest).at(first.line)
    }

    private fun parseArith(): Expr {
        var left = parseTerm()
        while (checkOp("+") || checkOp("-")) {
            val tok = advance()
            left = Bin(tok.text, left, parseTerm()).at(tok.line)
        }
        return left
    }

    private fun parseTerm(): Expr {
        var left = parseFactor()
        while (checkOp("*") || checkOp("/") || checkOp("//") || checkOp("%")) {
            val tok = advance()
            left = Bin(tok.text, left, parseFactor()).at(tok.line)
        }
        return left
    }

    private fun parseFactor(): Expr {
        if (checkOp("-") || checkOp("+")) {
            val tok = advance()
            return Unary(tok.text, parseFactor()).at(tok.line)
        }
        return parsePower()
    }

    private fun parsePower(): Expr {
        val base = parsePrimary()
        if (checkOp("**")) {
            val tok = advance()
            return Bin("**", base, parseFactor()).at(tok.line)
        }
        return base
    }

    private fun parsePrimary(): Expr {
        var expr = parseAtom()
        while (true) {
            expr = when {
                checkOp("(") -> parseCall(expr)
                checkOp("[") -> parseSubscript(expr)
                checkOp(".") -> {
                    val line = advance().line
                    if (peek().type != TokType.NAME) {
                        throw syntaxError("SyntaxError: invalid syntax", peek().line)
                    }
                    Attr(expr, advance().text).at(line)
                }
                else -> return expr
            }
        }
    }

    private fun parseCall(func: Expr): Expr {
        val line = advance().line
        val args = ArrayList<Expr>()
        val kwargs = ArrayList<Pair<String, Expr>>()
        if (!checkOp(")")) {
            while (true) {
                if (peek().type == TokType.NAME && peek(1).type == TokType.OP && peek(1).text == "=") {
                    val name = advance().text
                    advance()
                    kwargs.add(name to parseExpr())
                } else {
                    if (kwargs.isNotEmpty()) {
                        throw syntaxError("SyntaxError: positional argument follows keyword argument", peek().line)
                    }
                    args.add(parseExpr())
                }
                if (!matchOp(",")) break
                if (checkOp(")")) break
            }
        }
        expectOp(")")
        return Call(func, args, kwargs).at(line)
    }

    private fun parseSubscript(obj: Expr): Expr {
        val line = advance().line
        val lo = if (checkOp(":")) null else parseExpr()
        if (matchOp(":")) {
            val hi = if (checkOp(":") || checkOp("]")) null else parseExpr()
            var step: Expr? = null
            if (matchOp(":")) {
                step = if (checkOp("]")) null else parseExpr()
            }
            expectOp("]")
            return SliceExpr(obj, lo, hi, step).at(line)
        }
        expectOp("]")
        return IndexExpr(obj, lo!!).at(line)
    }

    private fun parseAtom(): Expr {
        val tok = peek()
        when (tok.type) {
            TokType.INT, TokType.FLOAT -> {
                advance()
                return Literal(tok.numValue!!).at(tok.line)
            }
            TokType.STRING -> {
                advance()
                return Literal(tok.text).at(tok.line)
            }
            TokType.FSTRING -> {
                advance()
                val parts = ArrayList<Any>()
                for (p in tok.fparts!!) {
                    when (p) {
                        is FPart.Lit -> parts.add(p.text)
                        is FPart.Expr -> parts.add(parseSubExpression(p.src, tok.line))
                    }
                }
                return FStr(parts).at(tok.line)
            }
            TokType.NAME -> {
                advance()
                return NameExpr(tok.text).at(tok.line)
            }
            TokType.KEYWORD -> when (tok.text) {
                "True" -> {
                    advance()
                    return Literal(true).at(tok.line)
                }
                "False" -> {
                    advance()
                    return Literal(false).at(tok.line)
                }
                "None" -> {
                    advance()
                    return Literal(PyNone).at(tok.line)
                }
                else -> throw syntaxError("SyntaxError: invalid syntax", tok.line)
            }
            TokType.OP -> {
                if (tok.text == "(") {
                    advance()
                    val inner = parseExpr()
                    expectOp(")")
                    return inner
                }
                if (tok.text == "[") {
                    advance()
                    val items = ArrayList<Expr>()
                    if (!checkOp("]")) {
                        while (true) {
                            items.add(parseExpr())
                            if (!matchOp(",")) break
                            if (checkOp("]")) break
                        }
                    }
                    expectOp("]")
                    return ListLit(items).at(tok.line)
                }
                throw syntaxError("SyntaxError: invalid syntax", tok.line)
            }
            else -> throw syntaxError("SyntaxError: invalid syntax", tok.line)
        }
    }

    private fun parseSubExpression(src: String, line: Int): Expr {
        val subTokens = Lexer(src, startLine = line).tokenize()
        val sub = Parser(subTokens)
        val expr = sub.parseExpr()
        if (sub.peek().type != TokType.NEWLINE && sub.peek().type != TokType.EOF) {
            throw syntaxError("SyntaxError: invalid syntax in f-string expression", line)
        }
        return expr
    }
}
