from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

import os

from app.models import *

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_api_user=True,
            phone=validated_data['phone']
        )
        return user


class UserChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True,        required=True)
    new_password_confirm = serializers.CharField(
        write_only=True,        required=True)

    class Meta:
        model = User
        fields = ['password', 'new_password', 'new_password_confirm']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        # 1. Проверка совпадения нового пароля и подтверждения
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                {"new_password_confirm": "Пароли не совпадают"}
            )

        # 2. Валидация сложности нового пароля
        try:
            validate_password(attrs['new_password'])
        except ValidationError as e:
            raise serializers.ValidationError(
                {'new_password': list(e.messages)})

        return attrs

    def update(self, instance, validated_data):
        # Этот метод будет вызван во viewset при save()
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'avatar']

    def validate_avatar(self, value):
        # Проверка размера файла (например, не более 2MB)
        max_size = 2 * 1024 * 1024  # 2MB
        if value.size > max_size:
            raise serializers.ValidationError(
                f"Файл слишком большой. Максимальный размер: {max_size//(1024*1024)}MB")

        # Проверка типа файла
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError(
                "Неподдерживаемый формат файла. Используйте JPG, PNG или GIF")

        return value


class SocialMediaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaType
        exclude = ['id']
        extra_kwargs = {
            'type': {'read_only': True},
        }


class SocialMediaSerializer(serializers.ModelSerializer):
    media_type_name = serializers.CharField(
        source='media_type.type', read_only=True)
    days_remaining = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SocialMedia
        exclude = ['id']

    def get_days_remaining(self, obj):
        return (obj.date_to - timezone.now()).days

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method in ('PUT', 'PATCH'):
            if 'target' in data and data['target'] != self.instance.target:
                raise serializers.ValidationError({
                    'target': 'Изменение компании запрещено после создания'
                })

        return data


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ['id']
        extra_kwargs = {
            'slug': {'read_only': True},
        }


class TourForCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        exclude = ['id']


class CompanyFullSerializer(serializers.ModelSerializer):
    social_media = SocialMediaSerializer(
        source='socialmedia_set',  # Указываем обратное отношение
        many=True,
        read_only=True
    )
    tours = TourForCompanySerializer(
        source='tour_set',
        many=True,
        read_only=True
    )

    class Meta:
        model = Company
        exclude = ['id']
        extra_kwargs = {
            'slug': {'read_only': True},
        }


class TourSerializer(serializers.ModelSerializer):
    favourites_count = serializers.SerializerMethodField(read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    company_slug = serializers.CharField(source='company.slug', read_only=True)
    country_name = serializers.CharField(source='country.name', read_only=True)

    def get_favourites_count(self, obj):
        if hasattr(obj, 'favourites_count'):
            return obj.favourites_count
        return obj.favourites_set.count()

    class Meta:
        model = Tour
        exclude = ['id']
        extra_kwargs = {
            'slug': {'read_only': True},
        }


class TourInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourInfo
        exclude = ['id']


class TourTimeSpanSerializer(serializers.ModelSerializer):
    places_released = serializers.SerializerMethodField(read_only=True)

    def get_places_released(self, obj):
        if hasattr(obj, 'places_released'):
            return obj.places_released
        return obj.reservation.count()

    class Meta:
        model = TourTimeSpan
        exclude = ['id']


class ReservationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationStatus
        exclude = ['id']


class TourToReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ['title', 'slug', 'img_preview_url', 'price']


class ReservationSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source='status.status', read_only=True)
    tour = TourToReservationSerializer(source='target.tour', read_only=True)

    class Meta:
        model = Reservation
        exclude = ['customer']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        exclude = ['id']
        extra_kwargs = {
            'name': {'read_only': True},
        }


class FavouriteSerializer(serializers.ModelSerializer):
    tour_slug = serializers.CharField(source='target.slug', read_only=True)
    tour_price = serializers.CharField(source='target.price', read_only=True)
    tour_img = serializers.URLField(
        source='target.img_preview_url', read_only=True)
    tour_title = serializers.CharField(source='target.title', read_only=True)

    class Meta:
        model = Favourites
        fields = '__all__'
