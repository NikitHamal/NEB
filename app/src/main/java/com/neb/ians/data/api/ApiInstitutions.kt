package com.neb.ians.data.api

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.JsonElement

// Institutions: the catalogue, the claimed portfolio and the option lists that drive its form.

@Serializable
data class ApiInstRow(
    val slug: String = "",
    val name: String = "",
    val kind: String = "school",
    val kindLabel: String = "",
    val district: String = "",
    val place: String = "",
    val location: String = "",
    val website: String = "",
    val verified: Boolean = false,
    val username: String = "",
    val students: Int = 0,
    val est: String = "",
    val photoUrl: String = "",
    val claimable: Boolean = false,
    val completeness: Int = 0,
    val levels: List<String> = emptyList(),
    val feeMin: Long? = null,
    val feeMax: Long? = null,
    val teachers: Int? = null,
    val studentsTotal: Int? = null,
    val admissionOpen: Boolean = false,
    val facilities: List<String> = emptyList()
)

@Serializable
data class ApiInstSearch(val total: Int = 0, val items: List<ApiInstRow> = emptyList())

@Serializable
data class ApiInstOption(val value: String = "", val label: String = "")

@Serializable
data class ApiInstSchema(
    val levels: List<ApiInstOption> = emptyList(),
    val streams: List<ApiInstOption> = emptyList(),
    val facilities: List<ApiInstOption> = emptyList(),
    val ownership: List<ApiInstOption> = emptyList(),
    val mediums: List<ApiInstOption> = emptyList(),
    val genderMix: List<ApiInstOption> = emptyList(),
    val affiliations: List<ApiInstOption> = emptyList()
)

/** `details` stays a loose map: the server owns the schema and only sends keys that are filled. */
@Serializable
data class ApiInstPortfolio(
    val details: Map<String, JsonElement> = emptyMap(),
    val completeness: Int = 0,
    val missing: List<String> = emptyList()
)

@Serializable
data class ApiInstPerson(
    val username: String = "",
    val displayName: String = "",
    val role: String = "",
    val photoUrl: String = ""
)

@Serializable
data class ApiInstCounts(val total: Int = 0, val students: Int = 0, val teachers: Int = 0)

@Serializable
data class ApiInstDetail(
    val slug: String = "",
    val name: String = "",
    val kind: String = "school",
    val kindLabel: String = "",
    val district: String = "",
    val place: String = "",
    val location: String = "",
    val website: String = "",
    val phone: String = "",
    val email: String = "",
    val verified: Boolean = false,
    val username: String = "",
    val est: String = "",
    val photoUrl: String = "",
    val counts: ApiInstCounts = ApiInstCounts(),
    val people: List<ApiInstPerson> = emptyList(),
    val portfolio: ApiInstPortfolio = ApiInstPortfolio(),
    val canEdit: Boolean = false,
    val claimable: Boolean = false
)

@Serializable
data class ApiInstApplication(
    val id: Int = 0,
    val status: String = "",
    val name: String = "",
    val note: String = "",
    val institution: String = ""
)

@Serializable
data class ApiMyInstitution(
    val institution: ApiMyInst? = null,
    val application: ApiInstApplication? = null,
    val role: String = "",
    val email: String = ""
)

@Serializable
data class ApiMyInst(
    val slug: String = "",
    val name: String = "",
    val completeness: Int = 0,
    val portfolio: ApiInstPortfolio = ApiInstPortfolio()
)

@Serializable
data class ApiInstSave(
    val status: String = "",
    val portfolio: ApiInstPortfolio = ApiInstPortfolio(),
    val error: String? = null
)

@Serializable
data class ApiInstClaimResult(
    val status: String = "",
    val application: ApiInstApplication? = null,
    val error: String? = null
)
