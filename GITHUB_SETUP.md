# GitHub Setup Guide

Как настроить оба репозитория и синхронизировать код.

## 📋 Шаг 1: Инициализация radiohelper (основной репозиторий)

```powershell
cd c:\Users\pizzalover\Desktop\radiohelper

# Инициализируем git (если не инициализирован)
git init

# Добавляем все файлы (кроме игнорируемых)
git add .

# Первый коммит
git commit -m "Initial commit: Flask app, Streamlit editor, guide system"

# Переименовываем ветку в main
git branch -M main

# Добавляем удалённый репозиторий
git remote add origin https://github.com/ImJustKisik/radiohelper.git

# Загружаем код на GitHub
git push -u origin main
```

## 🚀 Шаг 2: Инициализация radiohelper-app (мобильное приложение)

```powershell
cd c:\Users\pizzalover\Desktop\radiohelper\mobile\android-app

# Инициализируем git
git init

# Добавляем все файлы
git add .

# Первый коммит
git commit -m "Initial commit: Android app with Jetpack Compose"

# Переименовываем ветку в main
git branch -M main

# Добавляем удалённый репозиторий
git remote add origin https://github.com/ImJustKisik/radiohelper-app.git

# Загружаем код на GitHub
git push -u origin main
```

## 📝 Шаг 3: Проверка

После загрузки проверь на GitHub:

### radiohelper
- [ ] https://github.com/ImJustKisik/radiohelper
- [ ] Видишь `app.py`, `guide_editor.py`, `guide.json`
- [ ] Папка `guide_images/` пуста (или с изображениями)
- [ ] Папка `templates/` и `static/` с файлами

### radiohelper-app  
- [ ] https://github.com/ImJustKisik/radiohelper-app
- [ ] Видишь папку `app/` с исходным кодом
- [ ] Файл `build.gradle.kts`

## 🔄 Шаг 4: Будущие обновления

### Обновление методик (из radiohelper)

```powershell
cd c:\Users\pizzalover\Desktop\radiohelper

# После добавления новых методик через Streamlit редактор
git add guide.json guide_images/
git commit -m "Add new protocols and images"
git push origin main
```

### Обновление приложения (из radiohelper-app)

```powershell
cd c:\Users\pizzalover\Desktop\radiohelper\mobile\android-app

# После изменений кода
git add .
git commit -m "Update Android app"
git push origin main
```

## ✅ Готово!

Теперь:
1. **radiohelper** — основной репо с Flask, Streamlit, методиками
2. **radiohelper-app** — мобильное приложение
3. Приложение автоматически загружает методики с: `https://raw.githubusercontent.com/ImJustKisik/radiohelper/main/guide.json`

При каждом обновлении методик пользователи получат новые данные на следующий запуск приложения.
