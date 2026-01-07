# Настройка GitHub-центричного управления протоколами

## Шаг 1: Создание GitHub репозитория

1. Создай **новый публичный репозиторий** на GitHub:
   - Имя: `radiohelper-guide` (или другое)
   - Публичный репозиторий (чтобы приложение мог скачивать JSON)
   - Инициализировать с README

2. Клонируй репозиторий:
```bash
git clone https://github.com/YOUR_USERNAME/radiohelper-guide.git
cd radiohelper-guide
```

## Шаг 2: Подготовка файла guide.json

1. Скопируй `guide.json` из проекта в корень репозитория:
```bash
cp ../radiohelper/mobile/android-app/app/src/main/res/raw/guide.json .
```

2. Добавь версию в начало файла:
```json
{
  "version": 1,
  "lastUpdated": "2026-01-07",
  "protocols": [...]
}
```

3. Коммит:
```bash
git add guide.json
git commit -m "Initial guide.json with protocols"
git push origin main
```

## Шаг 3: Получить GitHub Raw URL

1. Открой файл в GitHub:
   - `https://github.com/YOUR_USERNAME/radiohelper-guide/blob/main/guide.json`

2. Нажми "Raw" — получишь URL:
   - `https://raw.githubusercontent.com/YOUR_USERNAME/radiohelper-guide/main/guide.json`

## Шаг 4: Обновить URL в приложении

Обнови в [GuideRepository.kt](mobile/android-app/app/src/main/java/com/radiohelper/dosecalc/guide/GuideRepository.kt):

```kotlin
private val baseUrl = "https://raw.githubusercontent.com/YOUR_USERNAME/radiohelper-guide/main/"
```

Замени:
- `YOUR_USERNAME` на твой GitHub username
- `radiohelper-guide` на имя своего репозитория

## Шаг 5: Редактирование протоколов

Теперь ты можешь:

1. **Локально в VS Code:**
   - Открыть `guide.json`
   - Редактировать протоколы
   - Увеличивать версию: `"version": 2`
   - Обновить дату: `"lastUpdated": "2026-01-08"`

2. **Загрузить на сервер:**
```bash
git add guide.json
git commit -m "Update protocols: added new CT protocols for chest"
git push origin main
```

3. **Приложение обновится:**
   - Нажми кнопку "Обновить" в справочнике
   - Или автоматически при следующем открытии

## JSON Структура

```json
{
  "version": 1,
  "lastUpdated": "2026-01-07T10:00:00Z",
  "protocols": [
    {
      "id": "ct_head_standard",
      "title": "КТ головного мозга стандартная",
      "type": "CT",
      "region": "HEAD",
      "kv": "120 кВ",
      "mas": "200-300 мАс",
      "description": "Подробное описание...",
      "imageUrl": null
    }
  ]
}
```

**Типы:**
- `type`: `"CT"` или `"RENTGEN"`
- `region`: `"HEAD"`, `"CHEST"`, `"SPINE"`, `"ABDOMEN"`, `"PELVIS"`, `"LIMBS"`, `"ALL"`

## Версионирование

Поднимай версию при значимых изменениях:
- v1 → v2: добавлены новые протоколы
- v1 → v1.1: исправлены описания (опционально)

Приложение будет уведомлять пользователей при обновлении версии.

## Советы

- ✅ Коммитим часто с понятными сообщениями
- ✅ Храним историю изменений (через git history)
- ✅ Тестируем локально перед push
- ✅ Не забываем обновить version и lastUpdated
- ❌ Не делаем большие break-changes без подготовки пользователей
