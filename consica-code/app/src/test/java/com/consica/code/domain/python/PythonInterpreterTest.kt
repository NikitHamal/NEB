package com.consica.code.domain.python

import com.consica.code.domain.execution.ExecutionResult
import com.consica.code.domain.execution.FriendlyErrorKind
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class PythonInterpreterTest {

    private fun run(code: String, stdin: List<String> = emptyList(), maxSteps: Int = 200_000): ExecutionResult =
        PythonInterpreter().run(code, stdin, maxSteps)

    private fun assertOutput(expected: String, code: String, stdin: List<String> = emptyList()) {
        val result = run(code, stdin)
        assertNull("expected success but got ${result.error}", result.error)
        assertEquals(expected, result.output)
    }

    private fun assertError(
        code: String,
        kind: FriendlyErrorKind,
        messagePart: String,
        expectedOutput: String? = null,
        expectedLine: Int? = null,
    ) {
        val result = run(code)
        val error = result.error
        assertNotNull("expected an error", error)
        assertEquals(kind, error!!.kind)
        assertTrue("message '${error.message}' should contain '$messagePart'", error.message.contains(messagePart))
        if (expectedOutput != null) assertEquals(expectedOutput, result.output)
        if (expectedLine != null) assertEquals(expectedLine, error.line)
    }

    // ----------------------------------------------------------- happy paths

    @Test
    fun printHelloWorld() {
        assertOutput("Hello, World!\n", "print(\"Hello, World!\")")
    }

    @Test
    fun printMultipleArgsSpaceSeparated() {
        assertOutput("1 a True None\n\n", "print(1, \"a\", True, None)\nprint()")
    }

    @Test
    fun integerAndFloatArithmetic() {
        assertOutput(
            "3.5\n3\n1\n1024\n2.0\n",
            "print(7 / 2)\nprint(7 // 2)\nprint(7 % 3)\nprint(2 ** 10)\nprint(10 / 5)",
        )
    }

    @Test
    fun floorDivisionAndModuloFollowPythonSignRules() {
        assertOutput("-4\n1\n-4.0\n", "print(-7 // 2)\nprint(-7 % 2)\nprint(-7.0 // 2)")
    }

    @Test
    fun floatReprMatchesPython() {
        assertOutput(
            "0.30000000000000004\n0.3333333333333333\n5.0\n",
            "print(0.1 + 0.2)\nprint(1/3)\nprint(5.0)",
        )
    }

    @Test
    fun stringConcatenationAndRepetition() {
        assertOutput("abcd\nababab\nxxx\n", "print(\"ab\" + \"cd\")\nprint(\"ab\" * 3)\nprint(3 * \"x\")")
    }

    @Test
    fun fStringsInterpolateExpressions() {
        assertOutput(
            "Ana has 6 apples\n",
            "x = 5\nname = \"Ana\"\nprint(f\"{name} has {x + 1} apples\")",
        )
    }

    @Test
    fun fStringWithMethodCallAndBuiltin() {
        assertOutput("up=ABC len=3\n", "s = \"abc\"\nprint(f\"up={s.upper()} len={len(s)}\")")
    }

    @Test
    fun augmentedAssignments() {
        assertOutput("6\n", "x = 10\nx += 5\nx *= 2\nx -= 6\nx //= 4\nprint(x)")
    }

    @Test
    fun ifElifElseBranches() {
        assertOutput(
            "low\nmid\nhigh\n",
            "for x in [1, 5, 10]:\n" +
                "    if x < 3:\n        print(\"low\")\n" +
                "    elif x < 8:\n        print(\"mid\")\n" +
                "    else:\n        print(\"high\")",
        )
    }

    @Test
    fun whileLoopWithBreakAndContinue() {
        assertOutput(
            "1\n2\n4\n5\n",
            "i = 0\nwhile True:\n    i += 1\n    if i == 3:\n        continue\n" +
                "    if i > 5:\n        break\n    print(i)",
        )
    }

    @Test
    fun forOverRangeVariants() {
        assertOutput(
            "0\n1\n2\n2\n3\n4\n10\n7\n4\n1\n",
            "for i in range(3):\n    print(i)\n" +
                "for i in range(2, 5):\n    print(i)\n" +
                "for i in range(10, 0, -3):\n    print(i)",
        )
    }

    @Test
    fun forOverListAndString() {
        assertOutput("10\n20\na\nb\n", "for x in [10, 20]:\n    print(x)\nfor c in \"ab\":\n    print(c)")
    }

    @Test
    fun recursiveFunctionFibonacci() {
        assertOutput(
            "55\n",
            "def fib(n):\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)\nprint(fib(10))",
        )
    }

    @Test
    fun localScopeWithGlobalReadAccess() {
        assertOutput(
            "101\n5\n100\n",
            "g = 100\ndef f():\n    x = 1\n    return x + g\nprint(f())\n" +
                "def h():\n    g = 5\n    return g\nprint(h())\nprint(g)",
        )
    }

    @Test
    fun functionWithoutReturnYieldsNone() {
        assertOutput("None\n", "def f():\n    pass\nprint(f())")
    }

    @Test
    fun listMethodsBattery() {
        assertOutput(
            "[1, 2, 3]\n[3, 2, 1]\n[3, 9, 2, 1]\n1\n3\n[2]\n2\n1\n",
            "a = [3, 1]\na.append(2)\na.sort()\nprint(a)\na.reverse()\nprint(a)\n" +
                "a.insert(1, 9)\nprint(a)\nprint(a.pop())\nprint(a.pop(0))\n" +
                "a.remove(9)\nprint(a)\nprint([1, 2, 2, 3].count(2))\nprint([5, 6, 7].index(6))",
        )
    }

    @Test
    fun stringMethodsBattery() {
        assertOutput(
            "Hello World\nABC\nabc\n['a', 'b', 'c']\n['a', 'b', 'c']\nheLLo\nTrue\nTrue\n2\n2\n-1\na-b\nHello World\nTrue\nFalse\n",
            "s = \"  Hello World  \"\nprint(s.strip())\nprint(\"abc\".upper())\nprint(\"ABC\".lower())\n" +
                "print(\"a,b,c\".split(\",\"))\nprint(\"a b  c\".split())\nprint(\"hello\".replace(\"l\", \"L\"))\n" +
                "print(\"hello\".startswith(\"he\"))\nprint(\"hello\".endswith(\"lo\"))\nprint(\"banana\".count(\"an\"))\n" +
                "print(\"hello\".find(\"ll\"))\nprint(\"hello\".find(\"z\"))\nprint(\"-\".join([\"a\", \"b\"]))\n" +
                "print(\"hello world\".title())\nprint(\"123\".isdigit())\nprint(\"12a\".isdigit())",
        )
    }

    @Test
    fun negativeIndexingAndIndexAssignment() {
        assertOutput(
            "1 3\nb a\n[1, 9, 3]\n",
            "a = [1, 2, 3]\nprint(a[0], a[-1])\ns = \"abc\"\nprint(s[1], s[-3])\na[1] = 9\nprint(a)",
        )
    }

    @Test
    fun slicingListsAndStrings() {
        assertOutput(
            "[1, 2]\n[0, 1]\n[3, 4]\n[3, 4]\n[4, 3, 2, 1, 0]\nell\nhlo\n",
            "a = [0, 1, 2, 3, 4]\nprint(a[1:3])\nprint(a[:2])\nprint(a[3:])\nprint(a[-2:])\n" +
                "print(a[::-1])\nprint(\"hello\"[1:4])\nprint(\"hello\"[::2])",
        )
    }

    @Test
    fun membershipOperators() {
        assertOutput(
            "True\nTrue\nTrue\nTrue\nTrue\n",
            "print(\"ell\" in \"hello\")\nprint(\"z\" not in \"hello\")\nprint(2 in [1, 2])\n" +
                "print(5 not in [1, 2])\nprint(3 in range(5))",
        )
    }

    @Test
    fun chainedComparisons() {
        assertOutput("True\nFalse\nTrue\n", "print(1 < 2 < 3)\nprint(1 < 2 > 5)\nprint(\"a\" < \"b\")")
    }

    @Test
    fun boolOpsShortCircuitAndReturnOperands() {
        assertOutput(
            "x\n2\nTrue\nFalse\nTrue\n",
            "print(0 or \"x\")\nprint(1 and 2)\nprint(not 0)\n" +
                "def boom():\n    return 1 / 0\nprint(False and boom())\nprint(True or boom())",
        )
    }

    @Test
    fun builtinsBattery() {
        assertOutput(
            "3 2 5\n4 2.5\n1 9\n6 4.0\n2 4 2.67\n[1, 2, 3]\n[3, 2, 1]\n['a', 'b']\n[0, 1, 2]\n",
            "print(len(\"abc\"), len([1, 2]), len(range(5)))\nprint(abs(-4), abs(-2.5))\n" +
                "print(min(3, 1, 2), max([4, 9, 2]))\nprint(sum([1, 2, 3]), sum([1.5, 2.5]))\n" +
                "print(round(2.5), round(3.5), round(2.675, 2))\nprint(sorted([3, 1, 2]))\n" +
                "print(sorted([3, 1, 2], reverse=True))\nprint(list(\"ab\"))\nprint(list(range(3)))",
        )
    }

    @Test
    fun typeBuiltinPrintsClassNames() {
        assertOutput(
            "<class 'int'>\n<class 'float'>\n<class 'str'>\n<class 'bool'>\n<class 'list'>\n<class 'NoneType'>\n",
            "print(type(5))\nprint(type(2.0))\nprint(type(\"s\"))\nprint(type(True))\nprint(type([]))\nprint(type(None))",
        )
    }

    @Test
    fun typeConversions() {
        assertOutput(
            "42 3 -3 1\n2.5 3.0\n12!\nFalse False True True\n",
            "print(int(\"42\"), int(3.9), int(-3.9), int(True))\nprint(float(\"2.5\"), float(3))\n" +
                "print(str(12) + \"!\")\nprint(bool(0), bool(\"\"), bool([1]), bool(-1))",
        )
    }

    @Test
    fun inputEchoesPromptAndConsumedLine() {
        assertOutput("Name: Ana\nHi Ana\n", "name = input(\"Name: \")\nprint(\"Hi\", name)", stdin = listOf("Ana"))
    }

    @Test
    fun inputReturnsEmptyStringWhenStdinExhausted() {
        assertOutput("x\n\n0\n", "a = input()\nb = input()\nprint(len(b))", stdin = listOf("x"))
    }

    @Test
    fun intOfInputPattern() {
        assertOutput("n=21\n42\n", "n = int(input(\"n=\"))\nprint(n * 2)", stdin = listOf("21"))
    }

    @Test
    fun listReprUsesSingleQuotesAndPythonLiterals() {
        assertOutput(
            "['a', 1, True, None, [2.5]]\n[\"it's\"]\n",
            "print([\"a\", 1, True, None, [2.5]])\nprint([\"it's\"])",
        )
    }

    @Test
    fun printStringRawButQuotedInsideList() {
        assertOutput("a'b\n[\"a'b\"]\n", "s = \"a'b\"\nprint(s)\nprint([s])")
    }

    @Test
    fun functionKeywordArguments() {
        assertOutput(
            "Hi, Bo\n",
            "def greet(name, greeting):\n    return greeting + \", \" + name\nprint(greet(\"Bo\", greeting=\"Hi\"))",
        )
    }

    @Test
    fun listsArePassedByReference() {
        assertOutput("[1, 99]\n", "def add_item(lst):\n    lst.append(99)\na = [1]\nadd_item(a)\nprint(a)")
    }

    @Test
    fun nestedLoopsWithBreak() {
        assertOutput(
            "0 0\n0 1\n1 0\n1 1\n2 0\n2 1\n",
            "for i in range(3):\n    for j in range(3):\n        if j == 2:\n            break\n        print(i, j)",
        )
    }

    @Test
    fun unaryMinusAndPowerPrecedence() {
        assertOutput("-5\n-4\n0.5\n3\n", "x = 5\nprint(-x)\nprint(-2 ** 2)\nprint(2 ** -1)\nprint(--3)")
    }

    @Test
    fun booleansBehaveAsIntsInArithmetic() {
        assertOutput("2\n3\nTrue\nTrue\n", "print(True + 1)\nprint(True * 3)\nprint(True == 1)\nprint(False == 0)")
    }

    @Test
    fun listConcatRepeatAndInPlaceExtend() {
        assertOutput(
            "[1, 2, 3]\n[0, 0, 0]\n[1, 2]\n",
            "print([1] + [2, 3])\nprint([0] * 3)\na = [1]\nb = a\na += [2]\nprint(b)",
        )
    }

    @Test
    fun printSepAndEndKeywordArguments() {
        assertOutput("1-2\nab\n", "print(1, 2, sep=\"-\")\nprint(\"a\", end=\"\")\nprint(\"b\")")
    }

    @Test
    fun sortedReturnsCopyWithoutMutating() {
        assertOutput("[3, 1, 2]\n[1, 2, 3]\n", "a = [3, 1, 2]\nb = sorted(a)\nprint(a)\nprint(b)")
    }

    @Test
    fun semicolonsAndComments() {
        assertOutput("3\n", "x = 1; y = 2; print(x + y)")
        assertOutput("1\n", "# leading comment\nx = 1  # trailing\n\nprint(x)")
    }

    @Test
    fun userFunctionCanShadowBuiltin() {
        assertOutput("42\n", "def len(x):\n    return 42\nprint(len(\"abc\"))")
    }

    // ---------------------------------------------------------------- errors

    @Test
    fun nameErrorWithLineNumber() {
        assertError("print(x)", FriendlyErrorKind.NAME, "NameError: name 'x' is not defined", "", 1)
    }

    @Test
    fun zeroDivisionErrorKeepsPriorOutput() {
        assertError(
            "print(\"before\")\nprint(1 / 0)",
            FriendlyErrorKind.DIVISION_BY_ZERO,
            "ZeroDivisionError: division by zero",
            "before\n",
            2,
        )
    }

    @Test
    fun integerFloorDivisionByZero() {
        assertError("print(5 // 0)", FriendlyErrorKind.DIVISION_BY_ZERO, "ZeroDivisionError", "", 1)
    }

    @Test
    fun typeErrorOnStringPlusInt() {
        assertError(
            "print(\"a\" + 1)",
            FriendlyErrorKind.TYPE,
            "TypeError: can only concatenate str (not \"int\") to str",
            "",
            1,
        )
    }

    @Test
    fun typeErrorOnIntPlusString() {
        assertError(
            "print(1 + \"a\")",
            FriendlyErrorKind.TYPE,
            "TypeError: unsupported operand type(s) for +: 'int' and 'str'",
            "",
            1,
        )
    }

    @Test
    fun indexErrorOnListAndString() {
        assertError("a = [1]\nprint(a[5])", FriendlyErrorKind.INDEX, "IndexError: list index out of range", "", 2)
        assertError("print(\"ab\"[9])", FriendlyErrorKind.INDEX, "IndexError: string index out of range", "", 1)
    }

    @Test
    fun valueErrorOnInvalidIntLiteral() {
        assertError(
            "print(int(\"abc\"))",
            FriendlyErrorKind.VALUE,
            "ValueError: invalid literal for int() with base 10: 'abc'",
            "",
            1,
        )
    }

    @Test
    fun syntaxErrorOnMalformedCode() {
        assertError("if x", FriendlyErrorKind.SYNTAX, "SyntaxError")
        assertError("print((((", FriendlyErrorKind.SYNTAX, "SyntaxError")
    }

    @Test
    fun timeoutOnInfiniteLoop() {
        assertError(
            "while True:\n    pass",
            FriendlyErrorKind.TIMEOUT,
            "Timeout: program took too long (possible infinite loop)",
        )
    }

    @Test
    fun timeoutRespectsMaxStepsParameter() {
        val result = run("i = 0\nwhile i < 100000:\n    i += 1\nprint(i)", maxSteps = 500)
        assertNotNull(result.error)
        assertEquals(FriendlyErrorKind.TIMEOUT, result.error!!.kind)
        assertFalse(result.isSuccess)
    }

    @Test
    fun outputBeforeErrorIsPreserved() {
        assertError(
            "for i in range(3):\n    print(i)\nprint(nope)",
            FriendlyErrorKind.NAME,
            "NameError",
            "0\n1\n2\n",
            3,
        )
    }

    @Test
    fun wrongArgumentCountErrors() {
        assertError(
            "def f(a, b):\n    return a\nf(1, 2, 3)",
            FriendlyErrorKind.TYPE,
            "f() takes 2 positional arguments but 3 were given",
            "",
            3,
        )
        assertError(
            "def f(a, b):\n    return a\nf(1)",
            FriendlyErrorKind.TYPE,
            "f() missing 1 required positional argument: 'b'",
            "",
            3,
        )
    }

    @Test
    fun returnAndBreakOutsideTheirContexts() {
        assertError("return 5", FriendlyErrorKind.SYNTAX, "'return' outside function", "", 1)
        assertError("break", FriendlyErrorKind.SYNTAX, "'break' outside loop", "", 1)
    }

    @Test
    fun recursionDepthIsBounded() {
        assertError(
            "def f():\n    return f()\nf()",
            FriendlyErrorKind.RUNTIME,
            "RecursionError: maximum recursion depth exceeded",
        )
    }

    @Test
    fun callingNonCallableAndIteratingNonIterable() {
        assertError("x = 5\nx()", FriendlyErrorKind.TYPE, "'int' object is not callable", "", 2)
        assertError("for i in 5:\n    print(i)", FriendlyErrorKind.TYPE, "'int' object is not iterable", "", 1)
    }

    @Test
    fun attributeErrorOnUnknownMethod() {
        assertError(
            "x = 5\nx.append(1)",
            FriendlyErrorKind.RUNTIME,
            "AttributeError: 'int' object has no attribute 'append'",
            "",
            2,
        )
    }

    @Test
    fun listRemoveMissingValueError() {
        assertError("[1].remove(9)", FriendlyErrorKind.VALUE, "list.remove(x): x not in list", "", 1)
    }

    @Test
    fun stringItemAssignmentIsTypeError() {
        assertError(
            "s = \"ab\"\ns[0] = \"x\"",
            FriendlyErrorKind.TYPE,
            "'str' object does not support item assignment",
            "",
            2,
        )
    }

    @Test
    fun incomparableTypesComparisonError() {
        assertError(
            "print(1 < \"a\")",
            FriendlyErrorKind.TYPE,
            "'<' not supported between instances of 'int' and 'str'",
            "",
            1,
        )
    }

    @Test
    fun minOfEmptySequenceIsValueError() {
        assertError("min([])", FriendlyErrorKind.VALUE, "min() arg is an empty sequence", "", 1)
    }

    @Test
    fun errorLineNumberInsideFunctionBody() {
        val result = run("def f():\n    return 1 / 0\nprint(\"go\")\nf()")
        assertNotNull(result.error)
        assertEquals(FriendlyErrorKind.DIVISION_BY_ZERO, result.error!!.kind)
        assertEquals(2, result.error!!.line)
        assertEquals("go\n", result.output)
    }

    @Test
    fun runNeverThrowsAndReportsSuccessFlag() {
        val ok = run("print(1)")
        assertTrue(ok.isSuccess)
        val bad = run("@@@@")
        assertFalse(bad.isSuccess)
        assertNotNull(bad.error)
    }
}
