import uuid

from django.db import models

from common.models import BaseModel


# Create your models here.
class Hotel(BaseModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.FloatField(default=0.0)
    amenities = models.TextField(help_text="Comma-separated list of amenities", null=True, blank=True)
    image = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return self.name


class RoomCategory(BaseModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    image = models.JSONField(default=dict, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    capacity = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Room(BaseModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    image = models.JSONField(default=dict, blank=True, null=True)
    gallery = models.JSONField(default=list, blank=True, null=True)
    room_number = models.CharField(max_length=10, unique=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.room_number}"
