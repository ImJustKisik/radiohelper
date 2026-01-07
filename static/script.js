// Глобальное состояние
let apiKey = localStorage.getItem('openrouter_api_key') || '';
let lastDoseValue = null;
let lastDoseText = null;

// История для Undo/Redo
let history = [];
let historyIndex = -1;
const MAX_HISTORY = 50;

// Элементы DOM
const settingsBtn = document.getElementById('settingsBtn');
const settingsModal = document.getElementById('settingsModal');
const closeModal = document.querySelector('.close');
const saveApiKeyBtn = document.getElementById('saveApiKey');
const apiKeyInput = document.getElementById('apiKey');
const pasteBtn = document.getElementById('pasteBtn');

const undoBtn = document.getElementById('undoBtn');
const redoBtn = document.getElementById('redoBtn');

const complaintsTextarea = document.getElementById('complaints');
const clearComplaintsBtn = document.getElementById('clearComplaints');
const improveBtn = document.getElementById('improveBtn');
const noComplaintsBtn = document.getElementById('noComplaintsBtn');

const traumaSelect = document.getElementById('trauma');
const operationsSelect = document.getElementById('operations');
const operationsDetailBlock = document.getElementById('operationsDetailBlock');
const operationsDetailInput = document.getElementById('operationsDetail');
const contrastSelect = document.getElementById('contrast');
const pregnancySelect = document.getElementById('pregnancy');
const extraInput = document.getElementById('extra');

const prepInput = document.getElementById('prep');
const toggleReferrerBtn = document.getElementById('toggleReferrerBtn');
const referrerBlock = document.getElementById('referrerBlock');
const referrerInput = document.getElementById('referrer');

const dlpInput = document.getElementById('dlp');
const dlpRegionSelect = document.getElementById('dlpRegion');
const dlpAgeSelect = document.getElementById('dlpAge');
const calculateDoseBtn = document.getElementById('calculateDoseBtn');
const doseResultP = document.getElementById('doseResult');

const generateBtn = document.getElementById('generateBtn');
const resultTextarea = document.getElementById('result');
const copyBtn = document.getElementById('copyBtn');
const clearBtn = document.getElementById('clearBtn');

const statusBar = document.getElementById('statusBar');

// Инициализация
if (apiKey) {
    apiKeyInput.value = apiKey;
}

// Сохранение начального состояния
saveState();

// История операций - функции
function getFormState() {
    return {
        complaints: complaintsTextarea.value,
        trauma: traumaSelect.value,
        operations: operationsSelect.value,
        operationsDetail: operationsDetailInput.value,
        operationsDetailVisible: operationsDetailBlock.style.display !== 'none',
        contrast: contrastSelect.value,
        pregnancy: pregnancySelect.value,
        extra: extraInput.value,
        prep: prepInput.value,
        referrer: referrerInput.value,
        referrerVisible: referrerBlock.style.display !== 'none',
        dlp: dlpInput.value,
        dlpRegion: dlpRegionSelect.value,
        dlpAge: dlpAgeSelect.value,
        doseResult: doseResultP.textContent,
        doseResultClass: doseResultP.className,
        lastDoseValue: lastDoseValue,
        lastDoseText: lastDoseText
    };
}

function restoreFormState(state) {
    complaintsTextarea.value = state.complaints || '';
    traumaSelect.value = state.trauma || 'Нет';
    operationsSelect.value = state.operations || 'Нет';
    operationsDetailInput.value = state.operationsDetail || '';
    operationsDetailBlock.style.display = state.operationsDetailVisible ? 'block' : 'none';
    contrastSelect.value = state.contrast || 'Нет';
    pregnancySelect.value = state.pregnancy || 'Не актуально';
    extraInput.value = state.extra || '';
    prepInput.value = state.prep || '';
    referrerInput.value = state.referrer || '';
    referrerBlock.style.display = state.referrerVisible ? 'block' : 'none';
    toggleReferrerBtn.textContent = state.referrerVisible ? 
        'Скрыть комментарий направления' : 'Показать комментарий направления';
    referrerVisible = state.referrerVisible || false;
    dlpInput.value = state.dlp || '';
    dlpRegionSelect.value = state.dlpRegion || 'Голова';
    dlpAgeSelect.value = state.dlpAge || '>15 лет';
    doseResultP.textContent = state.doseResult || '';
    doseResultP.className = state.doseResultClass || 'dose-result';
    lastDoseValue = state.lastDoseValue;
    lastDoseText = state.lastDoseText;
}

