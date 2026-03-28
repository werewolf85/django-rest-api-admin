#!/bin/bash
# Быстрый запуск Django проекта без Docker
# Требует: python3, pip

set -e

echo "=== Django Project Setup ==="

# Проверяем зависимости
if ! command -v python3 &> /dev/null; then
    echo "Ошибка: python3 не найден. Установите Python 3.11+"
    exit 1
fi

# Создаем virtualenv если его нет
if [ ! -d "venv" ]; then
    echo "Создаю виртуальное окружение..."
    python3 -m venv venv
fi

# Активируем venv и устанавливаем зависимости
echo "Устанавливаю зависимости..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Создаем .env если его нет
if [ ! -f ".env" ]; then
    echo "Создаю .env файл..."
    cp .env.example .env
    # Генерируем секретный ключ
    SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
    sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    echo "Сгенерирован SECRET_KEY в .env"
fi

# Применяем миграции
echo "Применяю миграции..."
python manage.py migrate --noinput

# Создаем тестовые данные (опционально, можно пропустить)
if [ ! -f ".initialized" ]; then
    echo "Создаю тестовые данные..."
    python manage.py create_default_data
    touch .initialized
fi

echo ""
echo "✅ Готово!"
echo ""
echo "Запуск сервера:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Админка: http://localhost:8000/admin/"
echo "  суперпользователь: admin / admin123"
echo ""
echo "API: http://localhost:8000/api/"
echo "Создать суперпользователя: python manage.py createsuperuser"
echo ""
echo "Для деактивации тестовых данных: rm .initialized && python manage.py create_default_data"
