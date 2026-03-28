# Django REST Framework проект с админкой
# Описание: Полноценный Django проект с REST API и админ-панелью

## Быстрый старт

### Вариант 1: Docker (рекомендуется)
```bash
# Сборка и запуск
docker-compose up --build

# Или если нет docker-compose:
docker build -t django-api .
docker run -p 8000:8000 django-api
```

После запуска:
- Админ-панель: http://localhost:8000/admin/
- REST API: http://localhost:8000/api/
- API корневая документация (если включена): http://localhost:8000/api/docs/

Суперпользователь:
```bash
docker-compose exec web python manage.py createsuperuser
```

### Вариант 2: Локальный запуск (без Docker)

1. Создайте виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Примените миграции:
```bash
python manage.py migrate
python manage.py createsuperuser
```

4. Запустите сервер:
```bash
python manage.py runserver
```

## Структура проекта

```
django_project/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
├── .env.example
├── README.md
└── project/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
└── api/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── migrations/
```

## Настройка

### Переменные окружения (для продакшена)
Скопируйте `.env.example` в `.env` и настройте:
- `SECRET_KEY` — сгенерируйте через `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
- `DEBUG=0` — для продакшена
- `ALLOWED_HOSTS` — домены/IP

### Расширения API
Проект использует:
- Django REST Framework (полный API)
- browsable API включен
- пагинация
- кэширование
- CORS поддерживается

## Примеры API

### Create item (POST)
```bash
curl -X POST http://localhost:8000/api/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Example", "description": "Test item"}'
```

### List items (GET)
```bash
curl http://localhost:8000/api/items/
```

## Админ-панель
Зайдите на http://localhost:8000/admin/ с суперпользователем.
Все модели автоматически добавляются в админку.

## Дальнейшие шаги

1. **Настройте модели** в `api/models.py` под свои нужды (модели уже созданы - Item и Category)
2. **Создайте сериализаторы** в `api/serializers.py` (если меняете модели)
3. **Настройте ViewSets** в `api/views.py` под свою логику
4. **Добавьте роуты** в `api/urls.py` если нужны кастомные эндпоинты
5. **Примените миграции**:
   ```bash
   python manage.py makemigrations api
   python manage.py migrate
   ```
6. **Создайте суперпользователя**:
   ```bash
   python manage.py createsuperuser
   ```
7. **Запустите сервер**:
   ```bash
   python manage.py runserver
   ```

## Расширение функциональности

### Добавление новой модели
1. Добавьте класс модели в `api/models.py`
2. Создайте сериализатор в `api/serializers.py`
3. Создайте ViewSet в `api/views.py`
4. Зарегистрируйте в `api/urls.py`:
   ```python
   router.register(r'yourmodel', views.YourModelViewSet)
   ```

### Кастомные эндпоинты (actions)
В ViewSet добавьте декоратор:
```python
@action(detail=False, methods=['get'])
def custom_action(self, request):
    # ваш код
    return Response(data)
```
Эндпоинт будет доступен как `/api/yourendpoint/custom_action/`

### Аутентификация
- SessionAuthentication (браузер, browsable API)
- TokenAuthentication (токены для мобильных/иностранных клиентов)
- JWT (SimpleJWT) - для SPA и мобильных приложений

### Настройка прав доступа
Используйте классы permissions:
```python
from rest_framework import permissions

class MyViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
```

### Пагинация
Измените в settings.py:
```python
REST_FRAMEWORK = {
    'PAGE_SIZE': 50,  # вместо 20
}
```

### Фильтрация
Фильтры уже настроены (DjangoFilterBackend, SearchFilter, OrderingFilter).
Добавьте в ViewSet:
```python
filter_fields = ['field1', 'field2']  # точные совпадения
search_fields = ['name', 'description']  # поиск по частичному совпадению
ordering_fields = ['created_at', 'price']  # сортировка
```

## Структура проекта

```
django_project/
├── Dockerfile                    # сборка контейнера
├── docker-compose.yml            # сервисы: web + postgres
├── docker-compose.sqlite.yml     # упрощенный вариант с SQLite
├── requirements.txt              # Python зависимости
├── manage.py                     # утилита Django
├── .env.example                  # пример переменных окружения
├── .env                          # ваши настройки (в .gitignore)
├── .gitignore
├── setup.sh                      # скрипт для быстрого запуска
├── README.md
├── API_EXAMPLES.md               # примеры запросов
├── project/                      # Django проект
│   ├── settings.py              # настройки (основной файл)
│   ├── urls.py                  # корневые урлы
│   ├── wsgi.py                  # для production
│   └── asgi.py                  # для ASGI ( Channels )
└── api/                         # ваше приложение
    ├── models.py                # модели БД
    ├── serializers.py           # сериализаторы (JSON)
    ├── views.py                 # ViewSets + логика
    ├── urls.py                  # урлы приложения
    ├── admin.py                 # админ-панель
    ├── apps.py                  # конфиг приложения
    └── migrations/              # миграции БД
```

## Лицензия
MIT
