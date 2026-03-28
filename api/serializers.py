from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    NavigationItem, SkillCategory, Skill,
    HeroSection, AboutSection, ContactSection,
    SiteSettings
)


class NavigationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavigationItem
        fields = ['id', 'title', 'url', 'order', 'is_active', 'parent']


class SkillCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillCategory
        fields = ['id', 'name', 'slug', 'description', 'order', 'icon_class']


class SkillSerializer(serializers.ModelSerializer):
    category = SkillCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=SkillCategory.objects.all(),
        source='category',
        write_only=True
    )
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = [
            'id', 'category', 'category_id', 'name', 'description',
            'image', 'image_url', 'proficiency', 'order', 'is_featured'
        ]

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class HeroSectionSerializer(serializers.ModelSerializer):
    background_url = serializers.SerializerMethodField()

    class Meta:
        model = HeroSection
        fields = [
            'id', 'title', 'subtitle', 'description',
            'background_image', 'background_url',
            'cta_text', 'cta_url', 'is_active'
        ]

    def get_background_url(self, obj):
        if obj.background_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.background_image.url)
            return obj.background_image.url
        return None


class AboutSectionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = AboutSection
        fields = ['id', 'title', 'content', 'image', 'image_url', 'is_active']

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class ContactSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSection
        fields = [
            'id', 'title', 'email', 'phone', 'telegram',
            'whatsapp', 'linkedin', 'github', 'location', 'is_active'
        ]


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = [
            'id', 'site_name', 'meta_description',
            'logo', 'favicon',
            'primary_color', 'secondary_color',
            'custom_css', 'updated_at'
        ]
        read_only_fields = ['updated_at']