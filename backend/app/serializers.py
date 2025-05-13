from rest_framework import serializers

from app.models import *


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['id']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)

        request = self.context.get('request')
        if request and request.method == 'GET':
            data.pop('password', None)

        return data


class SocialMediaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaType
        exclude = ['id']
        extra_kwargs = {
            'type': {'read_only': True},
        }


class SocialMediaSerializer(serializers.ModelSerializer):
    media_type_name = serializers.CharField(source='media_type.type', read_only=True)
    days_remaining = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SocialMedia
        exclude = ['id']

    def get_days_remaining(self, obj):
        return (obj.date_to - datetime.datetime.now()).days

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


class TourSerializer(serializers.ModelSerializer):
    favourites_count = serializers.SerializerMethodField(read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    company_slug = serializers.CharField(source='company.slug', read_only=True)

    def get_favourites_count(self, obj):
        if hasattr(obj, 'favourites_count'):
            return obj.favourites_count
        return obj.favourites.count()

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