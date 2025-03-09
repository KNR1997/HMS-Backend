import decimal

from django.db import transaction

from bookings.models import BookingItem, Booking
from common.utils import get_object
from hotels.models import Room


@transaction.atomic
def booking_item_create(*, booking: Booking,
                   room: Room,
                   price_per_night: decimal,
                   ) -> BookingItem:
    booking_item = BookingItem.objects.create(booking=booking,
                                              room=room,
                                              price_per_night=price_per_night,
                                              )

    return booking_item


@transaction.atomic
def booking_item_delete(*, booking_item_id: str) -> None:
    booking_item = get_object(BookingItem, id=booking_item_id)

    room = booking_item.room
    room.is_available = True
    room.save()

    booking_item.delete()
    return None
