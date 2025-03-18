import decimal
import json
from typing import List

from django.db import transaction

from accounts.models import BaseUser
from common.services import model_update
from common.utils import get_object
from hotels.models import RoomCategory


@transaction.atomic
def room_category_create(*, name: str,
                         slug: str,
                         image: json = None,
                         description: str = None,
                         capacity: int,
                         price_per_night: decimal,
                         ) -> RoomCategory:
    room = RoomCategory.objects.create(name=name,
                                       slug=slug,
                                       image=image,
                                       description=description,
                                       capacity=capacity,
                                       price_per_night=price_per_night,
                                       )

    return room


@transaction.atomic
def room_category_update(*, room_category: RoomCategory, data, updated_by: BaseUser) -> RoomCategory:
    non_side_effect_fields: List[str] = [
        "name",
        "slug",
        "image",
        "description",
        "capacity",
        "price_per_night",
    ]

    # all_fields = non_side_effect_fields + ["type", "department", "parent"]
    room_category, has_updated = model_update(instance=room_category, fields=non_side_effect_fields, data=data)

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...
    # if "updated_by" not in non_side_effect_fields:
    #     room.save(update_fields=["updated_by"])

    return room_category


@transaction.atomic
def room_category_delete(*, room_category_id: str) -> None:
    room = get_object(RoomCategory, id=room_category_id)
    room.delete()
    return None
