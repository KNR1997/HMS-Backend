# bookings/utils/calculations.py

import decimal
import datetime
from hotels.selectors import room_get_by_room_number

def calculate_total_price(*, booking_items: list[dict], check_in: str, check_out: str) -> decimal.Decimal:
    """
    Calculate the total price for the booking based on the booking items and the duration of the stay.
    """
    total_price = decimal.Decimal(0.0)

    # Convert check_in and check_out to date objects
    check_in_date = datetime.datetime.strptime(check_in, "%Y-%m-%d").date()
    check_out_date = datetime.datetime.strptime(check_out, "%Y-%m-%d").date()

    # Calculate the number of nights
    num_nights = (check_out_date - check_in_date).days

    # Loop through booking items and calculate the total price
    for booking_item in booking_items:
        room = room_get_by_room_number(room_number=booking_item.get('room_number'))
        room_category = room.category
        total_price += room_category.price_per_night * num_nights

    return total_price