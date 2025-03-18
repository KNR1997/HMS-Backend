import uuid

from django.db import models

from accounts.models import BaseUser
from common.models import BaseModel
from hotels.models import Room


# Create your models here.
class Booking(BaseModel):
    ORDER_STATUS = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
        ("CheckIn", "CheckIn"),
        ("CheckOut", "CheckOut")
    ]

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    booking_number = models.IntegerField(null=True, unique=True)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="bookings", null=True, blank=True)
    customer_name = models.CharField(max_length=255, null=True, unique=True)
    customer_id_number = models.CharField(max_length=255, null=True, unique=True)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="Pending")

    def __str__(self):
        return f"Booking {self.booking_number}"


class BookingItem(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booking_items')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking {self.booking.id} - Room {self.room.room_number}"
