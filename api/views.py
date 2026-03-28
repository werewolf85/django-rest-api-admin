from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import TemplateView
from .models import Item, Category, Page, Image, SiteSettings
from .serializers import (
    ItemSerializer, CategorySerializer, UserSerializer,
    PageSerializer, ImageSerializer, SiteSettingsSerializer
)
from django.contrib.auth.models import User


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Только владелец может изменять объект."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user or obj.owner is None


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'owner']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Item.objects.select_related('owner').all()
        is_active = self.request.query_params.get('active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        return queryset

    @action(detail=False, methods=['get'])
    def my(self, request):
        items = self.get_queryset().filter(owner=request.user)
        page = self.paginate_queryset(items)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        item = self.get_object()
        item.is_active = True
        item.save()
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        item = self.get_object()
        item.is_active = False
        item.save()
        serializer = self.get_serializer(item)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'parent']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'order']
    ordering = ['order', 'name']

    @action(detail=False, methods=['get'])
    def tree(self, request):
        queryset = self.get_queryset().filter(parent__isnull=True, is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def descendants(self, request, pk=None):
        category = self.get_object()
        def get_all_descendants(cat):
            children = cat.children.filter(is_active=True)
            descendants = list(children)
            for child in children:
                descendants.extend(get_all_descendants(child))
            return descendants
        descendants = get_all_descendants(category)
        serializer = self.get_serializer(descendants, many=True)
        return Response(serializer.data)


class PageViewSet(viewsets.ModelViewSet):
    """Страницы (CRUD)"""
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created_at']
    ordering = ['-created_at']

    @action(detail=True, methods=['get'])
    def published(self, request, pk=None):
        """Публичная страница с изображениями (JSON)"""
        page = self.get_object()
        if not page.is_active:
            return Response({'error': 'Страница не активна'}, status=404)
        images = page.images.filter(is_active=True).order_by('order')
        image_serializer = ImageSerializer(images, many=True, context={'request': request})
        data = {
            'page': PageSerializer(page).data,
            'images': image_serializer.data
        }
        return Response(data)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'created_at']
    ordering = ['order', '-created_at']

    def get_queryset(self):
        page_id = self.request.query_params.get('page_id')
        if page_id:
            return self.queryset.filter(page_id=page_id)
        return self.queryset


class SiteSettingsViewSet(viewsets.ModelViewSet):
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


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class PagePublicView(TemplateView):
    """Публичная страница (HTML)"""
    template_name = 'api/page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs.get('slug')
        try:
            page = Page.objects.get(slug=slug, is_active=True)
            images = page.images.filter(is_active=True).order_by('order')
            settings = SiteSettings.objects.first()
            context['page'] = page
            context['images'] = images
            context['settings'] = settings
        except Page.DoesNotExist:
            context['page'] = None
            context['images'] = []
            context['settings'] = None
        return context
