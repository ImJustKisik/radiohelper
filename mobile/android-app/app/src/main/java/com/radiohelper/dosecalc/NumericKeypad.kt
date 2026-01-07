package com.radiohelper.dosecalc

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Backspace
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun NumericKeypad(
    onNumberClick: (String) -> Unit,
    onBackspace: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        // Ряд 1: 7 8 9
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            NumberButton("7", Modifier.weight(1f), onNumberClick)
            NumberButton("8", Modifier.weight(1f), onNumberClick)
            NumberButton("9", Modifier.weight(1f), onNumberClick)
        }

        // Ряд 2: 4 5 6
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            NumberButton("4", Modifier.weight(1f), onNumberClick)
            NumberButton("5", Modifier.weight(1f), onNumberClick)
            NumberButton("6", Modifier.weight(1f), onNumberClick)
        }

        // Ряд 3: 1 2 3
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            NumberButton("1", Modifier.weight(1f), onNumberClick)
            NumberButton("2", Modifier.weight(1f), onNumberClick)
            NumberButton("3", Modifier.weight(1f), onNumberClick)
        }

        // Ряд 4: . 0 ⌫
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            NumberButton(".", Modifier.weight(1f), onNumberClick)
            NumberButton("0", Modifier.weight(1f), onNumberClick)
            Button(
                onClick = onBackspace,
                modifier = Modifier
                    .weight(1f)
                    .aspectRatio(1.5f),
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.errorContainer,
                    contentColor = MaterialTheme.colorScheme.onErrorContainer
                )
            ) {
                Icon(
                    Icons.AutoMirrored.Filled.Backspace,
                    contentDescription = "Удалить"
                )
            }
        }
    }
}

@Composable
private fun NumberButton(
    number: String,
    modifier: Modifier,
    onClick: (String) -> Unit
) {
    Button(
        onClick = { onClick(number) },
        modifier = modifier.aspectRatio(1.5f),
        colors = ButtonDefaults.buttonColors(
            containerColor = MaterialTheme.colorScheme.primaryContainer,
            contentColor = MaterialTheme.colorScheme.onPrimaryContainer
        )
    ) {
        Text(
            text = number,
            fontSize = 24.sp,
            style = MaterialTheme.typography.headlineMedium
        )
    }
}
