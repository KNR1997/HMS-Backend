from typing import List, Optional

from django.db import transaction

from accounts.models import BaseUser
from common.services import model_update


@transaction.atomic
def user_create(*, email: str,
                password: Optional[str] = None
                ) -> BaseUser:
    user = BaseUser.objects.create_user(email=email,
                                        password=password,
                                        )

    return user


@transaction.atomic
def user_update(*, user: BaseUser, data) -> BaseUser:
    non_side_effect_fields: List[str] = [
        # "first_name",
        # "last_name"
    ]

    user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...

    return user
