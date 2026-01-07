package com.radiohelper.dosecalc

import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.update
import kotlin.math.round

data class DoseUiState(
    val dlp: String = "",
    val region: Region = Region.HEAD,
    val age: AgeGroup = AgeGroup.GT_15,
    val result: String = "",
    val isError: Boolean = false
)

class DoseViewModel : ViewModel() {
    private val _state = MutableStateFlow(DoseUiState())
    val state: StateFlow<DoseUiState> = _state

    fun onDlpChange(newValue: String) {
        // Фильтруем ввод: только цифры и одна точка
        val filtered = newValue.filter { it.isDigit() || it == '.' }
        val dotCount = filtered.count { it == '.' }
        if (dotCount <= 1) {
            _state.update { it.copy(dlp = filtered) }
        }
    }
    
    fun onNumberClick(number: String) {
        val current = _state.value.dlp
        // Не добавляем вторую точку
        if (number == "." && current.contains(".")) return
        _state.update { it.copy(dlp = current + number) }
    }
    
    fun onBackspace() {
        val current = _state.value.dlp
        if (current.isNotEmpty()) {
            _state.update { it.copy(dlp = current.dropLast(1)) }
        }
    }
    
    fun onClear() {
        _state.update { DoseUiState() }
    }
    
    fun onRegionChange(region: Region) = _state.update { it.copy(region = region) }
    fun onAgeChange(age: AgeGroup) = _state.update { it.copy(age = age) }

    fun calculate() {
        val raw = _state.value.dlp.trim().replace(',', '.')
        val dlp = raw.toDoubleOrNull()
        if (dlp == null || dlp <= 0) {
            _state.update { it.copy(result = "Некорректный DLP", isError = true) }
            return
        }
        val k = DoseCoefficients.values[_state.value.region]?.get(_state.value.age)
        if (k == null) {
            _state.update { it.copy(result = "Нет коэффициента", isError = true) }
            return
        }
        val dose = dlp * k
        val text = "Эффективная доза: %.2f мЗв (DLP=%.0f, k=%.5f)"
            .format(dose, round(dlp), k)
        _state.update { it.copy(result = text, isError = false) }
    }
}
