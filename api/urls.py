from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'pages', views.PageViewSet)
router.register(r'images', views.ImageViewSet)
router.register(r'settings', views.SiteSettingsViewSet, basename='settings')
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('page/<slug:slug>/', views.PagePublicView.as_view(), name='page-public'),
    path('', include(router.urls)),
]
