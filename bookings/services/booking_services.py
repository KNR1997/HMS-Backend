import decimal
import uuid
from typing import List

from django.db import transaction
from django.db.models import Max

from accounts.models import BaseUser
from bookings.models import Booking
from bookings.services.booking_items_services import booking_item_create
from bookings.utils.calculations import calculate_total_price
from common.services import model_update
from common.utils import get_object
from hotels.selectors import room_get_by_room_number


@transaction.atomic
def process_booking(*, user_id: uuid = None,
                    customer_name: str,
                    customer_id_number: str,
                    check_in: str,
                    check_out: str,
                    booking_items: list[str],
                    status: str = None,
                    ) -> Booking:
    # Calculate the total price
    total_price = calculate_total_price(booking_items=booking_items, check_in=check_in, check_out=check_out)

    # Create the booking
    booking = booking_create(user_id=user_id,
                             customer_name=customer_name,
                             customer_id_number=customer_id_number,
                             check_in=check_in,
                             check_out=check_out,
                             total_price=total_price,
                             status=status,
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
def process_booking_by_customer(*, user: BaseUser,
                                customer_name: str,
                                customer_id_number: str,
                                check_in: str,
                                check_out: str,
                                booking_items: list[str],
                                status: str = None,
                                ) -> Booking:
    # Calculate the total price
    total_price = calculate_total_price(booking_items=booking_items, check_in=check_in, check_out=check_out)

    # Create the booking
    booking = booking_create(user_id=user.id,
                             customer_name=customer_name,
                             customer_id_number=customer_id_number,
                             check_in=check_in,
                             check_out=check_out,
                             total_price=total_price,
                             status='Pending',
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
                   customer_name: str,
                   customer_id_number: str,
                   check_in: str,
                   check_out: str,
                   total_price: decimal,
                   status: str = None,
                   ) -> Booking:
    # Find the maximum booking_number in the database
    max_booking_number = Booking.objects.aggregate(Max('booking_number'))['booking_number__max']
    if max_booking_number is None:
        booking_number = 1
    else:
        booking_number = max_booking_number + 1

    booking = Booking.objects.create(user_id=user_id,
                                     booking_number=booking_number,
                                     customer_name=customer_name,
                                     customer_id_number=customer_id_number,
                                     check_in=check_in,
                                     check_out=check_out,
                                     total_price=total_price,
                                     status=status,
                                     )

    return booking


@transaction.atomic
def booking_update(*, booking: Booking, data) -> Booking:
    non_side_effect_fields: List[str] = [
        "status",
    ]

    previous_status = booking.status  # Store previous status before updating

    # all_fields = non_side_effect_fields + ["type", "department", "parent"]
    booking, has_updated = model_update(instance=booking, fields=non_side_effect_fields, data=data)

    # If status changed to "CheckOut" or "Cancelled", update all associated rooms to is_available=True
    if has_updated and previous_status not in ["CheckOut", "Cancelled"] and booking.status in ["CheckOut", "Cancelled"]:
        booking_items = booking.booking_items.all()
        for booking_item in booking_items:
            if booking_item.room:  # Ensure room exists before updating
                booking_item.room.is_available = True
                booking_item.room.save(update_fields=["is_available"])

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
