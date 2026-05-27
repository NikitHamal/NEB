package com.neb.ians.data.repo

import com.neb.ians.data.db.ResourceEntity
import com.neb.ians.data.model.Grade
import com.neb.ians.data.model.ResourceType
import com.neb.ians.data.model.Subject

internal object SeedData {
    val resources: List<ResourceEntity> = listOf(
        ResourceEntity(
            id = "phy11-tb",
            title = "Principles of Physics — Grade 11",
            author = "NEB",
            description = "Official Grade 11 Physics textbook covering mechanics, heat, waves and modern physics.",
            subject = Subject.PHYSICS.name,
            grade = Grade.GRADE_11.name,
            type = ResourceType.TEXTBOOK.name,
            sourceUrl = "https://moecdc.gov.np/storage/textbook/physics-11.pdf",
            localPath = null, sizeBytes = 0, pageCount = 0,
        ),
        ResourceEntity(
            id = "chem11-tb",
            title = "Foundation of Chemistry — Grade 11",
            author = "NEB",
            description = "Comprehensive Grade 11 chemistry textbook with theory and numerical practice.",
            subject = Subject.CHEMISTRY.name,
            grade = Grade.GRADE_11.name,
            type = ResourceType.TEXTBOOK.name,
            sourceUrl = "https://moecdc.gov.np/storage/textbook/chemistry-11.pdf",
            localPath = null, sizeBytes = 0, pageCount = 0,
        ),
        ResourceEntity(
            id = "math12-notes",
            title = "Basic Mathematics — Grade 12 Notes",
            author = "Compiled",
            description = "Concise short notes for all chapters of Grade 12 Basic Mathematics.",
            subject = Subject.MATHEMATICS.name,
            grade = Grade.GRADE_12.name,
            type = ResourceType.NOTES.name,
            sourceUrl = "https://example.org/nebians/math12-notes.pdf",
            localPath = null, sizeBytes = 0, pageCount = 0,
        ),
        ResourceEntity(
            id = "bio12-past",
            title = "Biology — Past Papers (2018–2023)",
            author = "NEB",
            description = "Five-year compiled past question papers for Grade 12 Biology.",
            subject = Subject.BIOLOGY.name,
            grade = Grade.GRADE_12.name,
            type = ResourceType.PAST_PAPER.name,
            sourceUrl = "https://example.org/nebians/bio12-past.pdf",
            localPath = null, sizeBytes = 0, pageCount = 0,
        ),
        ResourceEntity(
            id = "eng11-tb",
            title = "Compulsory English — Grade 11",
            author = "NEB",
            description = "Grade 11 compulsory English textbook with literature & writing units.",
            subject = Subject.ENGLISH.name,
            grade = Grade.GRADE_11.name,
            type = ResourceType.TEXTBOOK.name,
            sourceUrl = "https://moecdc.gov.np/storage/textbook/english-11.pdf",
            localPath = null, sizeBytes = 0, pageCount = 0,
        ),
        ResourceEntity(
            id = "cs12-notes",
            title = "Computer Science — Grade 12 Notes",
            author = "Compiled",
            description = "Concise notes on networks, web tech, databases and programming.",
            subject = Subject.COMPUTER.name,
            grade = Grade.GRADE_12.name,
            type = ResourceType.NOTES.name,
            sourceUrl = "https://example.org/nebians/cs12-notes.pdf",
            localPath = null, sizeBytes = 0, pageCount = 0,
        ),
        ResourceEntity(
            id = "neb-syllabus",
            title = "NEB Syllabus — Grade 11 & 12 (All Subjects)",
            author = "CDC",
            description = "Latest CDC syllabus document covering all NEB subjects.",
            subject = Subject.NEPALI.name,
            grade = Grade.GRADE_11.name,
            type = ResourceType.SYLLABUS.name,
            sourceUrl = "https://moecdc.gov.np/storage/syllabus/neb.pdf",
            localPath = null, sizeBytes = 0, pageCount = 0,
        ),
        ResourceEntity(
            id = "acc11-tb",
            title = "Accountancy — Grade 11",
            author = "NEB",
            description = "Grade 11 Accountancy textbook with worked examples.",
            subject = Subject.ACCOUNTANCY.name,
            grade = Grade.GRADE_11.name,
            type = ResourceType.TEXTBOOK.name,
            sourceUrl = "https://moecdc.gov.np/storage/textbook/account-11.pdf",
            localPath = null, sizeBytes = 0, pageCount = 0,
        ),
    )
}
