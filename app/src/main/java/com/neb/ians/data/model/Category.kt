package com.neb.ians.data.model

data class Category(
    val id: String,
    val label: String,
    val group: CategoryGroup
)

enum class CategoryGroup {
    SUBJECT, GRADE, TYPE
}
