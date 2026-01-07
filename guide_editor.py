"""
RadioHelper Guide Editor
Streamlit приложение для редактирования медицинских протоколов
"""

import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd
from pathlib import Path
import shutil

# ============= КОНФИГУРАЦИЯ =============
st.set_page_config(page_title="RadioHelper Guide Editor", layout="wide")

GUIDE_JSON_PATH = os.path.join(os.path.dirname(__file__), 'guide.json')
IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'guide_images')

# Создаём папку для изображений если её нет
Path(IMAGES_DIR).mkdir(exist_ok=True)

# Стили
st.markdown("""
<style>
    .main { padding: 2rem; }
    .metric { font-size: 1.2rem; font-weight: bold; }
    .success { color: green; }
    .error { color: red; }
</style>
""", unsafe_allow_html=True)

# ============= ФУНКЦИИ =============

def load_guide_data():
    """Загрузить данные из guide.json"""
    try:
        with open(GUIDE_JSON_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Файл не найден: {GUIDE_JSON_PATH}")
        return None
    except json.JSONDecodeError:
        st.error("Ошибка в JSON файле")
        return None

def save_guide_data(data):
    """Сохранить данные в guide.json"""
    try:
        data['lastUpdated'] = datetime.now().isoformat() + 'Z'
        with open(GUIDE_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Ошибка при сохранении: {e}")
        return False

def validate_protocol(protocol):
    """Валидация протокола"""
    required_fields = ['id', 'title', 'type', 'region', 'kv', 'mas', 'description']
    missing = [f for f in required_fields if not protocol.get(f)]
    return missing

def save_uploaded_image(uploaded_file, protocol_id):
    """Сохранить загруженное изображение"""
    if uploaded_file is None:
        return None
    
    try:
        # Генерируем имя файла
        file_ext = os.path.splitext(uploaded_file.name)[1]
        filename = f"{protocol_id}{file_ext}"
        filepath = os.path.join(IMAGES_DIR, filename)
        
        # Сохраняем файл
        with open(filepath, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        return f"guide_images/{filename}"
    except Exception as e:
        st.error(f"Ошибка при сохранении изображения: {e}")
        return None

def delete_protocol_image(image_url):
    """Удалить изображение протокола"""
    if image_url:
        try:
            filepath = os.path.join(os.path.dirname(__file__), image_url)
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            st.warning(f"Не удалось удалить изображение: {e}")

def display_protocol_image(image_url):
    """Отобразить изображение протокола"""
    if image_url:
        try:
            image_path = os.path.join(os.path.dirname(__file__), image_url)
            if os.path.exists(image_path):
                st.image(image_path, use_container_width=True, caption="Изображение укладки")
                return True
        except Exception as e:
            st.warning(f"Не удалось загрузить изображение: {e}")
    return False

# ============= ИНТЕРФЕЙС =============

st.title("📋 RadioHelper Guide Editor")
st.markdown("Редактирование медицинских протоколов исследований")

data = load_guide_data()
if data is None:
    st.stop()

# Боковая панель
st.sidebar.header("⚙️ Управление")
action = st.sidebar.radio(
    "Выбери действие:",
    ["📊 Просмотр", "➕ Добавить", "✏️ Редактировать", "🗑️ Удалить", "⚡ Версия"]
)

st.sidebar.divider()
st.sidebar.info(f"""
**Версия:** {data['version']}
**Протоколов:** {len(data['protocols'])}
**Обновлено:** {data.get('lastUpdated', 'N/A')[:10]}
""")

# ============= ПРОСМОТР =============
if action == "📊 Просмотр":
    st.subheader("Список протоколов")
    
    # Фильтры
    col1, col2 = st.columns(2)
    with col1:
        filter_type = st.selectbox(
            "Тип исследования:",
            ["Все", "CT", "RENTGEN"],
            key="view_type"
        )
    with col2:
        filter_region = st.selectbox(
            "Область тела:",
            ["Все", "HEAD", "CHEST", "SPINE", "ABDOMEN", "PELVIS", "LIMBS", "ALL"],
            key="view_region"
        )
    
    # Фильтрация
    protocols = data['protocols']
    if filter_type != "Все":
        protocols = [p for p in protocols if p['type'] == filter_type]
    if filter_region != "Все":
        protocols = [p for p in protocols if p['region'] == filter_region]
    
    # Таблица
    if protocols:
        table_data = []
        for p in protocols:
            table_data.append({
                "ID": p['id'],
                "Название": p['title'],
                "Тип": p['type'],
                "Область": p['region'],
                "kV": p['kv'],
                "mAs": p['mas'],
                "🖼️": "✅" if p.get('imageUrl') else "❌",
                "Описание": p['description'][:50] + "..." if len(p['description']) > 50 else p['description']
            })
        
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, height=400)
        st.success(f"Всего: {len(protocols)} протоколов")
        
        # Просмотр деталей выбранного протокола
        selected_id = st.selectbox("Просмотреть детали протокола:", [p['id'] for p in protocols], key="view_detail")
        if selected_id:
            protocol = next(p for p in protocols if p['id'] == selected_id)
            st.subheader(f"📋 {protocol['title']}")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.write(f"**ID:** `{protocol['id']}`")
                st.write(f"**Тип:** {protocol['type']}")
                st.write(f"**Область:** {protocol['region']}")
                st.write(f"**kV:** {protocol['kv']}")
                st.write(f"**mAs:** {protocol['mas']}")
            
            with col2:
                st.write(f"**Описание:**")
                st.write(protocol['description'])
            
            if protocol.get('imageUrl'):
                display_protocol_image(protocol['imageUrl'])
    else:
        st.warning("Протоколы не найдены")

# ============= ДОБАВИТЬ =============
elif action == "➕ Добавить":
    st.subheader("Добавить новый протокол")
    
    with st.form("add_protocol_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            protocol_id = st.text_input(
                "ID (уникальный, без пробелов)",
                placeholder="ct_head_standard",
                help="Например: ct_abdomen_contrast или rentgen_chest_pa"
            )
            title = st.text_input(
                "Название",
                placeholder="КТ головного мозга",
                help="Полное название протокола"
            )
            protocol_type = st.selectbox("Тип исследования", ["CT", "RENTGEN"])
            region = st.selectbox(
                "Область тела",
                ["HEAD", "CHEST", "SPINE", "ABDOMEN", "PELVIS", "LIMBS", "ALL"]
            )
        
        with col2:
            kv = st.text_input(
                "kV (напряжение)",
                placeholder="120 кВ",
                help="Например: 70-80 кВ или 120 кВ"
            )
            mas = st.text_input(
                "mAs (экспозиция)",
                placeholder="200-300 мАс",
                help="Например: 30-50 мАс или 200-300 мАс"
            )
        
        description = st.text_area(
            "Описание укладки",
            placeholder="Подробное описание техники выполнения...",
            height=150
        )
        
        st.markdown("**Изображение укладки (необязательно)**")
        uploaded_image = st.file_uploader(
            "Загрузи изображение",
            type=['png', 'jpg', 'jpeg', 'gif'],
            key="add_image"
        )
        
        if st.form_submit_button("✅ Добавить протокол", use_container_width=True):
            if not protocol_id:
                st.error("ID обязателен")
            elif any(p['id'] == protocol_id for p in data['protocols']):
                st.error(f"❌ Протокол с ID '{protocol_id}' уже существует")
            else:
                new_protocol = {
                    "id": protocol_id,
                    "title": title,
                    "type": protocol_type,
                    "region": region,
                    "kv": kv,
                    "mas": mas,
                    "description": description,
                    "imageUrl": None
                }
                
                errors = validate_protocol(new_protocol)
                if errors:
                    st.error(f"Ошибка: отсутствуют поля {errors}")
                else:
                    # Сохраняем изображение если оно загружено
                    if uploaded_image:
                        image_url = save_uploaded_image(uploaded_image, protocol_id)
                        new_protocol['imageUrl'] = image_url
                    
                    data['protocols'].append(new_protocol)
                    if save_guide_data(data):
                        st.success("✅ Протокол добавлен успешно!")
                        st.rerun()
                    else:
                        st.error("Ошибка при сохранении")

# ============= РЕДАКТИРОВАТЬ =============
elif action == "✏️ Редактировать":
    st.subheader("Редактировать протокол")
    
    protocol_ids = [p['id'] for p in data['protocols']]
    selected_id = st.selectbox("Выбери протокол:", protocol_ids)
    
    protocol = next((p for p in data['protocols'] if p['id'] == selected_id), None)
    
    if protocol:
        with st.form("edit_protocol_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("Название", value=protocol['title'])
                protocol_type = st.selectbox(
                    "Тип исследования",
                    ["CT", "RENTGEN"],
                    index=0 if protocol['type'] == "CT" else 1
                )
                region = st.selectbox(
                    "Область тела",
                    ["HEAD", "CHEST", "SPINE", "ABDOMEN", "PELVIS", "LIMBS", "ALL"],
                    index=["HEAD", "CHEST", "SPINE", "ABDOMEN", "PELVIS", "LIMBS", "ALL"].index(protocol['region'])
                )
            
            with col2:
                kv = st.text_input("kV (напряжение)", value=protocol['kv'])
                mas = st.text_input("mAs (экспозиция)", value=protocol['mas'])
            
            description = st.text_area("Описание укладки", value=protocol['description'], height=150)
            
            st.markdown("**Изображение укладки**")
            if protocol.get('imageUrl'):
                st.success("✅ Изображение загружено")
                display_protocol_image(protocol['imageUrl'])
                if st.checkbox("Заменить изображение", key="replace_image"):
                    uploaded_image = st.file_uploader(
                        "Загрузи новое изображение",
                        type=['png', 'jpg', 'jpeg', 'gif'],
                        key="edit_image"
                    )
                else:
                    uploaded_image = None
            else:
                st.info("❌ Изображение не загружено")
                uploaded_image = st.file_uploader(
                    "Загрузи изображение",
                    type=['png', 'jpg', 'jpeg', 'gif'],
                    key="edit_image"
                )
            
            col_submit, col_delete = st.columns(2)
            
            with col_submit:
                if st.form_submit_button("💾 Сохранить", use_container_width=True):
                    protocol.update({
                        'title': title,
                        'type': protocol_type,
                        'region': region,
                        'kv': kv,
                        'mas': mas,
                        'description': description
                    })
                    
                    # Сохраняем изображение если оно загружено
                    if uploaded_image:
                        # Удаляем старое изображение если оно есть
                        if protocol.get('imageUrl'):
                            delete_protocol_image(protocol['imageUrl'])
                        # Сохраняем новое
                        image_url = save_uploaded_image(uploaded_image, protocol['id'])
                        protocol['imageUrl'] = image_url
                    
                    if save_guide_data(data):
                        st.success("✅ Протокол обновлен!")
                        st.rerun()
                    else:
                        st.error("Ошибка при сохранении")
            
            with col_delete:
                if st.form_submit_button("🗑️ Удалить", use_container_width=True, type="secondary"):
                    delete_protocol_image(protocol.get('imageUrl'))
                    data['protocols'] = [p for p in data['protocols'] if p['id'] != selected_id]
                    if save_guide_data(data):
                        st.success("✅ Протокол удалён!")
                        st.rerun()

# ============= УДАЛИТЬ =============
elif action == "🗑️ Удалить":
    st.subheader("Удалить протокол")
    
    protocol_ids = [p['id'] for p in data['protocols']]
    selected_id = st.selectbox("Выбери протокол для удаления:", protocol_ids)
    
    protocol = next((p for p in data['protocols'] if p['id'] == selected_id), None)
    
    if protocol:
        st.warning(f"⚠️ Вы собираетесь удалить: **{protocol['title']}**")
        st.info(f"ID: `{protocol['id']}` | Тип: {protocol['type']} | Область: {protocol['region']}")
        
        if st.button("🗑️ Подтвердить удаление", type="primary", use_container_width=True):
            delete_protocol_image(protocol.get('imageUrl'))
            data['protocols'] = [p for p in data['protocols'] if p['id'] != selected_id]
            if save_guide_data(data):
                st.success("✅ Протокол удалён успешно!")
                st.rerun()

# ============= ВЕРСИЯ =============
elif action == "⚡ Версия":
    st.subheader("Управление версией")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Текущая версия", data['version'])
        st.metric("Протоколов", len(data['protocols']))
    
    with col2:
        new_version = st.text_input(
            "Новая версия",
            value=str(data['version']),
            placeholder="2.0"
        )
        
        if st.button("✅ Обновить версию", use_container_width=True):
            try:
                data['version'] = float(new_version) if '.' in new_version else int(new_version)
                if save_guide_data(data):
                    st.success(f"✅ Версия обновлена на {data['version']}")
                    st.rerun()
            except ValueError:
                st.error("Некорректный формат версии")
    
    st.divider()
    st.subheader("📥 Экспорт / 📤 Импорт")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        st.download_button(
            label="📥 Скачать guide.json",
            data=json_str,
            file_name="guide.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        uploaded_file = st.file_uploader("📤 Загрузить guide.json", type=['json'])
        if uploaded_file:
            try:
                imported_data = json.load(uploaded_file)
                if st.button("✅ Импортировать", use_container_width=True):
                    with open(GUIDE_JSON_PATH, 'w', encoding='utf-8') as f:
                        json.dump(imported_data, f, ensure_ascii=False, indent=2)
                    st.success("✅ Данные импортированы!")
                    st.rerun()
            except json.JSONDecodeError:
                st.error("❌ Некорректный JSON файл")
    
    with col3:
        if st.button("🔄 Перезагрузить", use_container_width=True):
            st.rerun()

# ============= FOOTER =============
st.divider()
st.markdown("""
---
**RadioHelper Guide Editor** | Версия: 1.0 | [Документация](https://github.com/radiohelper)

💡 **Совет:** После изменений загрузи файл на GitHub через git commit/push
""")
