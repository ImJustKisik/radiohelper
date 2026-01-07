package com.radiohelper.dosecalc.guide

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProtocolDetailScreen(
    protocol: Protocol,
    onBack: () -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Детали протокола") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, "Назад")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Заголовок
            Text(
                protocol.title,
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold
            )
            
            // Тип и область
            Row(
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                AssistChip(
                    onClick = {},
                    label = { Text(protocol.type.label) }
                )
                AssistChip(
                    onClick = {},
                    label = { Text(protocol.region.label) }
                )
            }
            
            // Картинка укладки
            protocol.imageUrl?.let { url ->
                ElevatedCard(
                    modifier = Modifier.fillMaxWidth()
                ) {
                    AsyncImage(
                        model = url,
                        contentDescription = "Схема укладки",
                        modifier = Modifier
                            .fillMaxWidth()
                            .heightIn(max = 300.dp),
                        contentScale = ContentScale.Fit
                    )
                }
            }
            
            // Технические параметры
            ElevatedCard(
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Text(
                        "Технические параметры",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold
                    )
                    
                    Divider()
                    
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text("Напряжение (kV):", fontWeight = FontWeight.Medium)
                        Text(protocol.kv)
                    }
                    
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text("Экспозиция (mAs):", fontWeight = FontWeight.Medium)
                        Text(protocol.mas)
                    }
                }
            }
            
            // Описание укладки
            ElevatedCard(
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Text(
                        "Описание укладки",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold
                    )
                    
                    Divider()
                    
                    Text(
                        protocol.description,
                        style = MaterialTheme.typography.bodyMedium
                    )
                }
            }
        }
    }
}
