from django.db import models
from django.contrib.auth.models import User


class NavigationItem(models.Model):
    """Пункты верхнего меню"""
    title = models.CharField(max_length=100, verbose_name='Название')
    url = models.SlugField(max_length=100, unique=True, verbose_name='URL (якорь)')
    order = models.IntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительский пункт (для выпадающего меню)'
    )

    class Meta:
        ordering = ['order']
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.title


class SkillCategory(models.Model):
    """Категория навыков (например, Backend, Frontend, DevOps)"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Слаг')
    description = models.TextField(blank=True, verbose_name='Описание категории')
    order = models.IntegerField(default=0, verbose_name='Порядок')
    icon_class = models.CharField(max_length=100, blank=True, verbose_name='CSS класс иконки (FontAwesome)')

    class Meta:
        ordering = ['order']
        verbose_name = 'Категория навыков'
        verbose_name_plural = 'Категории навыков'

    def __str__(self):
        return self.name


class Skill(models.Model):
    """Конкретный навык"""
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.CASCADE,
        related_name='skills',
        verbose_name='Категория'
    )
    name = models.CharField(max_length=200, verbose_name='Название навыка')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='skills/', blank=True, null=True, verbose_name='Изображение/Иконка')
    proficiency = models.IntegerField(default=80, verbose_name='Уровень владения (%)', help_text='0-100')
    order = models.IntegerField(default=0, verbose_name='Порядок в категории')
    is_featured = models.BooleanField(default=False, verbose_name='Показывать в featured')

    class Meta:
        ordering = ['category__order', 'order']
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class HeroSection(models.Model):
    """Главный экран (hero)"""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    subtitle = models.CharField(max_length=300, blank=True, verbose_name='Подзаголовок')
    description = models.TextField(blank=True, verbose_name='Описание')
    background_image = models.ImageField(upload_to='hero/', blank=True, null=True, verbose_name='Фоновое изображение')
    cta_text = models.CharField(max_length=100, default='Узнать больше', verbose_name='Текст кнопки')
    cta_url = models.CharField(max_length=100, default='#skills', verbose_name='Ссылка кнопки (якорь)')
    is_active = models.BooleanField(default=True, verbose_name='Активный')

    class Meta:
        verbose_name = 'Hero секция'
        verbose_name_plural = 'Hero секция'

    def __str__(self):
        return "Главный экран"


class AboutSection(models.Model):
    """Секция 'Обо мне'"""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание (HTML)')
    image = models.ImageField(upload_to='about/', blank=True, null=True, verbose_name='Фотография/изображение')
    is_active = models.BooleanField(default=True, verbose_name='Активная')

    class Meta:
        verbose_name = 'Секция "Обо мне"'
        verbose_name_plural = 'Секция "Обо мне"'

    def __str__(self):
        return "Обо мне"


class ContactSection(models.Model):
    """Секция контактов"""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    email = models.EmailField(blank=True, verbose_name='Email')
    phone = models.CharField(max_length=50, blank=True, verbose_name='Телефон')
    telegram = models.CharField(max_length=100, blank=True, verbose_name='Telegram (username)')
    whatsapp = models.CharField(max_length=100, blank=True, verbose_name='WhatsApp')
    linkedin = models.URLField(blank=True, verbose_name='LinkedIn')
    github = models.URLField(blank=True, verbose_name='GitHub')
    location = models.CharField(max_length=200, blank=True, verbose_name='Местоположение')
    is_active = models.BooleanField(default=True, verbose_name='Активная')

    class Meta:
        verbose_name = 'Секция контактов'
        verbose_name_plural = 'Секция контактов'

    def __str__(self):
        return "Контакты"


class SiteSettings(models.Model):
    """Глобальные настройки сайта"""
    site_name = models.CharField(max_length=200, default='Портфолио', verbose_name='Название сайта')
    meta_description = models.TextField(blank=True, verbose_name='Meta description')
    logo = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name='Логотип')
    favicon = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name='Фавикон')
    primary_color = models.CharField(max_length=7, default='#007bff', verbose_name='Основной цвет')
    secondary_color = models.CharField(max_length=7, default='#6c757d', verbose_name='Вторичный цвет')
    custom_css = models.TextField(blank=True, verbose_name='Кастомный CSS')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return f"Настройки: {self.site_name}"