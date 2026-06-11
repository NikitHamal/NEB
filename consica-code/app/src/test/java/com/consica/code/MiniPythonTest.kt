package com.consica.code

import com.consica.code.runtime.html.HtmlSupport
import com.consica.code.runtime.python.MiniPython
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class MiniPythonTest {

    @Test
    fun `print hello`() {
        val r = MiniPython.run("print(\"Hello, Meadow!\")")
        assertTrue(r.success)
        assertEquals("Hello, Meadow!\n", r.output)
    }

    @Test
    fun `variables and math`() {
        val r = MiniPython.run("x = 6 * 7\nprint(x)")
        assertTrue(r.success)
        assertEquals("42\n", r.output)
    }

    @Test
    fun `string concat`() {
        val r = MiniPython.run("a = \"sun\"\nb = \"flower\"\nprint(a + b)")
        assertEquals("sunflower\n", r.output)
    }

    @Test
    fun `if else branch`() {
        val code = """
            sun = 8
            if sun > 5:
                print("grow!")
            else:
                print("rest")
        """.trimIndent()
        val r = MiniPython.run(code)
        assertTrue(r.success)
        assertEquals("grow!\n", r.output)
    }

    @Test
    fun `for loop with range`() {
        val r = MiniPython.run("for i in range(3):\n    print(\"drip\")")
        assertEquals("drip\ndrip\ndrip\n", r.output)
    }

    @Test
    fun `loop counter`() {
        val code = """
            count = 0
            for i in range(3):
                count = count + 1
                print(count)
        """.trimIndent()
        assertEquals("1\n2\n3\n", MiniPython.run(code).output)
    }

    @Test
    fun `lists and iteration`() {
        val code = """
            seeds = ["fern", "moss", "vine"]
            print(seeds[0])
            print(len(seeds))
            for s in seeds:
                print(s)
        """.trimIndent()
        assertEquals("fern\n3\nfern\nmoss\nvine\n", MiniPython.run(code).output)
    }

    @Test
    fun `functions with return`() {
        val code = """
            def double(n):
                return n * 2
            print(double(4))
        """.trimIndent()
        assertEquals("8\n", MiniPython.run(code).output)
    }

    @Test
    fun `function no return prints inside`() {
        val code = """
            def greet():
                print("namaste")

            greet()
        """.trimIndent()
        assertEquals("namaste\n", MiniPython.run(code).output)
    }

    @Test
    fun `name error reported with line`() {
        val r = MiniPython.run("season = \"autumn\"\nprnt(\"harvest time\")")
        assertFalse(r.success)
        assertEquals("NameError", r.error?.kind)
        assertEquals(2, r.error?.line)
    }

    @Test
    fun `division by zero`() {
        val r = MiniPython.run("print(1 / 0)")
        assertFalse(r.success)
        assertEquals("ZeroDivisionError", r.error?.kind)
    }

    @Test
    fun `infinite loop bounded`() {
        val r = MiniPython.run("while True:\n    x = 1")
        assertFalse(r.success)
        assertEquals("TimeoutError", r.error?.kind)
    }

    @Test
    fun `nested conditionals`() {
        val code = """
            rain = 7
            if rain > 5:
                if rain > 10:
                    print("flood watch")
                else:
                    print("good rain")
            else:
                print("dry day")
        """.trimIndent()
        assertEquals("good rain\n", MiniPython.run(code).output)
    }

    @Test
    fun `advanced data crunch lesson`() {
        val code = """
            rain = [4, 12, 8, 20, 15, 3]
            total = 0
            for r in rain:
                if r > 10:
                    total = total + r
            print(total)
        """.trimIndent()
        assertEquals("47\n", MiniPython.run(code).output)
    }

    @Test
    fun `debug lesson fixed code`() {
        val code = """
            values = [10, 20, 30]
            total = 0
            for v in values:
                total = total + v
            average = total / 3
            print("average:", average)
        """.trimIndent()
        val r = MiniPython.run(code)
        assertTrue(r.success)
        assertTrue(r.output.contains("average: 20"))
    }

    @Test
    fun `augmented assignment and while`() {
        val code = """
            n = 0
            while n < 3:
                n += 1
            print(n)
        """.trimIndent()
        assertEquals("3\n", MiniPython.run(code).output)
    }

    @Test
    fun `builtins sum min max sorted`() {
        val code = """
            nums = [3, 1, 2]
            print(sum(nums))
            print(min(nums))
            print(max(nums))
            print(sorted(nums))
        """.trimIndent()
        assertEquals("6\n1\n3\n[1, 2, 3]\n", MiniPython.run(code).output)
    }

    @Test
    fun `linear search algorithm puzzle`() {
        val code = """
            seeds = ["fern", "moss", "vine"]
            target = "moss"
            found = False
            for s in seeds:
                if s == target:
                    found = True
            print(found)
        """.trimIndent()
        assertEquals("True\n", MiniPython.run(code).output)
    }

    @Test
    fun `list append and pop`() {
        val code = """
            basket = []
            basket.append("apple")
            basket.append("mango")
            print(len(basket))
            basket.pop()
            print(basket)
        """.trimIndent()
        assertEquals("2\n['apple']\n", MiniPython.run(code).output)
    }

    @Test
    fun `string methods`() {
        assertEquals("HELLO\n", MiniPython.run("print(\"hello\".upper())").output)
    }
}

class HtmlSupportTest {

    @Test
    fun `detects h1 with content`() {
        assertTrue(HtmlSupport.hasTag("<h1>Sprout</h1>", "h1", "Sprout"))
        assertFalse(HtmlSupport.hasTag("<h2>Sprout</h2>", "h1"))
        assertFalse(HtmlSupport.hasTag("<h1>Tree</h1>", "h1", "Sprout"))
    }

    @Test
    fun `detects void img tag`() {
        assertTrue(HtmlSupport.hasTag("<img src=\"a.png\" alt=\"a\">", "img"))
    }

    @Test
    fun `unclosed tags reported`() {
        assertTrue(HtmlSupport.findUnclosedTags("<h1>Hello").contains("h1"))
        assertTrue(HtmlSupport.findUnclosedTags("<h1>Hello</h1>").isEmpty())
    }

    @Test
    fun `wrap preview only when fragment`() {
        assertTrue(HtmlSupport.wrapForPreview("<h1>x</h1>", false).contains("<!DOCTYPE html>"))
        val full = "<html><body>hi</body></html>"
        assertEquals(full, HtmlSupport.wrapForPreview(full, false))
    }
}