function saveState() {
    const state = getFormState();
    
    // Удаляем все состояния после текущего индекса
    if (historyIndex < history.length - 1) {
        history = history.slice(0, historyIndex + 1);
    }
    
    // Добавляем новое состояние
    history.push(state);
    
    // Ограничиваем размер истории
    if (history.length > MAX_HISTORY) {
        history.shift();
    } else {
        historyIndex++;
    }
    
    updateHistoryButtons();
}

function undo() {
    if (historyIndex > 0) {
        historyIndex--;
        restoreFormState(history[historyIndex]);
        updateHistoryButtons();
        showStatus('Действие отменено');
    }
}

function redo() {
    if (historyIndex < history.length - 1) {
        historyIndex++;
        restoreFormState(history[historyIndex]);
        updateHistoryButtons();
        showStatus('Действие повторено');
    }
}

function updateHistoryButtons() {
    undoBtn.disabled = historyIndex <= 0;
    redoBtn.disabled = historyIndex >= history.length - 1;
}

// Обработчики для Undo/Redo
undoBtn.addEventListener('click', undo);
redoBtn.addEventListener('click', redo);

// Отслеживание изменений для истории (debounced)
let saveStateTimeout;
function debounceSaveState() {
    clearTimeout(saveStateTimeout);
    saveStateTimeout = setTimeout(saveState, 500);
}

complaintsTextarea.addEventListener('input', debounceSaveState);
traumaSelect.addEventListener('change', saveState);
operationsSelect.addEventListener('change', saveState);
operationsDetailInput.addEventListener('input', debounceSaveState);
contrastSelect.addEventListener('change', saveState);
pregnancySelect.addEventListener('change', saveState);
extraInput.addEventListener('input', debounceSaveState);
prepInput.addEventListener('input', debounceSaveState);
referrerInput.addEventListener('input', debounceSaveState);
dlpInput.addEventListener('input', debounceSaveState);
dlpRegionSelect.addEventListener('change', saveState);
dlpAgeSelect.addEventListener('change', saveState);

// Модальное окно настроек
settingsBtn.addEventListener('click', () => {
    settingsModal.style.display = 'block';
});

closeModal.addEventListener('click', () => {
    settingsModal.style.display = 'none';
});

window.addEventListener('click', (e) => {
    if (e.target === settingsModal) {
        settingsModal.style.display = 'none';
    }
});

saveApiKeyBtn.addEventListener('click', () => {
    const key = apiKeyInput.value.trim();
    if (key) {
        apiKey = key;
        localStorage.setItem('openrouter_api_key', key);
        showStatus('Ключ сохранён', 'success');
    } else {
        apiKey = '';
        localStorage.removeItem('openrouter_api_key');
        showStatus('Ключ очищен');
    }
    settingsModal.style.display = 'none';
});

pasteBtn.addEventListener('click', async () => {
    try {
        const text = await navigator.clipboard.readText();
        apiKeyInput.value = text;
    } catch (err) {
        showStatus('Не удалось вставить из буфера', 'error');
    }
});

// Жалобы
clearComplaintsBtn.addEventListener('click', () => {
    complaintsTextarea.value = '';
    complaintsTextarea.focus();
    showStatus('Жалобы очищены');
});

noComplaintsBtn.addEventListener('click', () => {
    complaintsTextarea.value = 'не предъявляет';
    showStatus('Жалобы: не предъявляет', 'success');
    saveState(); // Сохраняем состояние
});

