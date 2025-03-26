from typing import Optional

from django.db.models import QuerySet

from bookings.filters import BaseBookingFilter
from bookings.models import Booking
from common.utils import get_object


def booking_list(*, filters=None) -> QuerySet[Booking]:
    filters = filters or {}

    qs = Booking.objects.all()

    return BaseBookingFilter(filters, qs).qs


def my_booking_list(*, filters=None, user=None) -> QuerySet[Booking]:
    filters = filters or {}

    qs = Booking.objects.filter(user=user)

    return qs


def booking_get_by_booking_number(booking_number) -> Optional[Booking]:
    booking = get_object(Booking, booking_number=booking_number)

    return booking
