from django.db import models

from accounts.models import User


# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    cover_image = models.JSONField(default=dict, blank=True, null=True)
    logo = models.JSONField(default=dict, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    address = models.JSONField(default=dict, blank=True, null=True)
    settings = models.JSONField(default=dict, blank=True, null=True)
    orders_count = models.PositiveIntegerField(default=0)
    products_count = models.PositiveIntegerField(default=0)

    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name}"
