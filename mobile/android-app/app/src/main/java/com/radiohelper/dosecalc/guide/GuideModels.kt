package com.radiohelper.dosecalc.guide

enum class BodyRegion(val label: String) {
    HEAD("Голова"),
    CHEST("Грудная клетка"),
    SPINE("Позвоночник"),
    ABDOMEN("Живот"),
    PELVIS("Таз"),
    LIMBS("Конечности"),
    ALL("Все")
}

enum class ProtocolType(val label: String) {
    RENTGEN("Рентген"),
    CT("КТ")
}

data class Protocol(
    val id: String,
    val title: String,
    val type: ProtocolType,
    val region: BodyRegion,
    val kv: String,
    val mas: String,
    val description: String,
    val imageUrl: String? = null
)

data class GuideData(
    val version: Int,
    val protocols: List<Protocol>
)
