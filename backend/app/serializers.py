from django.utils import timezone
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.validators import validate_email
from django.contrib.auth import get_user_model

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
            is_api_user=True
        )
        return user


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'avatar']


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


class CustomerTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['login'] = user.login
        token['email'] = user.email
        return token

    def validate(self, attrs):
        login = attrs.get('username')
        password = attrs.get('password')

        try:
            customer = Customer.objects.get(login=login)
        except Customer.DoesNotExist:
            raise serializers.ValidationError(
                'Пользователь с таким логином не найден')

        if not customer.check_password(password):
            raise serializers.ValidationError('Неверный пароль')

        data = {}
        refresh = self.get_token(customer)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        exclude = ['id']
        extra_kwargs = {
            'name': {'read_only': True},
        }
