from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Item, Category, Page, Image, SiteSettings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('date_joined',)


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class SiteSettingsSerializer(serializers.ModelSerializer):
    """Сериализатор настроек сайта"""
    class Meta:
        model = SiteSettings
        fields = [
            'id', 'site_name', 'theme', 'primary_color', 'secondary_color',
            'accent_color', 'logo', 'favicon', 'custom_css', 'updated_at'
        ]
        read_only_fields = ['updated_at']


class PageSerializer(serializers.ModelSerializer):
    """Сериализатор страниц"""
    class Meta:
        model = Page
        fields = [
            'id', 'title', 'slug', 'description', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор файлов"""
    page = serializers.PrimaryKeyRelatedField(
        queryset=Page.objects.all(),
        required=False,
        allow_null=True
    )
    file_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Image
        fields = [
            'id', 'page', 'title', 'file', 'file_url', 'mime_type',
            'order', 'description', 'is_active', 'created_at'
        ]
        read_only_fields = ['created_at', 'file_url', 'mime_type']

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class ItemSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='owner',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Item
        fields = [
            'id', 'name', 'description', 'price', 'is_active',
            'owner', 'owner_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной")
        return value


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'parent', 'parent_id',
            'children', 'order', 'is_active'
        ]
        read_only_fields = ['slug']

    def get_children(self, obj):
        children = obj.children.filter(is_active=True)
        return CategorySerializer(children, many=True, context=self.context).data

    def validate_name(self, value):
        if Category.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Категория с таким именем уже существует")
        return value