improveBtn.addEventListener('click', async () => {
    const text = complaintsTextarea.value.trim();
    if (!text) {
        showStatus('Заполните жалобы перед улучшением', 'error');
        return;
    }

    if (!apiKey) {
        showStatus('Укажите ключ в настройках', 'error');
        return;
    }

    improveBtn.disabled = true;
    improveBtn.textContent = 'Обработка...';
    showStatus('AI обрабатывает жалобы...');

    try {
        const response = await fetch('/api/improve-complaints', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                api_key: apiKey
            })
        });

        const data = await response.json();

        if (response.ok) {
            complaintsTextarea.value = data.improved_text;
            showStatus('Жалобы улучшены', 'success');
            saveState(); // Сохраняем состояние после улучшения
        } else {
            showStatus(data.error || 'Ошибка AI', 'error');
        }
    } catch (err) {
        showStatus('Ошибка соединения с сервером', 'error');
    } finally {
        improveBtn.disabled = false;
        improveBtn.textContent = '✨ Улучшить (AI)';
    }
});

// Операции - показать/скрыть детали
operationsSelect.addEventListener('change', () => {
    if (operationsSelect.value !== 'Нет') {
        operationsDetailBlock.style.display = 'block';
        operationsDetailInput.focus();
    } else {
        operationsDetailBlock.style.display = 'none';
        operationsDetailInput.value = '';
    }
});

// Показать/скрыть комментарий направления
let referrerVisible = false;
toggleReferrerBtn.addEventListener('click', () => {
    referrerVisible = !referrerVisible;
    if (referrerVisible) {
        referrerBlock.style.display = 'block';
        toggleReferrerBtn.textContent = 'Скрыть комментарий направления';
        referrerInput.focus();
    } else {
        referrerBlock.style.display = 'none';
        toggleReferrerBtn.textContent = 'Показать комментарий направления';
        referrerInput.value = '';
    }
});

// Расчёт дозы
calculateDoseBtn.addEventListener('click', calculateDose);
dlpInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        calculateDose();
    }
});

async function calculateDose() {
    const dlpValue = dlpInput.value.trim().replace(',', '.');
    const region = dlpRegionSelect.value;
    const age = dlpAgeSelect.value;

    if (!dlpValue) {
        doseResultP.textContent = 'Введите DLP';
        doseResultP.className = 'dose-result error';
        showStatus('Поле DLP пустое', 'error');
        return;
    }

    try {
        const response = await fetch('/api/calculate-dose', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                dlp: parseFloat(dlpValue),
                region: region,
                age: age
            })
        });

        const data = await response.json();

        if (response.ok) {
            lastDoseValue = data.dose_msv;
            lastDoseText = data.dose_text;
            doseResultP.textContent = data.dose_text;
            doseResultP.className = 'dose-result';
            showStatus('Доза рассчитана', 'success');
            saveState(); // Сохраняем состояние после расчета
        } else {
            doseResultP.textContent = data.error;
            doseResultP.className = 'dose-result error';
            lastDoseValue = null;
            lastDoseText = null;
            showStatus(data.error, 'error');
        }
    } catch (err) {
        doseResultP.textContent = 'Ошибка соединения';
        doseResultP.className = 'dose-result error';
        showStatus('Ошибка соединения с сервером', 'error');
    }
}

