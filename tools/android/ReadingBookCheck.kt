package com.neb.ians.ui.screens.reader.pdf

import java.io.File

/** JVM check: does a built book carry its structure, and does it unpack? kotlinc ... ReadingBookCheck.kt Pdf{Syntax,Structure,Fonts,Content,Reflow,Vector}.kt ReadingBookFiles.kt */
fun main(args: Array<String>) {
    val f = PdfFile.open(File(args[0])) ?: error("cannot open")
    val bytes = f.embeddedFile(ReadingBookFiles.ATTACHMENT) ?: error("no ${ReadingBookFiles.ATTACHMENT}")
    val dir = ReadingBookFiles.unpack(bytes, File(args[1]))
    println("attachment ${bytes.size} bytes -> ${dir.walkTopDown().count { it.isFile }} files, meta ${File(dir, "meta.json").length()} bytes")
}
