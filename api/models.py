from django.db import models
from django.contrib.auth.models import User


class Page(models.Model):
    """Страница для отображения контента"""
    title = models.CharField(max_length=200, verbose_name='Заголовок страницы')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL slug')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активная')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлена')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

    def __str__(self):
        return self.title


class Image(models.Model):
    """Файл (изображение или любой файл), привязанный к странице"""
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Страница',
        null=True,
        blank=True
    )
    title = models.CharField(max_length=200, verbose_name='Название')
    file = models.FileField(upload_to='uploads/', verbose_name='Файл')
    # Если загружаются изображения, можно сохранять их MIME-тип для отображения
    mime_type = models.CharField(max_length=100, blank=True, verbose_name='MIME тип')
    order = models.IntegerField(default=0, verbose_name='Порядок')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активное')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Загружено')

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Автоматически определить MIME тип при загрузке
        if self.file and not self.mime_type:
            import mimetypes
            self.mime_type, _ = mimetypes.guess_type(self.file.name)
        super().save(*args, **kwargs)


class SiteSettings(models.Model):
    """Настройки сайта (дизайн, цвета и т.д.)"""
    THEME_CHOICES = [
        ('light', 'Светлая'),
        ('dark', 'Темная'),
        ('custom', 'Кастомная'),
    ]

    site_name = models.CharField(max_length=200, default='Мой сайт', verbose_name='Название сайта')
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='light', verbose_name='Тема')
    primary_color = models.CharField(max_length=7, default='#007bff', verbose_name='Основной цвет (hex)')
    secondary_color = models.CharField(max_length=7, default='#6c757d', verbose_name='Вторительный цвет')
    accent_color = models.CharField(max_length=7, default='#28a745', verbose_name='Акцентный цвет')
    logo = models.FileField(upload_to='site/', blank=True, null=True, verbose_name='Логотип')
    favicon = models.FileField(upload_to='site/', blank=True, null=True, verbose_name='Фавикон')
    custom_css = models.TextField(blank=True, verbose_name='Кастомный CSS')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Настройка сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return f"Настройки: {self.site_name}"

    @property
    def primary_color_rgb(self):
        # Конверт hex в rgb для использования в CSS
        hex = self.primary_color.lstrip('#')
        return f"{int(hex[0:2], 16)}, {int(hex[2:4], 16)}, {int(hex[4:6], 16)}"


# Остальные модели из оригинала (Item, Category) остаются без изменений
class Item(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Владелец',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Элемент'
        verbose_name_plural = 'Элементы'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Слаг')
    description = models.TextField(blank=True, verbose_name='Описание')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительская категория'
    )
    order = models.IntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активная')

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
