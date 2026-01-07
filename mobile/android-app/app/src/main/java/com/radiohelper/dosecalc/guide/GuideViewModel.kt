package com.radiohelper.dosecalc.guide

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

sealed class GuideUiState {
    object Loading : GuideUiState()
    data class Success(val protocols: List<Protocol>) : GuideUiState()
    data class Error(val message: String) : GuideUiState()
}

class GuideViewModel(private val repository: GuideRepository) : ViewModel() {
    private val _state = MutableStateFlow<GuideUiState>(GuideUiState.Loading)
    val state: StateFlow<GuideUiState> = _state
    
    private val _selectedRegion = MutableStateFlow<BodyRegion?>(null)
    val selectedRegion: StateFlow<BodyRegion?> = _selectedRegion
    
    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery
    
    private val _selectedProtocolType = MutableStateFlow<ProtocolType?>(null)
    val selectedProtocolType: StateFlow<ProtocolType?> = _selectedProtocolType
    
    private var allProtocols: List<Protocol> = emptyList()
    
    init {
        loadData()
    }
    
    fun loadData(forceRefresh: Boolean = false) {
        viewModelScope.launch {
            _state.value = GuideUiState.Loading
            repository.getGuideData(forceRefresh).fold(
                onSuccess = { data ->
                    allProtocols = data.protocols
                    updateFilteredProtocols()
                },
                onFailure = { error ->
                    _state.value = GuideUiState.Error(
                        error.message ?: "Не удалось загрузить данные"
                    )
                }
            )
        }
    }
    
    fun onRegionSelected(region: BodyRegion?) {
        _selectedRegion.value = region
        updateFilteredProtocols()
    }
    
    fun onSearchQueryChanged(query: String) {
        _searchQuery.value = query
        updateFilteredProtocols()
    }
    
    fun onProtocolTypeSelected(type: ProtocolType?) {
        _selectedProtocolType.value = type
        updateFilteredProtocols()
    }
    
    private fun updateFilteredProtocols() {
        val filtered = allProtocols
            .filter { protocol ->
                val matchesRegion = _selectedRegion.value == null || 
                                   _selectedRegion.value == BodyRegion.ALL ||
                                   protocol.region == _selectedRegion.value
                
                val matchesSearch = _searchQuery.value.isBlank() ||
                                   protocol.title.contains(_searchQuery.value, ignoreCase = true) ||
                                   protocol.description.contains(_searchQuery.value, ignoreCase = true)
                
                val matchesType = _selectedProtocolType.value == null ||
                                 protocol.type == _selectedProtocolType.value
                
                matchesRegion && matchesSearch && matchesType
            }
        
        _state.value = GuideUiState.Success(filtered)
    }
}
