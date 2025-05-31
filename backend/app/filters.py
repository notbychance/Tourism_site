from django_filters import FilterSet, NumberFilter, CharFilter

from app.models import Tour

class TourFilter(FilterSet):
    min_price = NumberFilter(field_name="price", lookup_expr='gte')
    max_price = NumberFilter(field_name="price", lookup_expr='lte')
    country = CharFilter(field_name='country__name', lookup_expr='icontains')
    
    class Meta:
        model = Tour
        fields = ['country', 'price']