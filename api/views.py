from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.generic import TemplateView
from .models import (
    NavigationItem, SkillCategory, Skill,
    HeroSection, AboutSection, ContactSection,
    SiteSettings
)
from .serializers import (
    NavigationItemSerializer, SkillCategorySerializer, SkillSerializer,
    HeroSectionSerializer, AboutSectionSerializer, ContactSectionSerializer,
    SiteSettingsSerializer
)


class NavigationItemViewSet(viewsets.ModelViewSet):
    """Управление меню (админ)"""
    queryset = NavigationItem.objects.all()
    serializer_class = NavigationItemSerializer
    permission_classes = [permissions.IsAdminUser]
    ordering = ['order']


class SkillCategoryViewSet(viewsets.ModelViewSet):
    """Категории навыков"""
    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    ordering = ['order']


class SkillViewSet(viewsets.ModelViewSet):
    """Навыки"""
    queryset = Skill.objects.select_related('category').all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['category', 'is_featured']
    ordering_fields = ['order', 'proficiency']
    ordering = ['category__order', 'order']

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Популярные/featured навыки"""
        featured = self.get_queryset().filter(is_featured=True)
        page = self.paginate_queryset(featured)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)


class HeroSectionViewSet(viewsets.ModelViewSet):
    """Главный экран (hero)"""
    queryset = HeroSection.objects.filter(is_active=True)
    serializer_class = HeroSectionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        # Всегда возвращаем первый активный
        hero = self.get_queryset().first()
        if hero:
            serializer = self.get_serializer(hero)
            return Response(serializer.data)
        return Response({}, status=204)


class AboutSectionViewSet(viewsets.ModelViewSet):
    """Секция 'Обо мне'"""
    queryset = AboutSection.objects.filter(is_active=True)
    serializer_class = AboutSectionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        about = self.get_queryset().first()
        if about:
            serializer = self.get_serializer(about)
            return Response(serializer.data)
        return Response({}, status=204)


class ContactSectionViewSet(viewsets.ModelViewSet):
    """Секция контактов"""
    queryset = ContactSection.objects.filter(is_active=True)
    serializer_class = ContactSectionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        contact = self.get_queryset().first()
        if contact:
            serializer = self.get_serializer(contact)
            return Response(serializer.data)
        return Response({}, status=204)


class SiteSettingsViewSet(viewsets.ModelViewSet):
    """Настройки сайта (singleton)"""
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [permissions.IsAdminUser]

    def list(self, request, *args, **kwargs):
        settings = SiteSettings.objects.first()
        if settings:
            serializer = self.get_serializer(settings)
            return Response(serializer.data)
        return Response({}, status=204)

    def create(self, request, *args, **kwargs):
        if SiteSettings.objects.exists():
            return Response({'error': 'Настройки уже существуют. Используйте PUT.'}, status=400)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        settings = SiteSettings.objects.first()
        if not settings:
            return Response({'error': 'Настройки не найдены. Создайте через POST.'}, status=404)
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs, instance=settings)


class LandingPageView(TemplateView):
    """Публичная страница лендинга (index)"""
    template_name = 'api/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Все данные для страницы
        context['navigation'] = NavigationItem.objects.filter(is_active=True).order_by('order')
        context['hero'] = HeroSection.objects.filter(is_active=True).first()
        context['about'] = AboutSection.objects.filter(is_active=True).first()
        context['contact'] = ContactSection.objects.filter(is_active=True).first()
        context['settings'] = SiteSettings.objects.first()
        # Навыки: категории со вложенными навыками
        context['categories'] = SkillCategory.objects.all().order_by('order')
        # Собираем навыки по категориям
        skills_by_category = {}
        for cat in context['categories']:
            skills_by_category[cat.id] = cat.skills.all().order_by('order')
        context['skills_by_category'] = skills_by_category
        return context