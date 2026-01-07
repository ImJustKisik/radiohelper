import customtkinter as ctk
import pyperclip
import os
import threading
import requests


class AnamnesisApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Помощник Рентгенлаборанта")
        self.geometry("560x700")

        # Состояние расчёта дозы
        self.last_dose_value = None
        self.last_dose_text = None

        # Настройка сетки
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Основной фрейм с прокруткой
        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Шапка с заголовком и кнопкой настроек
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.label_title = ctk.CTkLabel(
            self.header_frame,
            text="Сбор Анамнеза",
            font=("Roboto", 20, "bold")
        )
        self.label_title.grid(row=0, column=0, sticky="w")

        self.btn_settings_toggle = ctk.CTkButton(
            self.header_frame,
            text="⚙",
            width=36,
            command=self.toggle_settings,
            fg_color=("#3A7EBF", "#1F6AA5"),
            hover_color=("#326dad", "#144870")
        )
        self.btn_settings_toggle.grid(row=0, column=1, sticky="e", padx=(10, 0))

        # Окно настроек (Toplevel)
        self.settings_window = None

        # Состояние ключа OpenRouter
        self.api_key = os.getenv("OPENROUTER_API_KEY") or ""

        # --- Секция: Анамнез ---
        self.section_anamnesis = ctk.CTkFrame(self.main_frame)
        self.section_anamnesis.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        self.section_anamnesis.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.section_anamnesis,
            text="Анамнез",
            font=("Roboto", 15, "bold"),
            anchor="w"
        ).grid(row=0, column=0, sticky="ew", pady=(8, 6), padx=8)

        self.label_complaints = ctk.CTkLabel(self.section_anamnesis, text="Жалобы:", anchor="w")
        self.label_complaints.grid(row=1, column=0, sticky="ew", pady=(4, 0), padx=8)
        # Контейнер для поля жалоб с быстрой очисткой
        self.complaints_container = ctk.CTkFrame(self.section_anamnesis)
        self.complaints_container.grid(row=2, column=0, sticky="ew", padx=8, pady=(0, 6))
        self.complaints_container.grid_columnconfigure(0, weight=1)

        self.entry_complaints = ctk.CTkTextbox(
            self.complaints_container,
            height=80
        )
        self.entry_complaints.grid(row=0, column=0, sticky="ew", pady=(0, 0), padx=(0, 6))

        self.btn_clear_complaints = ctk.CTkButton(
            self.complaints_container,
            text="×",
            width=36,
            command=self.clear_complaints,
            fg_color=("gray75", "gray30"),
            hover_color=("gray65", "gray25")
        )
        self.btn_clear_complaints.grid(row=0, column=1, sticky="ns")

        # Кнопки управления жалобами в один ряд
        self.complaints_buttons_frame = ctk.CTkFrame(self.section_anamnesis, fg_color="transparent")
        self.complaints_buttons_frame.grid(row=3, column=0, sticky="ew", pady=(6, 10), padx=8)
        self.complaints_buttons_frame.grid_columnconfigure(0, weight=1)
        self.complaints_buttons_frame.grid_columnconfigure(1, weight=1)

        self.btn_ai_complaints = ctk.CTkButton(
            self.complaints_buttons_frame,
            text="✨ Улучшить (AI)",
            command=self.improve_complaints,
            fg_color=("#3A7EBF", "#1F6AA5"),
            hover_color=("#326dad", "#144870")
        )
        self.btn_ai_complaints.grid(row=0, column=0, sticky="ew", padx=(0, 4))

        self.btn_no_complaints = ctk.CTkButton(
            self.complaints_buttons_frame,
            text="Жалоб нет",
            command=self.fill_no_complaints,
            fg_color=("#3A7EBF", "#1F6AA5"),
            hover_color=("#326dad", "#144870")
        )
        self.btn_no_complaints.grid(row=0, column=1, sticky="ew", padx=(4, 0))

        self.label_trauma = ctk.CTkLabel(self.section_anamnesis, text="Травмы:", anchor="w")
        self.label_trauma.grid(row=4, column=0, sticky="ew", padx=8)
        self.option_trauma = ctk.CTkOptionMenu(
            self.section_anamnesis,
            values=["Нет", "Бытовая", "Спортивная", "ДТП", "Уличная", "Производственная"]
        )
        self.option_trauma.set("Нет")
        self.option_trauma.grid(row=5, column=0, sticky="ew", pady=(0, 8), padx=8)

        self.label_operations = ctk.CTkLabel(self.section_anamnesis, text="Операции / импланты:", anchor="w")
        self.label_operations.grid(row=6, column=0, sticky="ew", padx=8)
        self.option_operations = ctk.CTkOptionMenu(
            self.section_anamnesis,
            values=["Нет", "В анамнезе", "Металлоконструкции", "Кардиостимулятор", "Стентирование"],
            command=self.on_operations_change
        )
        self.option_operations.set("Нет")
        self.option_operations.grid(row=7, column=0, sticky="ew", pady=(0, 8), padx=8)

        self.label_operations_detail = ctk.CTkLabel(self.section_anamnesis, text="Уточните вмешательство:", anchor="w")
        self.entry_operations_detail = ctk.CTkEntry(self.section_anamnesis, placeholder_text="Например: артроскопия коленного сустава")
        self.operations_detail_visible = False

        self.label_contrast = ctk.CTkLabel(self.section_anamnesis, text="Аллергия на контраст:", anchor="w")
        self.label_contrast.grid(row=10, column=0, sticky="ew", padx=8)
        self.option_contrast = ctk.CTkOptionMenu(
            self.section_anamnesis,
            values=["Нет", "Есть", "Неизвестно"],
            width=200
        )
        self.option_contrast.set("Нет")
        self.option_contrast.grid(row=11, column=0, sticky="ew", pady=(0, 8), padx=8)

        self.label_pregnancy = ctk.CTkLabel(self.section_anamnesis, text="Беременность (для женщин):", anchor="w")
        self.label_pregnancy.grid(row=12, column=0, sticky="ew", padx=8)
        self.option_pregnancy = ctk.CTkOptionMenu(
            self.section_anamnesis,
            values=["Не актуально", "Отрицает", "Возможна", "Подтверждена"],
            width=200
        )
        self.option_pregnancy.set("Не актуально")
        self.option_pregnancy.grid(row=13, column=0, sticky="ew", pady=(0, 8), padx=8)

        # Дополнительно / особенности
        self.label_extra = ctk.CTkLabel(self.section_anamnesis, text="Особенности / риски:", anchor="w")
        self.label_extra.grid(row=14, column=0, sticky="ew", padx=8)
        self.entry_extra = ctk.CTkEntry(self.section_anamnesis, placeholder_text="Например: бронхиальная астма, диабет")
        self.entry_extra.grid(row=15, column=0, sticky="ew", pady=(0, 12), padx=8)

        # --- Секция: Подготовка ---
        self.section_prep = ctk.CTkFrame(self.main_frame)
        self.section_prep.grid(row=3, column=0, sticky="ew", pady=(0, 12))
        self.section_prep.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.section_prep,
            text="Подготовка",
            font=("Roboto", 15, "bold"),
            anchor="w"
        ).grid(row=0, column=0, sticky="ew", pady=(8, 6), padx=8)

        self.label_prep = ctk.CTkLabel(self.section_prep, text="Подготовка / диета:", anchor="w")
        self.label_prep.grid(row=1, column=0, sticky="ew", padx=8)
        self.entry_prep = ctk.CTkEntry(self.section_prep, placeholder_text="Например: натощак, кишечник очищен")
        self.entry_prep.grid(row=2, column=0, sticky="ew", pady=(0, 8), padx=8)

        # Кнопка показа комментария врача-направителя
        self.btn_show_referrer = ctk.CTkButton(
            self.section_prep,
            text="Показать комментарий направления",
            command=self.toggle_referrer,
            fg_color=("#3A7EBF", "#1F6AA5"),
            hover_color=("#326dad", "#144870")
        )
        self.btn_show_referrer.grid(row=3, column=0, sticky="e", pady=(0, 8), padx=8)

        # Комментарий врача-направителя (скрыт до нажатия)
        self.label_referrer = ctk.CTkLabel(self.section_prep, text="Комментарий врача-направителя:", anchor="w")
        self.entry_referrer = ctk.CTkEntry(self.section_prep, placeholder_text="Коротко суть направления")
        self.referrer_visible = False

        # --- Секция: Расчёт дозы ---
        self.section_dose = ctk.CTkFrame(self.main_frame)
        self.section_dose.grid(row=3, column=0, sticky="ew", pady=(0, 12))
        self.section_dose.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.section_dose,
            text="Расчёт эффективной дозы (E)",
            font=("Roboto", 15, "bold"),
            anchor="w"
        ).grid(row=0, column=0, sticky="ew", pady=(8, 6), padx=8)

        self.label_dlp = ctk.CTkLabel(self.section_dose, text="DLP (мГр·см):", anchor="w")
        self.label_dlp.grid(row=1, column=0, sticky="ew", pady=(0, 0), padx=8)
        self.entry_dlp = ctk.CTkEntry(self.section_dose, placeholder_text="Например: 800")
        self.entry_dlp.grid(row=2, column=0, sticky="ew", pady=(0, 2), padx=8)
        self.entry_dlp.bind("<Return>", lambda e: self.calculate_dose())
        
        self.hint_dlp = ctk.CTkLabel(
            self.section_dose,
            text="Используйте точку или запятую для дробной части",
            text_color="gray",
            anchor="w"
        )
        self.hint_dlp.grid(row=3, column=0, sticky="ew", padx=8, pady=(0, 8))

        self.label_dlp_region = ctk.CTkLabel(self.section_dose, text="Область для расчёта дозы:", anchor="w")
        self.label_dlp_region.grid(row=4, column=0, sticky="ew", padx=8)
        self.option_dlp_region = ctk.CTkOptionMenu(self.section_dose, values=["Голова", "Туловище"])
        self.option_dlp_region.set("Голова")
        self.option_dlp_region.grid(row=5, column=0, sticky="ew", pady=(0, 6), padx=8)

        self.label_dlp_age = ctk.CTkLabel(self.section_dose, text="Возрастная группа:", anchor="w")
        self.label_dlp_age.grid(row=6, column=0, sticky="ew", padx=8)
        self.option_dlp_age = ctk.CTkOptionMenu(
            self.section_dose,
            values=[">15 лет", "15 лет", "10 лет", "5 лет", "1 год", "0-1 год"]
        )
        self.option_dlp_age.set(">15 лет")
        self.option_dlp_age.grid(row=7, column=0, sticky="ew", pady=(0, 8), padx=8)

        self.btn_calc_dose = ctk.CTkButton(
            self.section_dose,
            text="Рассчитать дозу",
            command=self.calculate_dose,
            fg_color=("#3A7EBF", "#1F6AA5"),
            hover_color=("#326dad", "#144870")
        )
        self.btn_calc_dose.grid(row=8, column=0, sticky="ew", pady=(0, 6), padx=8)

        self.label_dose_result = ctk.CTkLabel(self.section_dose, text="", anchor="w", justify="left")
        self.label_dose_result.grid(row=9, column=0, sticky="ew", pady=(0, 6), padx=8)

        # --- Секция: Итог ---
        self.section_result = ctk.CTkFrame(self.main_frame)
        self.section_result.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        self.section_result.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            self.section_result,
            text="Итоговый текст",
            font=("Roboto", 15, "bold"),
            anchor="w"
        ).grid(row=0, column=0, columnspan=2, sticky="ew", pady=(8, 6), padx=8)

        self.btn_generate = ctk.CTkButton(self.section_result, text="Сформировать текст", command=self.generate_text)
        self.btn_generate.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 6), padx=8)

        self.label_result = ctk.CTkLabel(self.section_result, text="Результат:", anchor="w")
        self.label_result.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(4, 0), padx=8)
        self.textbox_result = ctk.CTkTextbox(self.section_result, height=160)
        self.textbox_result.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 8), padx=8)

        self.btn_copy = ctk.CTkButton(
            self.section_result,
            text="Копировать",
            command=self.copy_to_clipboard,
            fg_color=("#2CC985", "#2FA572"),
            hover_color=("#229965", "#1E7E55")
        )
        self.btn_copy.grid(row=4, column=0, sticky="ew", pady=(0, 8), padx=(8, 4))

        self.btn_clear = ctk.CTkButton(
            self.section_result,
            text="Очистить поля",
            command=self.clear_fields,
            fg_color=("gray75", "gray30"),
            hover_color=("gray65", "gray25")
        )
        self.btn_clear.grid(row=4, column=1, sticky="ew", pady=(0, 8), padx=(4, 8))

        # Статус бар (для уведомлений)
        self.status_label = ctk.CTkLabel(self.main_frame, text="", text_color="gray")
        self.status_label.grid(row=5, column=0, pady=(4, 0))

        # Фокус и горячие клавиши
        self.entry_complaints.focus_set()
        self.bind("<Control-Return>", lambda e: self.generate_text())
        self.bind("<Control-KP_Enter>", lambda e: self.generate_text())
        self.bind("<Control-c>", lambda e: self.copy_to_clipboard())
        self.bind("<Escape>", lambda e: self.clear_fields())

    def set_status(self, text: str, color: str = "gray", timeout: int | None = 2500):
        """Установить текст статуса и автоматически очистить по таймеру."""
        self.status_label.configure(text=text, text_color=color)
        if timeout:
            self.after(timeout, lambda: self.status_label.configure(text=""))

    def toggle_settings(self):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = ctk.CTkToplevel(self)
            self.settings_window.title("Настройки")
            self.settings_window.geometry("400x220")
            
            # Делаем окно модальным (по желанию) или просто поверх
            self.settings_window.attributes("-topmost", True)

            ctk.CTkLabel(
                self.settings_window, 
                text="Настройки приложения", 
                font=("Roboto", 16, "bold")
            ).pack(pady=15)

            ctk.CTkLabel(self.settings_window, text="OpenRouter API Key:").pack(pady=(0, 5), padx=20, anchor="w")

            # Контейнер для поля ввода и кнопки вставки
            entry_frame = ctk.CTkFrame(self.settings_window, fg_color="transparent")
            entry_frame.pack(pady=(0, 15), padx=20, fill="x")

            self.settings_entry_api_key = ctk.CTkEntry(entry_frame, show="*")
            self.settings_entry_api_key.pack(side="left", fill="x", expand=True, padx=(0, 5))
            
            # Кнопка вставки из буфера обмена
            btn_paste = ctk.CTkButton(
                entry_frame, 
                text="Вставить", 
                width=70, 
                command=lambda: self.paste_to_entry(self.settings_entry_api_key),
                fg_color=("gray75", "gray30"),
                hover_color=("gray65", "gray25")
            )
            btn_paste.pack(side="right")
            
            if self.api_key:
                self.settings_entry_api_key.insert(0, self.api_key)

            ctk.CTkButton(
                self.settings_window, 
                text="Сохранить и закрыть", 
                command=self.save_api_key,
                fg_color=("#3A7EBF", "#1F6AA5"),
                hover_color=("#326dad", "#144870")
            ).pack(pady=10)
            
        else:
            self.settings_window.focus()

    def save_api_key(self):
        if not hasattr(self, "settings_entry_api_key") or not self.settings_entry_api_key.winfo_exists():
            return

        key = self.settings_entry_api_key.get().strip()
        if not key:
            self.api_key = ""
            self.set_status("Ключ очищен", color="gray")
        else:
            self.api_key = key
            self.set_status("Ключ сохранён (в памяти сессии)", color=("#2CC985", "#2FA572"))
        
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.destroy()

    def _set_ai_btn_state(self, busy: bool):
        if busy:
            self.btn_ai_complaints.configure(state="disabled", text="Обработка...")
        else:
            self.btn_ai_complaints.configure(state="normal", text="Улучшить жалобы (AI)")

    def improve_complaints(self):
        text = self.entry_complaints.get("1.0", "end-1c").strip()
        if not text:
            self.set_status("Заполните жалобы перед улучшением", color="red")
            return

        api_key = self.api_key or os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            self.set_status("Укажите ключ в настройках", color="red")
            return

        self._set_ai_btn_state(True)
        self.set_status("AI обрабатывает жалобы...")

        thread = threading.Thread(target=self._improve_complaints_worker, args=(text, api_key), daemon=True)
        thread.start()

    def _improve_complaints_worker(self, text: str, api_key: str):
        try:
            improved = self._call_openrouter(text, api_key)
            self.after(0, lambda: self._apply_improved_complaints(improved))
        except Exception as exc:  # pylint: disable=broad-except
            self.after(0, lambda: self._finish_ai_error(f"AI ошибка: {exc}"))

    def _apply_improved_complaints(self, improved: str | None):
        self._set_ai_btn_state(False)
        if improved:
            self.entry_complaints.delete("1.0", "end")
            self.entry_complaints.insert("1.0", improved.strip())
            self.set_status("Жалобы улучшены", color=("#2CC985", "#2FA572"))
        else:
            self.set_status("AI не вернул текст", color="red")

    def _finish_ai_error(self, message: str):
        self._set_ai_btn_state(False)
        self.set_status(message, color="red", timeout=4000)

    def _call_openrouter(self, complaints_text: str, api_key: str) -> str:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "radiohelper-local",
            "X-Title": "radiohelper-app",
        }
        payload = {
            "model": "google/gemini-3-flash-preview",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Ты медицинский редактор. Перепиши текст жалоб/анамнеза кратко и профессионально на русском "
                        "в стиле клинических записей, как в примерах: 'На постоянную, средней интенсивности боль...' / "
                        "'Со слов во время ... Хронические заболевания отрицает...'. Требования: 1–3 коротких предложения, "
                        "без списков и кавычек; не добавляй факты, которых нет в исходнике; сохрани отрицания 'отрицает/не отрицает'; "
                        "убери вводные слова про пациента; исправь грамматику и синтаксис, но не выдумывай новые данные."
                    ),
                },
                {"role": "user", "content": complaints_text},
            ],
            "temperature": 0.3,
            "max_tokens": 256,
        }

        response = requests.post(url, headers=headers, json=payload, timeout=20)
        if response.status_code == 401:
            raise Exception("Проверьте OPENROUTER_API_KEY")
        response.raise_for_status()
        data = response.json()
        choices = data.get("choices")
        if not choices:
            raise Exception("Пустой ответ от модели")
        content = choices[0].get("message", {}).get("content")
        if not content:
            raise Exception("Модель не вернула текст")
        return content.strip()

    def fill_no_complaints(self):
        self.entry_complaints.delete("1.0", "end")
        self.entry_complaints.insert("1.0", "не предъявляет")
        self.set_status("Жалобы: не предъявляет", color=("#2CC985", "#2FA572"))

    def clear_complaints(self):
        self.entry_complaints.delete("1.0", "end")
        self.entry_complaints.focus_set()
        self.set_status("Жалобы очищены")

    def clear_fields(self):
        self.entry_complaints.delete("1.0", "end")
        self.option_trauma.set("Нет")
        self.option_operations.set("Нет")
        self.option_contrast.set("Нет")
        self.option_pregnancy.set("Не актуально")
        self.entry_prep.delete(0, "end")
        self.entry_referrer.delete(0, "end")
        self.entry_operations_detail.delete(0, "end")
        self.entry_extra.delete(0, "end")
        self.entry_dlp.delete(0, "end")
        self.option_dlp_region.set("Голова")
        self.option_dlp_age.set(">15 лет")
        self.label_dose_result.configure(text="", text_color="gray")
        self.last_dose_value = None
        self.last_dose_text = None
        self.textbox_result.delete("1.0", "end")
        if self.referrer_visible:
            self.label_referrer.grid_remove()
            self.entry_referrer.grid_remove()
            self.referrer_visible = False
            self.btn_show_referrer.configure(text="Показать комментарий направления")
        if self.operations_detail_visible:
            self.label_operations_detail.grid_remove()
            self.entry_operations_detail.grid_remove()
            self.operations_detail_visible = False
        self.entry_complaints.focus_set()
        self.set_status("Поля очищены")

    def calculate_dose(self):
        coeffs = {
            "Голова": {
                ">15 лет": 0.0023,
                "15 лет": 0.00276,
                "10 лет": 0.0046,
                "5 лет": 0.00736,
                "1 год": 0.01173,
                "0-1 год": 0.02185,
            },
            "Туловище": {
                ">15 лет": 0.0081,
                "15 лет": 0.00972,
                "10 лет": 0.01458,
                "5 лет": 0.02106,
                "1 год": 0.03240,
                "0-1 год": 0.06399,
            },
        }

        raw_dlp = self.entry_dlp.get().strip()
        region = self.option_dlp_region.get()
        age = self.option_dlp_age.get()

        try:
            dlp = float(raw_dlp.replace(",", ".")) if raw_dlp else None
        except ValueError:
            self.label_dose_result.configure(text="Некорректный DLP", text_color="red")
            self.last_dose_value = None
            self.last_dose_text = None
            self.set_status("Введите число, например 800 или 800.5", color="red")
            return

        if dlp is None:
            self.label_dose_result.configure(text="Введите DLP", text_color="red")
            self.last_dose_value = None
            self.last_dose_text = None
            self.set_status("Поле DLP пустое", color="red")
            return

        k = coeffs.get(region, {}).get(age)
        if k is None:
            self.label_dose_result.configure(text="Нет коэффициента для выбора", text_color="red")
            self.last_dose_value = None
            self.last_dose_text = None
            self.set_status("Проверьте область и возраст", color="red")
            return

        dose_msv = dlp * k
        self.last_dose_value = dose_msv
        self.last_dose_text = f"Эффективная доза: {dose_msv:.2f} мЗв (DLP={dlp:.0f}, k={k})"
        self.label_dose_result.configure(text=self.last_dose_text, text_color=("#2CC985", "#2FA572"))
        self.set_status("Доза рассчитана", color=("#2CC985", "#2FA572"))

    def toggle_referrer(self):
        if not self.referrer_visible:
            self.label_referrer.grid(row=4, column=0, sticky="ew", pady=(0, 0), padx=8)
            self.entry_referrer.grid(row=5, column=0, sticky="ew", pady=(0, 8), padx=8)
            self.referrer_visible = True
            self.btn_show_referrer.configure(text="Скрыть комментарий направления")
            self.entry_referrer.focus()
        else:
            self.label_referrer.grid_remove()
            self.entry_referrer.grid_remove()
            self.referrer_visible = False
            self.entry_referrer.delete(0, "end")
            self.btn_show_referrer.configure(text="Показать комментарий направления")
            self.entry_prep.focus()

    def on_operations_change(self, value):
        if value != "Нет":
            if not self.operations_detail_visible:
                self.label_operations_detail.grid(row=8, column=0, sticky="ew", padx=8)
                self.entry_operations_detail.grid(row=9, column=0, sticky="ew", pady=(0, 8), padx=8)
                self.operations_detail_visible = True
            self.entry_operations_detail.focus()
        else:
            if self.operations_detail_visible:
                self.label_operations_detail.grid_remove()
                self.entry_operations_detail.grid_remove()
                self.operations_detail_visible = False
            self.entry_operations_detail.delete(0, "end")

    def generate_text(self):
        # страховка на случай, если объект создан без инициализации состояния дозы
        if not hasattr(self, "last_dose_value"):
            self.last_dose_value = None
        if not hasattr(self, "last_dose_text"):
            self.last_dose_text = None

        complaints = self.entry_complaints.get("1.0", "end-1c").strip()
        trauma = self.option_trauma.get()
        operations = self.option_operations.get()
        contrast = self.option_contrast.get()
        pregnancy = self.option_pregnancy.get()
        prep = self.entry_prep.get().strip()
        referrer = self.entry_referrer.get().strip()
        extra = self.entry_extra.get().strip()
        operations_detail = self.entry_operations_detail.get().strip()

        trauma_value = "Отрицает" if trauma == "Нет" else trauma
        operations_value = "Отрицает" if operations == "Нет" else operations
        complaints_value = complaints if complaints else "Отрицает"

        if operations != "Нет":
            if operations_detail:
                operations_text = f"{operations} ({operations_detail})"
            else:
                operations_text = f"{operations} (уточнить)"
        else:
            operations_text = operations_value

        lines = []
        lines.append(f"Жалобы: {complaints_value}")
        lines.append(f"Травмы: {trauma_value}")
        lines.append(f"Операции/импланты: {operations_text}")
        lines.append(f"Аллергия на контраст: {contrast}")

        if pregnancy and pregnancy != "Не актуально":
            lines.append(f"Беременность: {pregnancy}")

        if prep:
            lines.append(f"Подготовка/диета: {prep}")

        if referrer:
            lines.append(f"Комментарий направления: {referrer}")

        if extra:
            lines.append(f"Особенности: {extra}")

        if self.last_dose_value is not None and self.last_dose_text:
            lines.append(self.last_dose_text)

        final_text = "\n".join(lines)

        self.textbox_result.delete("1.0", "end")
        self.textbox_result.insert("1.0", final_text)
        self.set_status("Текст сформирован", color=("#2CC985", "#2FA572"))

    def copy_to_clipboard(self):
        text = self.textbox_result.get("1.0", "end-1c")
        if text.strip():
            pyperclip.copy(text)
            self.set_status("Скопировано в буфер обмена!", color=("#2CC985", "#2FA572"))
        else:
            self.set_status("Нет текста для копирования", color="red", timeout=3000)

    def paste_to_entry(self, entry_widget):
        try:
            text = pyperclip.paste()
            if text:
                entry_widget.delete(0, "end")
                entry_widget.insert(0, text)
        except Exception:
            pass


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = AnamnesisApp()
    app.mainloop()
