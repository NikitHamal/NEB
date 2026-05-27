package com.neb.ians.data.repository

import com.neb.ians.data.db.ResourceDao
import com.neb.ians.data.db.ResourceEntity
import com.neb.ians.data.model.Grade
import com.neb.ians.data.model.Resource
import com.neb.ians.data.model.ResourceType
import com.neb.ians.data.model.Subject
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map

class ResourceRepository(private val dao: ResourceDao) {

    val allResourcesFlow: Flow<List<Resource>> = dao.getAll().map { list ->
        list.map { it.toModel() }
    }

    suspend fun getAll(): List<Resource> {
        return dao.getAll().map { list -> list.map { it.toModel() } }.first()
    }

    suspend fun getByCategory(subject: Subject, grade: Grade, type: ResourceType): List<Resource> {
        return dao.getByCategory(subject.name, grade.name, type.name).map { it.toModel() }
    }

    suspend fun search(query: String): List<Resource> {
        return if (query.isBlank()) {
            emptyList()
        } else {
            dao.search(query).map { it.toModel() }
        }
    }

    suspend fun seedData() {
        val sample = listOf(
            ResourceEntity("1", "Physics Grade 11 Textbook", Subject.PHYSICS.name, Grade.GRADE_11.name, ResourceType.TEXTBOOK.name, "https://example.com/physics11.pdf", fileSizeBytes = 5_000_000),
            ResourceEntity("2", "Chemistry Notes Grade 11", Subject.CHEMISTRY.name, Grade.GRADE_11.name, ResourceType.NOTES.name, "https://example.com/chem11.pdf", fileSizeBytes = 2_000_000),
            ResourceEntity("3", "Mathematics Past Papers 2079", Subject.MATHEMATICS.name, Grade.GRADE_12.name, ResourceType.PAST_PAPERS.name, "https://example.com/math2079.pdf", fileSizeBytes = 3_500_000),
            ResourceEntity("4", "Biology Guide Grade 12", Subject.BIOLOGY.name, Grade.GRADE_12.name, ResourceType.GUIDE.name, "https://example.com/bio12.pdf", fileSizeBytes = 4_000_000),
            ResourceEntity("5", "Computer Science Notes", Subject.COMPUTER.name, Grade.GRADE_11.name, ResourceType.NOTES.name, "https://example.com/cs11.pdf", fileSizeBytes = 1_500_000),
            ResourceEntity("6", "English Grade 11 Textbook", Subject.ENGLISH.name, Grade.GRADE_11.name, ResourceType.TEXTBOOK.name, "https://example.com/eng11.pdf", fileSizeBytes = 3_000_000),
            ResourceEntity("7", "Nepali Grade 12 Notes", Subject.NEPALI.name, Grade.GRADE_12.name, ResourceType.NOTES.name, "https://example.com/nep12.pdf", fileSizeBytes = 1_200_000),
            ResourceEntity("8", "Physics Grade 12 Past Papers", Subject.PHYSICS.name, Grade.GRADE_12.name, ResourceType.PAST_PAPERS.name, "https://example.com/phy12pp.pdf", fileSizeBytes = 2_800_000),
            ResourceEntity("9", "Chemistry Grade 12 Guide", Subject.CHEMISTRY.name, Grade.GRADE_12.name, ResourceType.GUIDE.name, "https://example.com/chem12.pdf", fileSizeBytes = 4_500_000),
            ResourceEntity("10", "Mathematics Grade 11 Textbook", Subject.MATHEMATICS.name, Grade.GRADE_11.name, ResourceType.TEXTBOOK.name, "https://example.com/math11.pdf", fileSizeBytes = 6_000_000)
        )
        dao.insertAll(sample)
    }

    private fun ResourceEntity.toModel() = Resource(
        id = id,
        title = title,
        subject = Subject.valueOf(subject),
        grade = Grade.valueOf(grade),
        type = ResourceType.valueOf(type),
        remoteUrl = remoteUrl,
        localPath = localPath,
        fileSizeBytes = fileSizeBytes,
        isDownloaded = isDownloaded
    )
}
