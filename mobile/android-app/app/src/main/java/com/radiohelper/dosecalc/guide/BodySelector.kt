package com.radiohelper.dosecalc.guide

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun BodySelector(
    selectedRegion: BodyRegion?,
    onRegionSelected: (BodyRegion?) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier.fillMaxWidth(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            "Выберите область",
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.SemiBold
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // Упрощённая схема человека из кликабельных блоков
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 32.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            // Голова
            BodyPartButton(
                label = "Голова",
                isSelected = selectedRegion == BodyRegion.HEAD,
                onClick = { onRegionSelected(BodyRegion.HEAD) },
                modifier = Modifier.size(width = 100.dp, height = 60.dp),
                shape = CircleShape
            )
            
            // Грудная клетка
            BodyPartButton(
                label = "Грудь",
                isSelected = selectedRegion == BodyRegion.CHEST,
                onClick = { onRegionSelected(BodyRegion.CHEST) },
                modifier = Modifier.size(width = 140.dp, height = 80.dp)
            )
            
            // Живот
            BodyPartButton(
                label = "Живот",
                isSelected = selectedRegion == BodyRegion.ABDOMEN,
                onClick = { onRegionSelected(BodyRegion.ABDOMEN) },
                modifier = Modifier.size(width = 130.dp, height = 70.dp)
            )
            
            // Таз
            BodyPartButton(
                label = "Таз",
                isSelected = selectedRegion == BodyRegion.PELVIS,
                onClick = { onRegionSelected(BodyRegion.PELVIS) },
                modifier = Modifier.size(width = 120.dp, height = 60.dp)
            )
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // Кнопки для других областей
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            RegionChip(
                label = "Позвоночник",
                isSelected = selectedRegion == BodyRegion.SPINE,
                onClick = { onRegionSelected(BodyRegion.SPINE) }
            )
            RegionChip(
                label = "Конечности",
                isSelected = selectedRegion == BodyRegion.LIMBS,
                onClick = { onRegionSelected(BodyRegion.LIMBS) }
            )
        }
    }
}

@Composable
private fun BodyPartButton(
    label: String,
    isSelected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    shape: androidx.compose.ui.graphics.Shape = RoundedCornerShape(12.dp)
) {
    val backgroundColor = if (isSelected) 
        MaterialTheme.colorScheme.primaryContainer 
    else 
        MaterialTheme.colorScheme.surfaceVariant
    
    val borderColor = if (isSelected)
        MaterialTheme.colorScheme.primary
    else
        Color.Transparent
    
    Box(
        modifier = modifier
            .clip(shape)
            .background(backgroundColor)
            .border(
                width = if (isSelected) 3.dp else 0.dp,
                color = borderColor,
                shape = shape
            )
            .clickable(onClick = onClick),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.bodyMedium,
            fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal,
            color = if (isSelected) 
                MaterialTheme.colorScheme.onPrimaryContainer 
            else 
                MaterialTheme.colorScheme.onSurfaceVariant,
            textAlign = TextAlign.Center
        )
    }
}

@Composable
private fun RegionChip(
    label: String,
    isSelected: Boolean,
    onClick: () -> Unit
) {
    androidx.compose.material3.FilterChip(
        selected = isSelected,
        onClick = onClick,
        label = { Text(label) }
    )
}
