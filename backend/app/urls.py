from rest_framework.routers import DefaultRouter

from app import views
from django.urls import  path

from .addons import SlugRouter
from .views import *

router = DefaultRouter()
router.register(r'customer', CustomerViewSet, basename='customer')

slug_router = SlugRouter()
slug_router.register(r'company', CompanyViewSet, basename='company')
slug_router.register(r'tour', TourViewSet, basename='tour')

urlpatterns = [
    path('social-media-type/', SocialMediaTypeListView.as_view()),
    path('reservation-status-type/', ReservationStatusListView.as_view()),
    path('country/', CountryListView.as_view()),
    path('register/', CustomerRegistrationView.as_view(), name='register'),
    path('token/', CustomerTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
urlpatterns += slug_router.urls