// Формирование текста
generateBtn.addEventListener('click', () => {
    const complaints = complaintsTextarea.value.trim() || 'Отрицает';
    const trauma = traumaSelect.value === 'Нет' ? 'Отрицает' : traumaSelect.value;
    const operations = operationsSelect.value;
    const operationsDetail = operationsDetailInput.value.trim();
    const contrast = contrastSelect.value;
    const pregnancy = pregnancySelect.value;
    const prep = prepInput.value.trim();
    const referrer = referrerInput.value.trim();
    const extra = extraInput.value.trim();

    let operationsText = operations === 'Нет' ? 'Отрицает' : operations;
    if (operations !== 'Нет') {
        if (operationsDetail) {
            operationsText = `${operations} (${operationsDetail})`;
        } else {
            operationsText = `${operations} (уточнить)`;
        }
    }

    const lines = [];
    lines.push(`Жалобы: ${complaints}`);
    lines.push(`Травмы: ${trauma}`);
    lines.push(`Операции/импланты: ${operationsText}`);
    lines.push(`Аллергия на контраст: ${contrast}`);

    if (pregnancy && pregnancy !== 'Не актуально') {
        lines.push(`Беременность: ${pregnancy}`);
    }

    if (prep) {
        lines.push(`Подготовка/диета: ${prep}`);
    }

    if (referrer) {
        lines.push(`Комментарий направления: ${referrer}`);
    }

    if (extra) {
        lines.push(`Особенности: ${extra}`);
    }

    if (lastDoseValue !== null && lastDoseText) {
        lines.push(lastDoseText);
    }

    const finalText = lines.join('\n');
    resultTextarea.value = finalText;
    showStatus('Текст сформирован', 'success');
});

// Копирование в буфер
copyBtn.addEventListener('click', async () => {
    const text = resultTextarea.value.trim();
    if (!text) {
        showStatus('Нет текста для копирования', 'error');
        return;
    }

    try {
        await navigator.clipboard.writeText(text);
        showStatus('Скопировано в буфер обмена!', 'success');
    } catch (err) {
        // Fallback для старых браузеров
        resultTextarea.select();
        document.execCommand('copy');
        showStatus('Скопировано в буфер обмена!', 'success');
    }
});

// Очистка полей
clearBtn.addEventListener('click', () => {
    complaintsTextarea.value = '';
    traumaSelect.value = 'Нет';
    operationsSelect.value = 'Нет';
    operationsDetailBlock.style.display = 'none';
    operationsDetailInput.value = '';
    contrastSelect.value = 'Нет';
    pregnancySelect.value = 'Не актуально';
    prepInput.value = '';
    referrerInput.value = '';
    extraInput.value = '';
    dlpInput.value = '';
    dlpRegionSelect.value = 'Голова';
    dlpAgeSelect.value = '>15 лет';
    doseResultP.textContent = '';
    doseResultP.className = 'dose-result';
    lastDoseValue = null;
    lastDoseText = null;
    resultTextarea.value = '';
    
    if (referrerVisible) {
        referrerBlock.style.display = 'none';
        referrerVisible = false;
        toggleReferrerBtn.textContent = 'Показать комментарий направления';
    }
    
    complaintsTextarea.focus();
    showStatus('Поля очищены');
    
    // Сохраняем состояние после очистки
    saveState();
});

// Горячие клавиши
document.addEventListener('keydown', (e) => {
    // Ctrl+Z - Undo
    if (e.ctrlKey && e.key === 'z' && !e.shiftKey) {
        undo();
        e.preventDefault();
    }
    // Ctrl+Y или Ctrl+Shift+Z - Redo
    if ((e.ctrlKey && e.key === 'y') || (e.ctrlKey && e.shiftKey && e.key === 'z')) {
        redo();
        e.preventDefault();
    }
    // Ctrl+Enter - сформировать текст
    if (e.ctrlKey && e.key === 'Enter') {
        generateBtn.click();
        e.preventDefault();
    }
    // Esc - очистить
    if (e.key === 'Escape') {
        clearBtn.click();
        e.preventDefault();
    }
});

// Функция показа статуса
function showStatus(message, type = 'info') {
    statusBar.textContent = message;
    statusBar.className = 'status-bar show';
    
    if (type === 'success') {
        statusBar.classList.add('success');
    } else if (type === 'error') {
        statusBar.classList.add('error');
    }
    
    setTimeout(() => {
        statusBar.className = 'status-bar';
    }, 2500);
}
