from django.db import models

# Create your models here.
class FileAttachment(models.Model):
    original = models.ImageField(max_length=255, blank=True, null=True)
    thumbnail = models.ImageField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original}"
