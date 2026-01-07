package com.radiohelper.dosecalc.guide

import android.content.Context
import com.google.gson.Gson
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.io.File

class GuideRepository(private val context: Context) {
    private val gson = Gson()
    private val cacheFile = File(context.filesDir, "guide_cache.json")
    
    // GitHub raw URL для guide.json из radiohelper репозитория
    private val baseUrl = "https://raw.githubusercontent.com/ImJustKisik/radiohelper/main/"
    
    private val api: GuideApi by lazy {
        Retrofit.Builder()
            .baseUrl(baseUrl)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(GuideApi::class.java)
    }
    
    private fun loadBundledData(): GuideData {
        val inputStream = context.resources.openRawResource(
            context.resources.getIdentifier("guide", "raw", context.packageName)
        )
        return gson.fromJson(inputStream.reader(), GuideData::class.java)
    }
    
    suspend fun getGuideData(forceRefresh: Boolean = false): Result<GuideData> = withContext(Dispatchers.IO) {
        try {
            // Сначала проверяем кэш
            if (!forceRefresh && cacheFile.exists()) {
                val cachedData = gson.fromJson(cacheFile.readText(), GuideData::class.java)
                return@withContext Result.success(cachedData)
            }
            
            // Если кэша нет или требуется обновление, загружаем из bundled ресурсов
            if (!cacheFile.exists()) {
                val bundledData = loadBundledData()
                cacheFile.writeText(gson.toJson(bundledData))
                return@withContext Result.success(bundledData)
            }
            
            // Пытаемся обновить из сети (в фоновом режиме, не блокируя UI)
            if (forceRefresh) {
                try {
                    val freshData = api.getGuideData()
                    cacheFile.writeText(gson.toJson(freshData))
                    return@withContext Result.success(freshData)
                } catch (networkException: Exception) {
                    // Если сеть не работает, возвращаем кэш
                    val cachedData = gson.fromJson(cacheFile.readText(), GuideData::class.java)
                    return@withContext Result.success(cachedData)
                }
            }
            
            // Возвращаем кэш по умолчанию
            val cachedData = gson.fromJson(cacheFile.readText(), GuideData::class.java)
            return@withContext Result.success(cachedData)
        } catch (e: Exception) {
            // Последняя попытка — загрузить bundled данные
            try {
                val bundledData = loadBundledData()
                return@withContext Result.success(bundledData)
            } catch (bundledException: Exception) {
                return@withContext Result.failure(e)
            }
        }
    }
}
