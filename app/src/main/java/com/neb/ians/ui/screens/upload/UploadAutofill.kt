package com.neb.ians.ui.screens.upload

/**
 * Everything the screen can work out for itself.
 *
 * A file already carries most of what the old form asked for: its name is
 * usually the title, its extension is the type, and a camera filename is a
 * useful signal too — it means the name is noise and the title box should stay
 * empty rather than be filled with IMG_20240912_181204.
 */
object UploadAutofill {

    private val CAMERA_NAME = Regex(
        "^(img|pxl|dsc|dcim|photo|image|screenshot|scan|doc|20\\d{6})[ _-]?\\d*.*$",
        RegexOption.IGNORE_CASE
    )

    private val AUDIO_EXTENSIONS = setOf("mp3", "m4a", "wav", "ogg", "opus", "aac", "flac")
    private val SLIDE_EXTENSIONS = setOf("ppt", "pptx", "odp", "key")

    /** A title worth prefilling, or blank when the filename says nothing. */
    fun titleFrom(fileName: String): String {
        val stem = fileName.substringBeforeLast('.', fileName).trim()
        if (stem.isBlank() || CAMERA_NAME.matches(stem)) return ""
        val cleaned = stem
            .replace(Regex("[_]+"), " ")
            .replace(Regex("\\s+"), " ")
            .trim()
        if (cleaned.length < 3) return ""
        return cleaned.replaceFirstChar { it.uppercaseChar() }.take(120)
    }

    /**
     * The resource type the files themselves imply. A set of page photos is a
     * note, not a pile of images, because that is what it becomes on upload.
     */
    fun typeFor(fileNames: List<String>, combinedPages: Boolean): String {
        if (combinedPages) return "Note"
        val name = fileNames.firstOrNull().orEmpty()
        val extension = name.substringAfterLast('.', "").lowercase()
        return when {
            extension == "pdf" -> "PDF"
            UploadOptions.isVideoFileName(name) -> "Video"
            extension in AUDIO_EXTENSIONS -> "Audio"
            extension in SLIDE_EXTENSIONS -> "Presentation"
            extension in setOf("jpg", "jpeg", "png", "webp", "heic", "heif", "bmp") -> "Image"
            else -> "PDF"
        }
    }

    /** A subject named in the filename, when one of the known subjects is in there. */
    fun subjectFrom(fileName: String, known: List<String>): String {
        val haystack = fileName.lowercase()
        return known.firstOrNull { subject ->
            val needle = subject.lowercase()
            needle.length > 3 && haystack.contains(needle)
        }.orEmpty()
    }
}
