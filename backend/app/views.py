from django.db.models import Prefetch, Count, Q
from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from app.models import *
from app.serializers import *
from app.filters import *


class SocialMediaTypeListView(generics.ListAPIView):
    queryset = SocialMediaType.objects.all()
    serializer_class = SocialMediaTypeSerializer


class ReservationStatusListView(generics.ListAPIView):
    queryset = ReservationStatus.objects.all()
    serializer_class = ReservationStatusSerializer


class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class SocialMediaViewSet(viewsets.ModelViewSet):
    serializer_class = SocialMediaSerializer
    queryset = SocialMedia.objects.select_related('media_type', 'target')


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyFilter
    http_method_names = ['get', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CompanyFullSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'retrieve':
            queryset = queryset.prefetch_related(
                Prefetch('socialmedia_set',
                        queryset=SocialMedia.objects.select_related('media_type')
                       )
            )
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.annotate(
        favourites_count=Count('favourites')
    ).select_related('company', 'country')
    serializer_class = TourSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TourFilter

    @action(detail=True, methods=['get'], url_path='favourite')
    def get_favourite(self, request, slug=None):
        response_data = {'is_favorite': False}

        if not request.user.is_authenticated:
            return Response(response_data)

        try:
            tour = self.get_object()
            response_data['is_favorite'] = Favourites.objects.filter(
                customer=request.user,
                target=tour
            ).exists()
        except Exception:
            pass

        return Response(response_data)

    @action(detail=True, methods=['post'], url_path='favourite')
    def set_favourite(self, request, slug=None):
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        tour = self.get_object()
        customer = request.user

        if not Favourites.objects.filter(customer=customer, target=tour).exists():
            Favourites.objects.create(customer=customer, target=tour)

        return Response(
            {'is_favorite': True},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['delete'], url_path='favourite')
    def delete_favourite(self, request, slug=None):
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        tour = self.get_object()
        customer = request.user
        deleted, _ = Favourites.objects.filter(
            customer=customer,
            target=tour
        ).delete()

        if deleted == 0:
            return Response(
                {'detail': 'Tour was not in favorites'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {'is_favorite': False},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['get'], url_path='full')
    def get_full_info(self, request, slug=None):
        desired_statuses = [ReservationStatus.PAID]

        tour = Tour.objects.filter(slug=slug).annotate(
            favourites_count=Count('favourites')
        ).select_related(
            'tourinfo',
            'company',
            'country'
        ).prefetch_related(
            Prefetch(
                'tourtimespan_set',
                queryset=TourTimeSpan.objects.order_by('-date_to').annotate(
                    places_released=Count(
                        'reservation',
                        filter=Q(
                            reservation__status__status__in=desired_statuses)
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
        popular_tours = self.get_queryset().order_by('-favourites_count')[:7]
        serializer = self.get_serializer(popular_tours, many=True)
        return Response(serializer.data)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related('status')
    serializer_class = ReservationSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_data = {
            'message': 'Пользователь успешно создан',
            'username': user.username,
            'email': user.email,
            'phone': user.phone
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class UserDetailView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class FavouritesAPIView(generics.GenericAPIView):
    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        response = {'is_favorite': False}

        if request.user.is_authenticated:
            response['is_favorite'] = Favourites.objects.filter(
                customer=request.user,
                target__slug=slug
            ).exists()

        return Response(response)

    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        tour = get_object_or_404(Tour, slug=slug)
        Favourites.objects.get_or_create(
            customer=request.user,
            target=tour
        )
        return Response({'is_favorite': True}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        Favourites.objects.filter(
            customer=request.user,
            target__slug=slug
        ).delete()
        return Response({'is_favorite': False}, status=status.HTTP_200_OK)


class FavouriteViewSet(viewsets.GenericViewSet):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'delete', 'head', 'options']

    def get_queryset(self):
        return Favourites.objects.select_related('target').filter(customer=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = FavouriteSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)

    @action(detail=False, methods=['get'], url_path='clear')
    def clear(self, request, *args, **kwargs):
        self.get_queryset().delete()
        return Response(status=204)
