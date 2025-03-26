from typing import Optional

from django.db.models import QuerySet

from accounts.filters import BaseUserFilter
from accounts.models import BaseUser
from common.utils import get_object


def user_get(user_id) -> Optional[BaseUser]:
    user = get_object(BaseUser, id=user_id)

    return user


def user_list(*, filters=None) -> QuerySet[BaseUser]:
    filters = filters or {}

    qs = BaseUser.objects.all()

    return BaseUserFilter(filters, qs).qs


def admin_list(*, filters=None) -> QuerySet[BaseUser]:
    filters = filters or {}

    qs = BaseUser.objects.filter(is_admin=True)

    return qs
