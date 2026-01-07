package com.radiohelper.dosecalc.guide

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun GuideListScreen(
    viewModel: GuideViewModel,
    onProtocolClick: (String) -> Unit
) {
    val state by viewModel.state.collectAsState()
    val selectedRegion by viewModel.selectedRegion.collectAsState()
    val searchQuery by viewModel.searchQuery.collectAsState()
    val selectedProtocolType by viewModel.selectedProtocolType.collectAsState()
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Справочник укладок") },
                actions = {
                    if (selectedRegion != null) {
                        IconButton(onClick = { viewModel.loadData(forceRefresh = true) }) {
                            Icon(Icons.Default.Refresh, contentDescription = "Обновить")
                        }
                    }
                }
            )
        }
    ) { padding ->
        // Если регион не выбран - показываем только селектор
        if (selectedRegion == null) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding),
                contentAlignment = Alignment.Center
            ) {
                BodySelector(
                    selectedRegion = selectedRegion,
                    onRegionSelected = viewModel::onRegionSelected
                )
            }
        } else {
            // Если регион выбран - показываем список
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
            ) {
                // Показываем выбранный регион и кнопку "Изменить"
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 8.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "Область: ${selectedRegion?.label ?: "Все"}",
                        style = MaterialTheme.typography.bodyLarge,
                        fontWeight = FontWeight.SemiBold
                    )
                    TextButton(onClick = { viewModel.onRegionSelected(null) }) {
                        Text("Изменить")
                    }
                }
                
                Divider()
                
                // Фильтр по типу исследования
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 8.dp, vertical = 8.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    FilterChip(
                        selected = selectedProtocolType == null,
                        onClick = { viewModel.onProtocolTypeSelected(null) },
                        label = { Text("Все") }
                    )
                    FilterChip(
                        selected = selectedProtocolType == ProtocolType.RENTGEN,
                        onClick = { viewModel.onProtocolTypeSelected(ProtocolType.RENTGEN) },
                        label = { Text("📷 Рентген") }
                    )
                    FilterChip(
                        selected = selectedProtocolType == ProtocolType.CT,
                        onClick = { viewModel.onProtocolTypeSelected(ProtocolType.CT) },
                        label = { Text("🔲 КТ") }
                    )
                }
                
                Divider()
                
                // Поиск
                OutlinedTextField(
                    value = searchQuery,
                    onValueChange = viewModel::onSearchQueryChanged,
                    label = { Text("Поиск") },
                    leadingIcon = { Icon(Icons.Default.Search, null) },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 8.dp),
                    singleLine = true
                )
                
                // Список протоколов
                when (val currentState = state) {
                is GuideUiState.Loading -> {
                    Box(
                        modifier = Modifier.fillMaxSize(),
                        contentAlignment = Alignment.Center
                    ) {
                        CircularProgressIndicator()
                    }
                }
                
                is GuideUiState.Error -> {
                    Box(
                        modifier = Modifier.fillMaxSize(),
                        contentAlignment = Alignment.Center
                    ) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text(currentState.message)
                            Spacer(modifier = Modifier.height(8.dp))
                            Button(onClick = { viewModel.loadData(forceRefresh = true) }) {
                                Text("Повторить")
                            }
                        }
                    }
                }
                
                is GuideUiState.Success -> {
                    if (currentState.protocols.isEmpty()) {
                        Box(
                            modifier = Modifier.fillMaxSize(),
                            contentAlignment = Alignment.Center
                        ) {
                            Text("Протоколы не найдены")
                        }
                    } else {
                        LazyColumn(
                            modifier = Modifier.fillMaxSize(),
                            contentPadding = PaddingValues(16.dp),
                            verticalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            items(currentState.protocols) { protocol ->
                                ProtocolCard(
                                    protocol = protocol,
                                    onClick = { onProtocolClick(protocol.id) }
                                )
                            }
                        }
                    }
                }
            }
            }
        }
    }
}

@Composable
private fun ProtocolCard(
    protocol: Protocol,
    onClick: () -> Unit
) {
    ElevatedCard(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Иконка типа + название
                Row(
                    modifier = Modifier.weight(1f),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Text(
                        text = if (protocol.type == ProtocolType.RENTGEN) "📷" else "🔲",
                        style = MaterialTheme.typography.titleMedium
                    )
                    Text(
                        protocol.title,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold
                    )
                }
                
                FilterChip(
                    selected = false,
                    onClick = {},
                    label = { Text(protocol.type.label) },
                    enabled = false
                )
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Row(
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Text(
                    "kV: ${protocol.kv}",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    "mAs: ${protocol.mas}",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            
            if (protocol.description.length > 100) {
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    protocol.description.take(100) + "...",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}
