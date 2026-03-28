from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Item, Category, Page, Image, SiteSettings


# Перерегистрируем User с кастомным Admin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'owner', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'owner')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основное', {
            'fields': ('name', 'description', 'price', 'is_active')
        }),
        ('Владелец', {
            'fields': ('owner',),
            'classes': ('collapse',)
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Сделать активными"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Сделать неактивными"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'order', 'is_active')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Сделать активными"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Сделать неактивными"


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'page', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'page', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('order', '-created_at')
    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('page')


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'theme', 'primary_color', 'updated_at')
    readonly_fields = ('updated_at',)
    fieldsets = (
        ('Основное', {
            'fields': ('site_name', 'theme')
        }),
        ('Цвета', {
            'fields': ('primary_color', 'secondary_color', 'accent_color')
        }),
        ('Изображения', {
            'fields': ('logo', 'favicon'),
            'classes': ('collapse',)
        }),
        ('Дополнительно', {
            'fields': ('custom_css',),
            'classes': ('collapse',)
        }),
        ('Метаданные', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
