# Copilot Instructions: RadioHelper

This repo has two primary apps: a Flask web app (patient anamnesis + dose calculator + AI text refining) and a minimal Android app (offline dose calculator). A legacy desktop `customtkinter` UI mirrors the web features.

## Language
- All AI agent responses and user-facing text must be in Russian.

## Architecture & Key Files
- Flask server: `app.py` — routes `/`, `/api/improve-complaints`, `/api/calculate-dose` (uses `DOSE_COEFFICIENTS`).
- Frontend: `templates/index.html`, `static/script.js`, `static/style.css` — vanilla JS, no framework.
- Desktop legacy: `main.py` — `customtkinter` UI with the same flows.
- Android: `mobile/android-app/` — Jetpack Compose app; build config in `app/build.gradle.kts`, manifest in `app/src/main/AndroidManifest.xml`.

## Dev Workflows
- Web run:
  1. `pip install -r requirements.txt`
  2. `python app.py` → open http://localhost:5000
- Android build (Windows):
  - `Set-Location mobile/android-app; .\gradlew.bat :app:assembleDebug`
  - APK: `mobile/android-app/app/build/outputs/apk/debug/app-debug.apk`
- Desktop legacy run:
  - `pip install customtkinter pyperclip`
  - `python main.py`

## Backend API Contracts
- POST `/api/improve-complaints`
  - Body: `{ text: string, api_key?: string }`
  - Uses OpenRouter (`Authorization: Bearer`), model `google/gemini-3-flash-preview`.
  - Error 401 → missing/invalid `OPENROUTER_API_KEY`.
- POST `/api/calculate-dose`
  - Body: `{ dlp: number, region: 'Голова'|'Туловище', age: one of ['>15 лет','15 лет','10 лет','5 лет','1 год','0-1 год'] }`
  - Returns `{ dose_msv: number, dose_text: string }` built from `DOSE_COEFFICIENTS`.

## Frontend Patterns (script.js)
- Global state for Undo/Redo: `history[]`, `historyIndex`, `MAX_HISTORY=50`.
- Persist OpenRouter key in `localStorage('openrouter_api_key')`.
- Keyboard shortcuts: Ctrl+Enter (generate), Esc (clear), Ctrl+Z/Y (undo/redo).
- Dose flow: client normalizes DLP (comma→dot) then calls `/api/calculate-dose`; UI shows `lastDoseText`.
- Operations detail UI toggles when `operations != 'Нет'`.

## Output Text Conventions
- Generated lines order: Жалобы → Травмы → Операции/импланты → Аллергия → Беременность (если не "Не актуально") → Подготовка → Комментарий направления → Особенности → Доза.
- Defaults: empty complaint → `Отрицает`; operations `Нет` → `Отрицает`; operations with detail → `Операции (деталь)` else `Операции (уточнить)`.

## Android Notes
- Namespace `com.radiohelper.dosecalc`, minSdk 24, targetSdk 34.
- Adaptive launcher icon at `res/mipmap-anydpi-v26/ic_launcher.xml` and declared in manifest `android:icon="@mipmap/ic_launcher"`.
- Pure offline dose calculation (mirror of web coefficients).

## Examples
- Dose (curl): `curl -X POST http://localhost:5000/api/calculate-dose -H "Content-Type: application/json" -d "{\"dlp\":800,\"region\":\"Голова\",\"age\":\">15 лет\"}"`
- Improve (curl): `curl -X POST http://localhost:5000/api/improve-complaints -H "Content-Type: application/json" -d "{\"text\":\"Болит колено...\"}"`

## Extending
- Add fields: update `index.html` controls, wire events in `script.js` (include in `getFormState/restoreFormState` and history), adjust `generate` logic order if needed.
- Dose tables: edit `DOSE_COEFFICIENTS` in `app.py`; keep age/region keys consistent with client selects.
- AI model: change `model` in `app.py` or pass via request; keep concise system prompt in Russian.
