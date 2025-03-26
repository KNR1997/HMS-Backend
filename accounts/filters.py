import django_filters

from accounts.models import BaseUser


class BaseUserFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains', label="Email")

    class Meta:
        model = BaseUser
        fields = ('id', 'email')
