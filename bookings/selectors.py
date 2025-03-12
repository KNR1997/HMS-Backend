from typing import Optional

from django.db.models import QuerySet

from bookings.models import Booking
from common.utils import get_object


def booking_list(*, filters=None) -> QuerySet[Booking]:
    filters = filters or {}

    qs = Booking.objects.all()

    return qs


def booking_get_by_booking_number(booking_number) -> Optional[Booking]:
    booking = get_object(Booking, booking_number=booking_number)

    return booking
