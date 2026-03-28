from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    NavigationItem, SkillCategory, Skill,
    HeroSection, AboutSection, ContactSection,
    SiteSettings
)


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(NavigationItem)
class NavigationItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'order', 'is_active', 'parent')
    list_editable = ('order', 'is_active')
    ordering = ['order']
    list_filter = ('is_active', 'parent')


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'icon_class')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency', 'order', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'description')
    ordering = ['category__order', 'order']
    list_editable = ('order', 'proficiency', 'is_featured')


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'cta_text', 'cta_url', 'is_active')
    search_fields = ('title', 'subtitle', 'description')


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    search_fields = ('title',)


@admin.register(ContactSection)
class ContactSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'email', 'phone', 'telegram', 'is_active')


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'primary_color', 'secondary_color', 'updated_at')
    readonly_fields = ('updated_at',)
    fieldsets = (
        ('Основное', {'fields': ('site_name', 'meta_description')}),
        ('Цвета', {'fields': ('primary_color', 'secondary_color')}),
        ('Изображения', {'fields': ('logo', 'favicon'), 'classes': ('collapse',)}),
        ('Дополнительно', {'fields': ('custom_css',), 'classes': ('collapse',)}),
        ('Метаданные', {'fields': ('updated_at',), 'classes': ('collapse',)}),
    )