# Используем официальный Python образ
FROM python:3.13-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем .env если есть (но .env в .gitignore лучше)
COPY .env* .env 2>/dev/null || true

# Копируем все файлы проекта
COPY . .

# Собираем статику
RUN python manage.py collectstatic --noinput

# Экспонируем порт
EXPOSE 8000

# Запускаем через Gunicorn (для продакшена)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi:application"]

# Для разработки можно использовать:
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
