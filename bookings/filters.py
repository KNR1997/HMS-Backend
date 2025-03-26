import django_filters

from bookings.models import Booking


class BaseBookingFilter(django_filters.FilterSet):
    customer_name = django_filters.CharFilter(field_name='customer_name', lookup_expr='icontains', label="Name")

    class Meta:
        model = Booking
        fields = ('id', 'customer_name')
