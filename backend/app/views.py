from django.db.models import Prefetch, Count, Q
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from app.models import *
from app.serializers import *
from app.filters import *


class SocialMediaTypeViewSet(viewsets.GenericViewSet):
    queryset = SocialMediaType.objects.all()
    serializer_class = SocialMediaTypeSerializer

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)


class ReservationStatusViewSet(viewsets.GenericViewSet):
    queryset = ReservationStatus.objects.all()
    serializer_class = ReservationStatusSerializer

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)


class CountryViewSet(viewsets.GenericViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)


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
                         queryset=SocialMedia.objects.select_related(
                             'media_type')
                         ),
                Prefetch('tour_set',
                         queryset=Tour.objects.all()
                         )
            )
        return queryset


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


class AuthViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action in ['user', 'list', 'delete', 'change-password', 'update']:
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        return TokenObtainPairView.as_view()(request._request)

    @action(detail=False, methods=['post'], url_path='refresh')
    def refresh(self, request):
        return TokenRefreshView.as_view()(request._request)

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_data = {
            'message': 'Пользователь успешно создан',
            'username': user.username,
            'email': user.email,
            'phone': user.phone
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='user')
    def user(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'], url_path='delete')
    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        user = request.user
        serializer = UserChangePasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(serializer.validated_data['password']):
            return Response(
                {"password": "Неверный текущий пароль"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response(
            {"message": "Пароль успешно изменен"},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['patch'], url_path='update')
    def patch_user(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_path='avatar')
    def delete_avatar(self, request):
        user = request.user

        if not user.avatar:
            return Response(
                {"detail": "Аватар отсутствует"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            # Удаляем файл с диска
            if os.path.isfile(user.avatar.path):
                os.remove(user.avatar.path)

            # Очищаем поле в базе данных
            user.avatar = None
            user.save()

            return Response(
                {"detail": "Аватар успешно удален"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"detail": f"Ошибка при удалении аватара: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['update'], url_path='update')
    def update_user(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(status=status.HTTP_404_NOT_FOUND)
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)


class FavouritesViewsSet(viewsets.GenericViewSet):
    queryset = Favourites.objects.all()
    serializer_class = FavouriteSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def get_permissions(self):
        if self.action in ['add', 'remove']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(status=status.HTTP_404_NOT_FOUND)
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='check')
    def check(self, request, slug=None):
        response = {'is_favorite': False}

        if request.user.is_authenticated:
            response['is_favorite'] = Favourites.objects.filter(
                customer=request.user,
                target__slug=slug
            ).exists()

        return Response(response)

    @action(detail=True, methods=['post'], url_path='add')
    def add(self, request, slug=None):
        tour = get_object_or_404(Tour, slug=slug)
        Favourites.objects.get_or_create(
            customer=request.user,
            target=tour
        )
        return Response({'is_favorite': True}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], url_path='remove')
    def remove(self, request, slug=None):
        Favourites.objects.filter(
            customer=request.user,
            target__slug=slug
        ).delete()
        return Response({'is_favorite': False}, status=status.HTTP_204_NO_CONTENT)


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


class ReservationViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def get_queryset(self):
        queryset = Reservation.objects.select_related(
            'target', 'status'
        ).filter(customer=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        desired_statuses = [ReservationStatus.WAITING]

        instance = self.get_queryset().filter(status__status__in=desired_statuses)
        page = paginator.paginate_queryset(instance, request)

        serializer = self.get_serializer(instance, many=True)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='count')
    def count(self, request, *args, **kwargs):
        desired_statuses = [ReservationStatus.WAITING]
        count = self.get_queryset().filter(status__status__in=desired_statuses).count()
        return Response(
            {
                'count': count
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], url_path='history')
    def history(self, request, *args, **kwargs):
        paginator = PageNumberPagination()

        queryset = self.get_queryset()
        page = paginator.paginate_queryset(queryset, request)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='reserve')
    def reserve(self, request, slug=None, *args, **kwargs):
        instance = Tour.objects.prefetch_related(
            Prefetch(
                'tourtimespan_set',
                queryset=TourTimeSpan.objects.order_by('-date_to')
            )
        ).get(slug=slug)

        timespan = instance.tourtimespan_set.first()
        customer = request.user
        stat = ReservationStatus.objects.get(status=ReservationStatus.WAITING)
        count = request.data.get('count')

        Reservation.objects.create(
            status=stat,
            customer=customer,
            target=timespan,
            count=count if count else 1
        )

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'], url_path='delete')
    def delete(self, request, *args, **kwargs):
        try:
            reservation_id = request.data.get('id')
            if not reservation_id:
                return Response(
                    {"error": "Reservation ID is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            deleted_count, _ = self.get_queryset().filter(
                id=reservation_id
            ).delete()

            if deleted_count == 0:
                return Response(
                    {"error": "Reservation not found or not owned by user"},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['patch'], url_path='update')
    def update_count(self, request, *args, **kwargs):
        try:
            reservation_id = request.data.get('id')

            try:
                count = int(request.data.get('count', 1))
            except (TypeError, ValueError):
                return Response(
                    {"error": "Count must be a valid integer"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not reservation_id:
                return Response(
                    {"error": "Reservation ID is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            item = self.get_queryset().filter(
                id=reservation_id
            ).first()

            if not item:
                return Response(
                    {"error": "Reservation not found or not owned by user"},
                    status=status.HTTP_404_NOT_FOUND
                )

            if count <= 0:
                return Response(
                    {"error": "Count must be a positive integer"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            item.count = count
            item.save()

            return Response(status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['patch'], url_path='status')
    def update_status(self, request, *args, **kwargs):
        ids = request.data.get('ids', [])
        if not isinstance(ids, list) or not ids:
            return Response(
                {"error": "A non-empty list of IDs is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        stat = ReservationStatus.objects.get(status=ReservationStatus.PAID)

        query = self.get_queryset().filter(id__in=ids).update(status=stat)

        return Response(status=status.HTTP_200_OK)
