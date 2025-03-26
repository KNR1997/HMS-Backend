import django_filters

from hotels.models import Room


class BaseRoomFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains', label="Category")

    class Meta:
        model = Room
        fields = ('id', 'category')


class BaseRoomCategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label="Name")

    class Meta:
        model = Room
        fields = ('id', 'name')