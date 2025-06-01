from rest_framework.routers import DefaultRouter

from app import views
from django.urls import  path

from .addons import SlugRouter
from .views import *

router = DefaultRouter()
# router.register(r'customer', CustomerViewSet, basename='customer')

slug_router = SlugRouter()
slug_router.register(r'company', CompanyViewSet, basename='company')
slug_router.register(r'tour', TourViewSet, basename='tour')
slug_router.register(r'favourite', FavouritesViewSet, basename='favourite')

urlpatterns = [
    path('social-media-type/', SocialMediaTypeListView.as_view()),
    path('reservation-status-type/', ReservationStatusListView.as_view()),
    path('country/', CountryListView.as_view()),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('user/', UserDetailView.as_view(), name='customer_detail')
]

urlpatterns += router.urls
urlpatterns += slug_router.urls