package com.radiohelper.dosecalc.guide

import retrofit2.http.GET

interface GuideApi {
    @GET("guide.json")
    suspend fun getGuideData(): GuideData
}
