import decimal
import uuid
from typing import List

from django.db import transaction
from django.db.models import Max

from accounts.models import User
from bookings.models import Booking
from bookings.services.booking_items_services import booking_item_create
from bookings.utils.calculations import calculate_total_price
from common.services import model_update
from common.utils import get_object
from hotels.selectors import room_get_by_room_number


@transaction.atomic
def process_booking(*, user_id: uuid,
                    check_in: str,
                    check_out: str,
                    booking_items: list[str],
                    ) -> Booking:
    # Calculate the total price
    total_price = calculate_total_price(booking_items=booking_items, check_in=check_in, check_out=check_out)

    # Create the booking
    booking = booking_create(user_id=user_id,
                             check_in=check_in,
                             check_out=check_out,
                             total_price=total_price,
                             )

    # Create booking items and mark rooms as unavailable
    for booking_item in booking_items:
        room = room_get_by_room_number(room_number=booking_item.get('room_number'))
        room_category = room.category

        booking_item_create(booking=booking,
                            room=room,
                            price_per_night=room_category.price_per_night,
                            )

        room.is_available = False
        room.save()

    return booking


@transaction.atomic
def booking_create(*, user_id: uuid,
                   check_in: str,
                   check_out: str,
                   total_price: decimal,
                   ) -> Booking:
    # Find the maximum booking_number in the database
    max_booking_number = Booking.objects.aggregate(Max('booking_number'))['booking_number__max']
    if max_booking_number is None:
        booking_number = 1
    else:
        booking_number = max_booking_number + 1

    booking = Booking.objects.create(user_id=user_id,
                                     booking_number=booking_number,
                                     check_in=check_in,
                                     check_out=check_out,
                                     total_price=total_price,
                                     )

    return booking


@transaction.atomic
def booking_update(*, booking: Booking, data, updated_by: User) -> Booking:
    non_side_effect_fields: List[str] = [
        "status",
    ]

    # all_fields = non_side_effect_fields + ["type", "department", "parent"]
    booking, has_updated = model_update(instance=booking, fields=non_side_effect_fields, data=data)

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...
    # if "updated_by" not in non_side_effect_fields:
    #     room.save(update_fields=["updated_by"])

    return booking


@transaction.atomic
def booking_delete(*, booking_id: str) -> None:
    booking = get_object(Booking, id=booking_id)
    booking_items = booking.booking_items.all()

    for booking_item in booking_items:
        room = booking_item.room
        room.is_available = True
        room.save()

    booking.delete()
    return None
