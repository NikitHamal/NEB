package com.consica.code.domain.python

internal sealed class Stmt {
    var line: Int = 0
}

internal class ExprStmt(val expr: Expr) : Stmt()
internal class Assign(val target: Expr, val value: Expr) : Stmt()
internal class AugAssign(val target: Expr, val op: String, val value: Expr) : Stmt()
internal class If(val branches: List<Pair<Expr, List<Stmt>>>, val elseBody: List<Stmt>?) : Stmt()
internal class While(val cond: Expr, val body: List<Stmt>) : Stmt()
internal class For(val varName: String, val iterable: Expr, val body: List<Stmt>) : Stmt()
internal class FuncDef(val name: String, val params: List<String>, val body: List<Stmt>) : Stmt()
internal class Return(val value: Expr?) : Stmt()
internal class Break : Stmt()
internal class Continue : Stmt()
internal class Pass : Stmt()

internal sealed class Expr {
    var line: Int = 0
}

internal class Literal(val value: Any) : Expr()
internal class NameExpr(val id: String) : Expr()
internal class ListLit(val items: List<Expr>) : Expr()
internal class FStr(val parts: List<Any>) : Expr()
internal class Bin(val op: String, val left: Expr, val right: Expr) : Expr()
internal class BoolOp(val op: String, val left: Expr, val right: Expr) : Expr()
internal class NotOp(val operand: Expr) : Expr()
internal class Unary(val op: String, val operand: Expr) : Expr()
internal class Compare(val first: Expr, val rest: List<Pair<String, Expr>>) : Expr()
internal class Call(val func: Expr, val args: List<Expr>, val kwargs: List<Pair<String, Expr>>) : Expr()
internal class Attr(val obj: Expr, val name: String) : Expr()
internal class IndexExpr(val obj: Expr, val index: Expr) : Expr()
internal class SliceExpr(val obj: Expr, val lo: Expr?, val hi: Expr?, val step: Expr?) : Expr()
