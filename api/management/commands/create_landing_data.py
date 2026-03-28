from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import (
    NavigationItem, SkillCategory, Skill,
    HeroSection, AboutSection, ContactSection,
    SiteSettings
)


class Command(BaseCommand):
    help = 'Создает тестовые данные для лендинг-портфолио'

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
            NavigationItem.objects.all().delete()
            Skill.objects.all().delete()
            SkillCategory.objects.all().delete()
            HeroSection.objects.all().delete()
            AboutSection.objects.all().delete()
            ContactSection.objects.all().delete()
            SiteSettings.objects.all().delete()
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
                'site_name': 'Моё Портфолио',
                'meta_description': 'Портфолио разработчика',
                'primary_color': '#007bff',
                'secondary_color': '#6c757d',
            }
        )
        if created:
            self.stdout.write('Созданы настройки сайта')
        else:
            self.stdout.write('Настройки уже есть')

        # Меню навигации
        nav_items = [
            {'title': 'Главная', 'url': 'home', 'order': 1},
            {'title': 'Навыки', 'url': 'skills', 'order': 2},
            {'title': 'Обо мне', 'url': 'about', 'order': 3},
            {'title': 'Контакты', 'url': 'contact', 'order': 4},
        ]
        for item in nav_items:
            NavigationItem.objects.get_or_create(
                url=item['url'],
                defaults={**item, 'is_active': True}
            )
        self.stdout.write('Создано меню навигации')

        # Категории навыков
        categories = [
            {'name': 'Backend', 'slug': 'backend', 'description': 'Серверная разработка', 'order': 1, 'icon_class': 'fa-server'},
            {'name': 'Frontend', 'slug': 'frontend', 'description': 'Клиентская разработка', 'order': 2, 'icon_class': 'fa-code'},
            {'name': 'DevOps', 'slug': 'devops', 'description': 'Инфраструктура и CI/CD', 'order': 3, 'icon_class': 'fa-cogs'},
            {'name': 'Боты', 'slug': 'bots', 'description': 'Telegram, Discord боты', 'order': 4, 'icon_class': 'fa-robot'},
        ]
        cat_objs = {}
        for cat_data in categories:
            cat, _ = SkillCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            cat_objs[cat_data['slug']] = cat
        self.stdout.write('Создано категорий навыков: 4')

        # Навыки
        skills_data = [
            {'category': 'backend', 'name': 'Python', 'description': 'Основной язык', 'proficiency': 95, 'order': 1, 'is_featured': True},
            {'category': 'backend', 'name': 'Django', 'description': 'Веб-фреймворк', 'proficiency': 90, 'order': 2, 'is_featured': True},
            {'category': 'backend', 'name': 'FastAPI', 'description': 'Асинхронный фреймворк', 'proficiency': 85, 'order': 3, 'is_featured': False},
            {'category': 'frontend', 'name': 'HTML/CSS', 'description': 'Вёрстка, адаптивность', 'proficiency': 80, 'order': 1, 'is_featured': False},
            {'category': 'frontend', 'name': 'JavaScript', 'description': 'Базовый JS', 'proficiency': 75, 'order': 2, 'is_featured': False},
            {'category': 'devops', 'name': 'Docker', 'description': 'Контейнеризация', 'proficiency': 85, 'order': 1, 'is_featured': True},
            {'category': 'devops', 'name': 'Git', 'description': 'Контроль версий', 'proficiency': 90, 'order': 2, 'is_featured': False},
            {'category': 'bots', 'name': 'Telegram Bot', 'description': 'Боты на python-telegram-bot', 'proficiency': 90, 'order': 1, 'is_featured': True},
            {'category': 'bots', 'name': 'AI интеграция', 'description': 'OpenRouter, Gemini, локальные модели', 'proficiency': 85, 'order': 2, 'is_featured': True},
        ]
        for s in skills_data:
            Skill.objects.get_or_create(
                category=cat_objs[s['category']],
                name=s['name'],
                defaults={**s}
            )
        self.stdout.write('Создано навыков: 9')

        # Hero секция
        hero, _ = HeroSection.objects.get_or_create(
            defaults={
                'title': 'Привет, яPython Developer',
                'subtitle': 'Создаю ботов и веб-приложения',
                'description': 'Специализируюсь на разработке Telegram-ботов, REST API и автоматизации. Использую современные технологии и подходы.',
                'cta_text': 'Узнать больше',
                'cta_url': '#skills',
                'is_active': True,
            }
        )
        self.stdout.write('Hero секция создана')

        # About секция
        about, _ = AboutSection.objects.get_or_create(
            defaults={
                'title': 'Обо мне',
                'content': '<p>Я — опытный Python-разработчик с фокусом на backend, ботостроение и DevOps.</p><p>Работаю с Django, FastAPI, Docker, пишу Telegram-ботов с AI-интеграцией.</p>',
                'is_active': True,
            }
        )
        self.stdout.write('About секция создана')

        # Contact секция
        contact, _ = ContactSection.objects.get_or_create(
            defaults={
                'title': 'Контакты',
                'email': 'example@email.com',
                'telegram': '@username',
                'github': 'https://github.com/werewolf85',
                'location': 'Вьетнам, Нячанг',
                'is_active': True,
            }
        )
        self.stdout.write('Contact секция создана')

        self.stdout.write(self.style.SUCCESS('✅ Все данные созданы!'))
        self.stdout.write('Перейди на http://localhost:8000/ чтобы увидеть лендинг')
        self.stdout.write('Админка: http://localhost:8000/admin/ (admin/admin123)')