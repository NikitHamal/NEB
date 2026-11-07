package com.neb.ians.data.local.entity

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * A personal note, stored only on the device. [body] is Markdown; checklist lines are
 * `- [ ]` / `- [x]`. [tone] indexes the tonal fills in `NoteTones`. [trashedAt] is 0 for a
 * live note and the deletion time while it waits in the bin.
 */
@Entity(tableName = "notes")
data class NoteEntity(
    @PrimaryKey val id: String,
    val title: String,
    val body: String,
    val tone: Int,
    val pinned: Boolean,
    val archived: Boolean,
    val trashedAt: Long,
    /** Lowercase tags separated by single spaces. */
    val tags: String,
    val createdAt: Long,
    val updatedAt: Long,
    /** The note as blocks (JSON). Empty for notes written before blocks; they open from [body]. */
    @ColumnInfo(defaultValue = "") val doc: String = "",
) {
    val tagList: List<String>
        get() = tags.split(' ').filter { it.isNotBlank() }

    val isTrashed: Boolean
        get() = trashedAt > 0L
}
