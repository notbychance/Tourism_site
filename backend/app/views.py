from django.db.models import Prefetch, Count, Q
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from app.models import *
from app.serializers import *


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    # def list(self, request, *args, **kwargs):
    #     return Response(
    #         {"detail": "Listing all customers is not allowed."},
    #         status=status.HTTP_403_FORBIDDEN
    #     )


class SocialMediaTypeListView(generics.ListAPIView):
    queryset = SocialMediaType.objects.all()
    serializer_class = SocialMediaTypeSerializer


class ReservationStatusListView(generics.ListAPIView):
    queryset = ReservationStatus.objects.all()
    serializer_class = ReservationStatusSerializer


class SocialMediaViewSet(viewsets.ModelViewSet):
    serializer_class = SocialMediaSerializer
    queryset = SocialMedia.objects.select_related('media_type', 'target')


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.prefetch_related(
        Prefetch('socialmedia_set',
                queryset=SocialMedia.objects.select_related('media_type')
                )
    )
    serializer_class = CompanySerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.annotate(
        favourites_count=Count('favourites')
    ).select_related('company')
    serializer_class = TourSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    @action(detail=True, methods=['get'], url_path='full')
    def get_full_info(self, request, slug=None):
        desired_statuses = [ReservationStatus.PAID]

        tour = Tour.objects.filter(slug=slug).select_related(
            'tourinfo',
            'company'
        ).prefetch_related(
            Prefetch(
                'tourtimespan_set',
                queryset=TourTimeSpan.objects.order_by('-date_to').annotate(
                    places_released=Count(
                        'reservation',
                        filter=Q(reservation__status__status__in=desired_statuses)
                    )
                ).prefetch_related(
                    Prefetch(
                        'reservation_set',
                        queryset=Reservation.objects.select_related('status')
                        .filter(status__status__in=desired_statuses),
                        to_attr='filtered_reservations'
                    )
                )
            )
        ).first()

        nearest_timespan = tour.tourtimespan_set.first()

        data = {
            'basic_info': TourSerializer(tour).data,
            'detailed_info': TourInfoSerializer(tour.tourinfo).data if hasattr(tour, 'tourinfo') else None,
            'time_spans': TourTimeSpanSerializer(nearest_timespan).data if nearest_timespan else None
        }
        return Response(data)

    @action(detail=False, methods=['get'], url_path='popular')
    def get_popular_tours(self, request):
        popular_tours = self.get_queryset().order_by('-favourites_count')[:5]
        serializer = self.get_serializer(popular_tours, many=True)
        return Response(serializer.data)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related('status')
    serializer_class = ReservationSerializer


class CustomerRegistrationView(generics.CreateAPIView):
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer = Customer.objects.create_user(
            login=serializer.validated_data['login'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            credentials=serializer.validated_data['credentials'],
            phone=serializer.validated_data['phone']
        )

        return Response({
            'message': 'Пользователь успешно зарегистрирован',
            'login': customer.login
        }, status=status.HTTP_201_CREATED)


class CustomerTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer