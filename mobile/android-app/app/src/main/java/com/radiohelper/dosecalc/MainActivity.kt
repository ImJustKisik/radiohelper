package com.radiohelper.dosecalc

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.relocation.BringIntoViewRequester
import androidx.compose.foundation.relocation.bringIntoViewRequester
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Calculate
import androidx.compose.material.icons.filled.ContentCopy
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.MenuBook
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.radiohelper.dosecalc.guide.*
import kotlinx.coroutines.launch

sealed class Screen(val route: String, val title: String, val icon: androidx.compose.ui.graphics.vector.ImageVector) {
    object Dose : Screen("dose", "Калькулятор", Icons.Default.Calculate)
    object Guide : Screen("guide", "Справочник", Icons.Default.MenuBook)
}

class MainActivity : ComponentActivity() {
    private val vm: DoseViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                MainScreen(vm)
            }
        }
    }
}

@Composable
fun MainScreen(doseVm: DoseViewModel) {
    val navController = rememberNavController()
    val context = LocalContext.current
    val guideVm: GuideViewModel = remember {
        GuideViewModel(GuideRepository(context))
    }
    
    Scaffold(
        bottomBar = { BottomNavigationBar(navController) }
    ) { padding ->
        NavHost(
            navController = navController,
            startDestination = Screen.Dose.route,
            modifier = Modifier.padding(padding)
        ) {
            composable(Screen.Dose.route) {
                DoseScreen(doseVm)
            }
            
            composable(Screen.Guide.route) {
                GuideListScreen(
                    viewModel = guideVm,
                    onProtocolClick = { protocolId ->
                        navController.navigate("protocol_detail/$protocolId")
                    }
                )
            }
            
            composable("protocol_detail/{protocolId}") { backStackEntry ->
                val protocolId = backStackEntry.arguments?.getString("protocolId")
                val state by guideVm.state.collectAsState()
                
                if (state is GuideUiState.Success && protocolId != null) {
                    val protocol = (state as GuideUiState.Success).protocols
                        .find { it.id == protocolId }
                    
                    protocol?.let {
                        ProtocolDetailScreen(
                            protocol = it,
                            onBack = { navController.popBackStack() }
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun BottomNavigationBar(navController: NavHostController) {
    val screens = listOf(Screen.Dose, Screen.Guide)
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route
    
    NavigationBar {
        screens.forEach { screen ->
            NavigationBarItem(
                icon = { Icon(screen.icon, contentDescription = screen.title) },
                label = { Text(screen.title) },
                selected = currentRoute == screen.route,
                onClick = {
                    navController.navigate(screen.route) {
                        popUpTo(navController.graph.startDestinationId) {
                            saveState = true
                        }
                        launchSingleTop = true
                        restoreState = true
                    }
                }
            )
        }
    }
}

@OptIn(ExperimentalFoundationApi::class)
@Composable
fun DoseScreen(vm: DoseViewModel = viewModel()) {
    val state by vm.state.collectAsState()
    val context = LocalContext.current
    val scrollState = rememberScrollState()
    val resultRequester = remember { BringIntoViewRequester() }
    val scope = rememberCoroutineScope()
    val isDlpValid = state.dlp.toDoubleOrNull()?.let { it > 0 } == true

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(scrollState)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Заголовок с кнопкой очистки
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    "Расчёт дозы облучения",
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.Bold
                )
                IconButton(onClick = vm::onClear) {
                    Icon(
                        Icons.Default.Delete,
                        contentDescription = "Очистить",
                        tint = MaterialTheme.colorScheme.error
                    )
                }
            }

            // Карточка ввода DLP
            ElevatedCard(
                modifier = Modifier.fillMaxWidth(),
                elevation = CardDefaults.elevatedCardElevation(defaultElevation = 2.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        "Введите DLP",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                    
                    OutlinedTextField(
                        value = state.dlp,
                        onValueChange = {},
                        label = { Text("DLP (мГр·см)") },
                        readOnly = true,
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth(),
                        textStyle = MaterialTheme.typography.headlineMedium.copy(
                            textAlign = TextAlign.Center
                        )
                    )
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    // Числовая клавиатура
                    NumericKeypad(
                        onNumberClick = vm::onNumberClick,
                        onBackspace = vm::onBackspace
                    )
                }
            }

            FilledTonalButton(
                onClick = {
                    vm.calculate()
                    scope.launch {
                        val result = vm.state.value.result
                        if (result.isNotEmpty()) {
                            resultRequester.bringIntoView()
                        }
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                enabled = isDlpValid
            ) {
                Icon(Icons.Default.Calculate, contentDescription = null)
                Spacer(modifier = Modifier.padding(4.dp))
                Text("Рассчитать эффективную дозу", style = MaterialTheme.typography.titleMedium)
            }

            // Карточка параметров
            ElevatedCard(
                modifier = Modifier.fillMaxWidth(),
                elevation = CardDefaults.elevatedCardElevation(defaultElevation = 2.dp)
            ) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    Text(
                        "Параметры",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold
                    )

                    DropdownField(
                        label = "Область исследования",
                        items = Region.entries.map { it.label },
                        selectedItem = state.region.label,
                        onItemSelected = { label ->
                            Region.entries.find { it.label == label }?.let { vm.onRegionChange(it) }
                        }
                    )

                    DropdownField(
                        label = "Возрастная группа",
                        items = AgeGroup.entries.map { it.label },
                        selectedItem = state.age.label,
                        onItemSelected = { label ->
                            AgeGroup.entries.find { it.label == label }?.let { vm.onAgeChange(it) }
                        }
                    )
                }
            }

            // Карточка результата
            if (state.result.isNotEmpty()) {
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .bringIntoViewRequester(resultRequester),
                    colors = CardDefaults.cardColors(
                        containerColor = if (state.isError) 
                            MaterialTheme.colorScheme.errorContainer 
                        else 
                            MaterialTheme.colorScheme.primaryContainer
                    )
                ) {
                    Column(
                        modifier = Modifier.padding(16.dp)
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                "Результат",
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.SemiBold,
                                color = if (state.isError) 
                                    MaterialTheme.colorScheme.onErrorContainer 
                                else 
                                    MaterialTheme.colorScheme.onPrimaryContainer
                            )
                            
                            if (!state.isError) {
                                IconButton(
                                    onClick = {
                                        val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                                        val clip = ClipData.newPlainText("Доза", state.result)
                                        clipboard.setPrimaryClip(clip)
                                        Toast.makeText(context, "Скопировано в буфер обмена", Toast.LENGTH_SHORT).show()
                                    }
                                ) {
                                    Icon(
                                        Icons.Default.ContentCopy,
                                        contentDescription = "Копировать",
                                        tint = MaterialTheme.colorScheme.onPrimaryContainer
                                    )
                                }
                            }
                        }
                        
                        Spacer(modifier = Modifier.height(8.dp))
                        
                        Text(
                            state.result,
                            style = MaterialTheme.typography.bodyLarge,
                            color = if (state.isError) 
                                MaterialTheme.colorScheme.onErrorContainer 
                            else 
                                MaterialTheme.colorScheme.onPrimaryContainer
                        )
                    }
                }
            }
        }
    }
}
