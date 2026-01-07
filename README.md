# Помощник Рентгенлаборанта (Веб-версия)

Веб-приложение для быстрого сбора анамнеза и формирования текста для вставки в электронную карту.

## Возможности

- **Анамнез**: жалобы, травмы, операции/импланты, аллергии, беременность
- **AI улучшение**: автоматическое улучшение текста жалоб через OpenRouter API
- **История операций**: отмена (Undo) и повтор (Redo) действий с автосохранением состояния формы
- **Расчёт дозы**: расчёт эффективной дозы облучения по DLP
- **Подготовка**: поля для подготовки/диеты и комментария врача-направителя
- **Горячие клавиши**: 
  - `Ctrl+Enter` — сформировать текст
  - `Esc` — очистить все поля
  - `Ctrl+Z` — отменить последнее действие (Undo)
  - `Ctrl+Y` или `Ctrl+Shift+Z` — повторить действие (Redo)
- **Удобный интерфейс**: современный дизайн с адаптацией под мобильные устройства

## Установка и запуск

### Локальный запуск

1. **Установите Python 3.8+** (если еще не установлен)

2. **Установите зависимости**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Запустите приложение**:
   ```bash
   python app.py
   ```

4. **Откройте в браузере**:
   ```
   http://localhost:5000
   ```

### Настройка OpenRouter API

1. Получите API ключ на [openrouter.ai](https://openrouter.ai)
2. В веб-интерфейсе нажмите кнопку настроек (⚙)
3. Вставьте ключ и сохраните
4. Ключ будет храниться в localStorage браузера

Либо установите переменную среды:
```bash
# Windows (PowerShell)
$env:OPENROUTER_API_KEY="your-key-here"

# Linux/Mac
export OPENROUTER_API_KEY="your-key-here"
```

## Развертывание в производстве

### Вариант 1: Использование Gunicorn (Linux/Mac)

1. Установите Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Запустите:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Вариант 2: Использование Waitress (Windows)

1. Установите Waitress:
   ```bash
   pip install waitress
   ```

2. Запустите:
   ```bash
   waitress-serve --host=0.0.0.0 --port=5000 app:app
   ```

### Вариант 3: Docker

Создайте `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Запустите:
```bash
docker build -t radiohelper .
docker run -p 5000:5000 radiohelper
```

### Вариант 4: Облачные платформы

Приложение можно развернуть на:
- **Heroku**: создайте `Procfile` с содержимым `web: gunicorn app:app`
- **Railway**: просто подключите GitHub репозиторий
- **Render**: выберите Web Service и укажите команду запуска
- **PythonAnywhere**: загрузите файлы и настройте WSGI

## Структура проекта

```
radiohelper/
├── app.py              # Flask сервер
├── templates/
│   └── index.html      # HTML шаблон
├── static/
│   ├── style.css       # Стили
│   └── script.js       # JavaScript логика
├── requirements.txt    # Зависимости
├── main.py            # Старая десктопная версия
└── README.md          # Документация
```

## Примечания

- Веб-версия работает в любом современном браузере
- Данные не сохраняются на сервере (все локально в браузере)
- API ключ хранится в localStorage браузера
- Для работы AI требуется подключение к интернету

## Миграция с десктопной версии

Старая десктопная версия (`main.py`) сохранена для совместимости. Веб-версия полностью повторяет функциональность, но работает через браузер.

Для запуска старой версии:
```bash
pip install customtkinter pyperclip
python main.py
```

## Android (Jetpack Compose, офлайн калькулятор дозы)

В репозитории добавлен минимальный Android‑проект с офлайн‑калькулятором дозы (формула и коэффициенты такие же, как в веб‑версии). Код лежит в каталоге `mobile/android-app/`.

### Сборка через VS Code / терминал

#### Предварительная установка

1. **Установите JDK 17**:
   - Скачайте Temurin 17 (LTS) с https://adoptium.net/temurin/releases/ (Windows x64 MSI).
   - После установки задайте переменную окружения `JAVA_HOME`:
     ```powershell
     # В PowerShell (от администратора)
     [System.Environment]::SetEnvironmentVariable('JAVA_HOME', 'C:\Program Files\Eclipse Adoptium\jdk-17.0.x-hotspot', 'Machine')
     ```
   - Проверьте: `java -version`

2. **Установите Android SDK**:
   - Скачайте cmdline-tools с https://developer.android.com/studio#command-tools (Windows, commandlinetools-win-*.zip).
   - Создайте папку `C:\Android\cmdline-tools\latest` и распакуйте туда содержимое архива.
   - Задайте переменную окружения `ANDROID_HOME` и добавьте в PATH:
     ```powershell
     # В PowerShell (от администратора)
     [System.Environment]::SetEnvironmentVariable('ANDROID_HOME', 'C:\Android', 'Machine')
     $path = [System.Environment]::GetEnvironmentVariable('Path', 'Machine')
     [System.Environment]::SetEnvironmentVariable('Path', "$path;C:\Android\platform-tools;C:\Android\cmdline-tools\latest\bin", 'Machine')
     ```
   - Перезапустите PowerShell и установите компоненты SDK:
     ```powershell
     sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"
     sdkmanager --licenses
     ```   ls "C:\Program Files\Eclipse Adoptium\"

#### Сборка APK

1. В каталоге `mobile/android-app/` выполните:
   ```bash
   ./gradlew assembleDebug
   ```
   (на Windows можно `gradlew.bat assembleDebug`). Если wrapper ещё не сгенерирован, сначала выполните `gradle wrapper` (нужен установленный Gradle) или используйте установленный Gradle напрямую: `gradle assembleDebug`.
2. APK появится в `mobile/android-app/app/build/outputs/apk/debug/app-debug.apk`.
3. Установка на устройство/эмулятор (подключите устройство или запустите AVD):
   ```bash
   adb install -r mobile/android-app/app/build/outputs/apk/debug/app-debug.apk
   ```

### Что внутри

- Compose UI + ViewModel: выбор области/возраста, ввод DLP, кнопка «Рассчитать»; выводит текст `Эффективная доза: ...`.
- Коэффициенты и формула идентичны веб‑версии: `E = DLP × k`.
- Нет сетевых вызовов; всё офлайн.
