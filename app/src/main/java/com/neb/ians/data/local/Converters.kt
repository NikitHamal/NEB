package com.neb.ians.data.local

import androidx.room.TypeConverter
import com.neb.ians.data.model.AnnotationType

class Converters {
    @TypeConverter
    fun fromAnnotationType(value: AnnotationType): String = value.name

    @TypeConverter
    fun toAnnotationType(value: String): AnnotationType = AnnotationType.valueOf(value)
}
