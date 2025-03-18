import uuid
from typing import List

from django.db import transaction
from rest_framework.exceptions import ValidationError

from accounts.models import BaseUser
from common.services import model_update
from common.utils import get_object
from hotels.models import Room
from hotels.selectors import hotel_list


@transaction.atomic
def room_create(*, category_id: uuid.UUID,
                room_number: str,
                is_available: bool) -> Room:
    hotels = hotel_list()
    hotel_id = hotels.first().id

    # Check if the room number already exists in the same hotel
    if Room.objects.filter(hotel_id=hotel_id, room_number=room_number).exists():
        raise ValidationError(f"A room with room number {room_number} already exists in this hotel.")

    # Create the room if no duplicate is found
    room = Room.objects.create(
        hotel_id=hotel_id,
        category_id=category_id,
        room_number=room_number,
        is_available=is_available,
    )

    return room


@transaction.atomic
def room_update(*, room: Room, data, updated_by: BaseUser) -> Room:
    non_side_effect_fields: List[str] = [
        "name",
        "slug",
        "description",
        "capacity",
        "price_per_night",
    ]

    # all_fields = non_side_effect_fields + ["type", "department", "parent"]
    room, has_updated = model_update(instance=room, fields=non_side_effect_fields, data=data)

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...
    # if "updated_by" not in non_side_effect_fields:
    #     room.save(update_fields=["updated_by"])

    return room


@transaction.atomic
def room_delete(*, room_id: str) -> None:
    room = get_object(Room, id=room_id)
    room.delete()
    return None
