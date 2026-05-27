package com.neb.ians.data.local

import androidx.room.TypeConverter
import com.neb.ians.data.model.Grade
import com.neb.ians.data.model.ResourceType
import com.neb.ians.data.model.Subject

class NebConverters {
    @TypeConverter fun fromSubject(v: Subject): String = v.name
    @TypeConverter fun toSubject(v: String): Subject = runCatching { Subject.valueOf(v) }.getOrDefault(Subject.Other)
    @TypeConverter fun fromGrade(v: Grade): String = v.name
    @TypeConverter fun toGrade(v: String): Grade = runCatching { Grade.valueOf(v) }.getOrDefault(Grade.Other)
    @TypeConverter fun fromType(v: ResourceType): String = v.name
    @TypeConverter fun toType(v: String): ResourceType = runCatching { ResourceType.valueOf(v) }.getOrDefault(ResourceType.Other)
    @TypeConverter fun fromAnnKind(v: AnnotationKind): String = v.name
    @TypeConverter fun toAnnKind(v: String): AnnotationKind = runCatching { AnnotationKind.valueOf(v) }.getOrDefault(AnnotationKind.Highlight)
}
