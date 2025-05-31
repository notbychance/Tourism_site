from django.utils import timezone
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from app.models import *


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Customer
        fields = ['credentials', 'email', 'login',
                  'password', 'password_confirm']
        extra_kwargs = {
            'credentials': {'required': True},
            'email': {'required': True},
            'login': {'required': True},
        }

    def validate(self, attrs):
        # Проверка совпадения паролей
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {"password": "Пароли не совпадают"})

        # Проверка уникальности email
        if Customer.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                {"email": "Этот email уже используется"})

        # Проверка уникальности login
        if Customer.objects.filter(login=attrs['login']).exists():
            raise serializers.ValidationError(
                {"login": "Этот логин уже занят"})

        # Валидация email
        try:
            validate_email(attrs['email'])
        except ValidationError:
            raise serializers.ValidationError({"email": "Некорректный email"})

        return attrs

    def create(self, validated_data):
        # Удаляем подтверждение пароля
        validated_data.pop('password_confirm')

        # Хешируем пароль
        password = validated_data.pop('password')
        customer = Customer(**validated_data)
        customer.set_password(password)
        customer.save()

        return customer


class CustomerLoginSerializer(serializers.Serializer):
    login = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('password')

        try:
            customer = Customer.objects.get(login=login)
        except Customer.DoesNotExist:
            raise serializers.ValidationError(
                {"login": "Неверный логин или пароль"})

        if not customer.check_password(password):
            raise serializers.ValidationError(
                {"login": "Неверный логин или пароль"})

        attrs['customer'] = customer
        return attrs


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
    social_media = SocialMediaSerializer(
        source='socialmedia_set',  # Указываем обратное отношение
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


class ReservationSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='status.status', read_only=True)

    class Meta:
        model = Reservation
        exclude = ['id']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['login'] = user.login
        return token


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        exclude = ['id']
        extra_kwargs = {
            'name': {'read_only': True},
        }
