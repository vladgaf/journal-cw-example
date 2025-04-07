# 🌟 Гостевой журнал с сентимент-анализом

Веб-приложение для сбора отзывов с автоматическим определением эмоциональной окраски текста и админ-панелью для модерации.

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey?logo=flask)](https://flask.palletsprojects.com/)

## ✨ Особенности

- 📝 Добавление отзывов с определением тональности (positive/negative/neutral)
- 📊 Визуализация эмоциональной окраски через цветовые индикаторы
- 🔐 Админ-панель с авторизацией (хранение ключа в конфигурационном файле)
- 🎨 Адаптивный интерфейс с современным дизайном
- 📦 Хранение данных в JSON (без использования СУБД)

## 🛠 Технологии

- **Backend**: Python + Flask
- **Frontend**: HTML5, CSS3, Jinja2
- **Анализ текста**: Le Chat Mistral
- **Хранение данных**: JSON-файлы
- **Безопасность**: Cookies для авторизации

## 🚀 Быстрый старт

### 1. Установка зависимостей
```bash
pip install flask requests
```
### 2. Файл настроек
Находится по пути `config/settings.json`
При первом запуске файл создастся автоматически со следующими данными:
```json
{
    "admin_key": "admin",
    "ai_key": ""
}
```
`admin_key` - ключ доступа к админ-панели
`ai_key` - API-ключ нейросети Le Chat Mistral.\
*При отсутствии API-ключа/ошибке API будут генерироваться случайные оценки эмоциональной окраски*

## 🔍 Как это работает

### 📌 Основной принцип
1. **Добавление отзыва**:
   - Пользователь вводит имя и текст
   - Система отправляет текст в Le chat Mistral для оценки эмоциональной окраски
   - API возвращает оценку (`positive`/`negative`/`neutral`)
   - Отзыв сохраняется в JSON-файле с меткой тональности

2. **Визуализация**:
   - Каждый отзыв отображается в цветной рамке:
     - ✅ Зеленая — положительный
     - ⚠️ Желтая — нейтральный
     - ❌ Красная — отрицательный

3. **Администрирование**:
   - Доступ по секретному ключу из конфига
   - Возможность удалять отзывы
   - Фильтрация по типу тональности

### 📂 Структура данных
Отзывы хранятся в формате:
```json
[
  {
    "id": 1,
    "name": "Анна",
    "text": "Отличный сервис!",
    "sentiment": "positive",
    "timestamp": "2023-05-20 14:30"
  }
]