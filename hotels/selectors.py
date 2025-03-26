from typing import Optional

from django.db.models import QuerySet

from common.utils import get_object
from hotels.filters import BaseRoomFilter, BaseRoomCategoryFilter
from hotels.models import Room, RoomCategory, Hotel


def hotel_list(*, filters=None) -> QuerySet[Hotel]:
    filters = filters or {}

    qs = Hotel.objects.all()

    return qs


def room_list(*, filters=None) -> QuerySet[Room]:
    filters = filters or {}

    qs = Room.objects.all()

    return BaseRoomFilter(filters, qs).qs


def room_get(room_id) -> Optional[Room]:
    room = get_object(Room, id=room_id)

    return room


def room_get_by_room_number(room_number) -> Optional[Room]:
    room = get_object(Room, room_number=room_number)

    return room


def room_category_list(*, filters=None) -> QuerySet[RoomCategory]:
    filters = filters or {}

    qs = RoomCategory.objects.all()

    return BaseRoomCategoryFilter(filters, qs).qs


def room_category_get(room_category_id) -> Optional[RoomCategory]:
    room_category = get_object(RoomCategory, id=room_category_id)

    return room_category


def room_category_get_by_slug(slug) -> Optional[RoomCategory]:
    room_category = get_object(RoomCategory, slug=slug)

    return room_category


def hotel_get() -> Optional[Hotel]:
    hotel = Hotel.objects.first()

    return hotel
