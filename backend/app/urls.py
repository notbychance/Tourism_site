from rest_framework.routers import DefaultRouter

from app import views
from django.urls import path, include

from .addons import CustomRouter
from .views import *

router = CustomRouter()
router.register(r'company', CompanyViewSet, basename='company')
router.register(r'tour', TourViewSet, basename='tour')
router.register(r'favourite', FavouriteViewSet, basename='favourites')
router.register(r'favourites', FavouritesViewsSet, basename='toggle_favourite')
router.register(r'social-media-type', SocialMediaTypeViewSet, basename='social_media_type')
router.register(r'reservation-status-type', ReservationStatusViewSet, basename='reservation_status_type')
router.register(r'country', CountryViewSet, basename='country')
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'reservation', ReservationViewSet, basename='reservations')
