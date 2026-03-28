# Примеры использования API

## Аутентификация

### Получить токен (если используете SimpleJWT)
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```
Ответ:
```json
{
  "refresh": "...",
  "access": "..."
}
```

### Использовать токен
```bash
export TOKEN="your-access-token-here"

curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/items/
```

## Items (CRUD)

### Список всех items (публичный доступ)
```bash
curl http://localhost:8000/api/items/
```

### Список с фильтрацией
```bash
# Только активные
curl "http://localhost:8000/api/items/?is_active=true"

# По владельцу
curl "http://localhost:8000/api/items/?owner=1"

# Поиск по названию/описанию
curl "http://localhost:8000/api/items/?search=ноутбук"

# Сортировка
curl "http://localhost:8000/api/items/?ordering=-created_at"
curl "http://localhost:8000/api/items/?ordering=price"
```

### Создание item (требуется аутентификация)
```bash
curl -X POST http://localhost:8000/api/items/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Новый товар",
    "description": "Описание товара",
    "price": 199.99,
    "is_active": true
  }'
```

### Получение конкретного item
```bash
curl http://localhost:8000/api/items/1/
```

### Обновление item
```bash
curl -X PUT http://localhost:8000/api/items/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Обновленное название",
    "description": "Новое описание",
    "price": 299.99,
    "is_active": false
  }'
```

### Частичное обновление (PATCH)
```bash
curl -X PATCH http://localhost:8000/api/items/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"price": 150.00}'
```

### Удаление item
```bash
curl -X DELETE http://localhost:8000/api/items/1/ \
  -H "Authorization: Bearer $TOKEN"
```

### Специальные действия (кастомные actions)
```bash
# Активировать item
curl -X POST http://localhost:8000/api/items/1/activate/ \
  -H "Authorization: Bearer $TOKEN"

# Деактивировать item
curl -X POST http://localhost:8000/api/items/1/deactivate/ \
  -H "Authorization: Bearer $TOKEN"

# Только мои items
curl http://localhost:8000/api/items/my/ \
  -H "Authorization: Bearer $TOKEN"
```

## Categories

### Список категорий
```bash
curl http://localhost:8000/api/categories/
```

### Создание категории
```bash
curl -X POST http://localhost:8000/api/categories/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Новая категория",
    "description": "Описание категории",
    "parent": null,
    "order": 0,
    "is_active": true
  }'
```

### Дерево категорий (только корневые)
```bash
curl http://localhost:8000/api/categories/tree/
```

### Потомки категории
```bash
curl http://localhost:8000/api/categories/1/descendants/
```

## Users (только для админов)

### Список пользователей
```bash
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/users/
```

## Пагинация

По умолчанию 20 элементов на страницу.
Можно изменить через параметр `page_size`:

```bash
curl "http://localhost:8000/api/items/?page=1&page_size=10"
```

## Browsable API

Откройте в браузере http://localhost:8000/api/items/ - вы увидите
веб-интерфейс Django REST Framework для взаимодействия с API.

Для входа нажмите "Log in" в правом верхнем углу и используйте
суперпользователя (admin / admin123).
