from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Category, Page, SiteSettings


class Command(BaseCommand):
    help = 'Создает тестовые данные для разработки'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Удалить все данные и создать заново',
        )

    def handle(self, *args, **options):
        reset = options['reset']

        if reset:
            self.stdout.write('Удаляем существующие данные...')
            Category.objects.all().delete()
            Page.objects.all().delete()
            SiteSettings.objects.all().delete()
            User.objects.filter(is_superuser=False).exclude(username='admin').delete()
            self.stdout.write(self.style.SUCCESS('Данные удалены'))

        # Суперпользователь
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('Создан суперпользователь: admin / admin123'))

        # Настройки сайта
        settings, created = SiteSettings.objects.get_or_create(
            defaults={
                'site_name': 'Мой сайт',
                'theme': 'light',
                'primary_color': '#007bff',
                'secondary_color': '#6c757d',
                'accent_color': '#28a745',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Созданы настройки сайта по умолчанию'))
        else:
            self.stdout.write('Настройки сайта уже существуют')

        # Страницы
        page, created = Page.objects.get_or_create(
            slug='home',
            defaults={
                'title': 'Главная',
                'description': 'Добро пожаловать на мой сайт!',
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Создана страница "Главная" (slug: home)'))
        else:
            self.stdout.write('Страница "home" уже существует')

        # Категории (изначальные)
        categories_data = [
            {'name': 'Электроника', 'slug': 'electronics', 'description': 'Электронные устройства'},
            {'name': 'Книги', 'slug': 'books', 'description': 'Книги и литература'},
            {'name': 'Одежда', 'slug': 'clothing', 'description': 'Одежда и аксессуары'},
            {'name': 'Дом и сад', 'slug': 'home-garden', 'description': 'Товары для дома и сада'},
            {'name': 'Спорт', 'slug': 'sports', 'description': 'Спортивные товары'},
        ]
        created_cats = 0
        for cat_data in categories_data:
            cat, created_flag = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created_flag:
                created_cats += 1
        self.stdout.write(self.style.SUCCESS(f'Создано {created_cats} новых категорий'))

        # Тестовые Items (изначальные)
        from api.models import Item
        admin_user = User.objects.get(username='admin')
        items_data = [
            {'name': 'Ноутбук', 'description': 'Мощный ноутбук для работы', 'price': 999.99, 'owner': admin_user},
            {'name': 'Книга "Django для начинающих"', 'description': 'Подробное руководство', 'price': 29.99, 'owner': admin_user},
            {'name': 'Футболка', 'description': 'Хлопковая футболка', 'price': 15.50, 'owner': admin_user},
            {'name': 'Фонарь', 'description': 'Светодиодный фонарь', 'price': 12.99, 'owner': admin_user},
            {'name': 'Мяч футбольный', 'description': 'Профессиональный мяч', 'price': 45.00, 'owner': admin_user},
        ]
        items_created = 0
        for item_data in items_data:
            item, created_flag = Item.objects.get_or_create(
                name=item_data['name'],
                defaults=item_data
            )
            if created_flag:
                items_created += 1
        self.stdout.write(self.style.SUCCESS(f'Создано {items_created} тестовых товаров'))

        # Итог
        self.stdout.write(self.style.SUCCESS('Все данные созданы!'))
        self.stdout.write('')
        self.stdout.write('Чтобы просмотреть сайт:')
        self.stdout.write('  1. Запустите сервер: python manage.py runserver 0.0.0.0:8000')
        self.stdout.write('  2. Откройте в браузере: http://localhost:8000/page/home/')
        self.stdout.write('  3. Админка: http://localhost:8000/admin/ (admin / admin123)')
        self.stdout.write('')
        self.stdout.write('В админке можно:')
        self.stdout.write('  - Загружать изображения и привязывать к странице "Главная"')
        self.stdout.write('  - Изменять настройки сайта (тему, цвета)')
        self.stdout.write('  - Редактировать страницы, категории, товары')
