import django_filters

from hotels.models import Room


class BaseRoomFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains', label="Category")

    class Meta:
        model = Room
        fields = ('id', 'category')
