# Быстрая инструкция: GitHub-управляемый справочник

## Что произойдёт:

1. **Ты редактируешь** `guide.json` в VS Code (на своём ПК)
2. **Коммитишь и пушишь** в GitHub
3. **Приложение обновляется** автоматически с GitHub

## Первый запуск

### 1. Создай репозиторий на GitHub:
```
https://github.com/new
```
- Имя: `radiohelper-guide`
- Выбери "Public"
- "Add a README file"

### 2. Клонируй локально:
```bash
git clone https://github.com/YOUR_USERNAME/radiohelper-guide.git
cd radiohelper-guide
```

### 3. Скопируй guide.json:
```bash
# Из основного проекта radiohelper
cp ../radiohelper/guide.json .
git add guide.json
git commit -m "Initial guide.json"
git push origin main
```

### 4. Получи Raw URL:
Открой в браузере и нажми "Raw":
```
https://github.com/YOUR_USERNAME/radiohelper-guide/blob/main/guide.json
```

Получишь URL вида:
```
https://raw.githubusercontent.com/YOUR_USERNAME/radiohelper-guide/main/guide.json
```

### 5. Обнови URL в приложении:
[GuideRepository.kt](mobile/android-app/app/src/main/java/com/radiohelper/dosecalc/guide/GuideRepository.kt) (строка 7):

```kotlin
private val baseUrl = "https://raw.githubusercontent.com/YOUR_USERNAME/radiohelper-guide/main/"
```

### 6. Собери APK:
```bash
cd mobile/android-app
.\gradlew.bat :app:assembleDebug
```

---

## Работа с протоколами

### Редактирование:
1. Открой `guide.json` в VS Code
2. Отредактируй протоколы (название, описание, параметры)
3. **Важно:** увеличь `version` на 1

### Добавление нового:
Скопируй существующий протокол и измени:
- `id` — уникальный идентификатор (строчные буквы + подчёркивание)
- `title` — название
- `type` — `"CT"` или `"RENTGEN"`
- `region` — область (HEAD, CHEST, SPINE, ABDOMEN, PELVIS, LIMBS, ALL)
- `kv`, `mas` — параметры
- `description` — описание

### Загрузка на сервер:
```bash
cd radiohelper-guide

# Отредактировал файл
code guide.json

# Проверь что нравится
git diff guide.json

# Коммит
git add guide.json
git commit -m "Update protocols: added CT abdomen protocol"

# Загрузить
git push origin main
```

### Обновление в приложении:
- Пользователь нажимает "🔄" в справочнике
- Или приложение проверяет при открытии
- Скачивает новый `guide.json` с GitHub

---

## Примеры коммитов:

```bash
git commit -m "Add CT protocols for thorax"
git commit -m "Update chest X-ray description"
git commit -m "Fix typo in skull protocol"
git commit -m "Increase version to 2.0: major update"
```

---

## Возможные проблемы:

**Q: Приложение не обновляется?**
A: 
- Проверь URL в GuideRepository.kt (правильный username?)
- Собери новый APK и переустанови
- Убедись что guide.json лежит на GitHub raw URL

**Q: JSON синтаксис ошибка?**
A:
- Открой guide.json в браузере (если ошибка, GitHub покажет)
- Используй VS Code JSON валидатор

**Q: Потерял старые версии?**
A:
- Git история сохраняет всё!
- `git log` — посмотреть историю
- `git checkout <commit>` — вернуться к старой версии

---

## Структура JSON:

```json
{
  "version": 2,                    // Поднимай при обновлении
  "lastUpdated": "2026-01-08T15:00:00Z",
  "protocols": [
    {
      "id": "unique_id",          // Уникальный (не меняй!)
      "title": "Название",
      "type": "CT" или "RENTGEN",
      "region": "HEAD/CHEST/SPINE/ABDOMEN/PELVIS/LIMBS/ALL",
      "kv": "120 кВ",
      "mas": "200-300 мАс",
      "description": "Подробное описание укладки...",
      "imageUrl": null            // Будущее расширение для картинок
    }
  ]
}
```

Готово! Теперь полный контроль над протоколами 🎉
