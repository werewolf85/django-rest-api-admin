from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'navigation', views.NavigationItemViewSet)
router.register(r'skills', views.SkillViewSet)
router.register(r'skill-categories', views.SkillCategoryViewSet)
router.register(r'hero', views.HeroSectionViewSet)
router.register(r'about', views.AboutSectionViewSet)
router.register(r'contact', views.ContactSectionViewSet)
router.register(r'settings', views.SiteSettingsViewSet, basename='settings')

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing'),
    path('api/', include(router.urls)),
]