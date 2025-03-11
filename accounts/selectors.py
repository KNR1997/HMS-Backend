from typing import Optional

from django.db.models import QuerySet

from accounts.models import User
from common.utils import get_object


def user_get(user_id) -> Optional[User]:
    user = get_object(User, id=user_id)

    return user


def user_list(*, filters=None) -> QuerySet[User]:
    filters = filters or {}

    qs = User.objects.all()

    return qs


def admin_list(*, filters=None) -> QuerySet[User]:
    filters = filters or {}

    qs = User.objects.filter(is_staff=True)

    return qs
