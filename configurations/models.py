from django.db import models


def default_translated_languages():
    return ["en"]


# Create your models here.
class FileAttachment(models.Model):
    original = models.ImageField(max_length=255, blank=True, null=True)
    thumbnail = models.ImageField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original}"


class FAQ(models.Model):
    faq_title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    faq_description = models.TextField()
    faq_type = models.CharField(max_length=55, default='global', blank=True, null=True)
    issued_by = models.CharField(max_length=25, default='Super Admin', blank=True, null=True)
    language = models.CharField(max_length=10, default='en', blank=True, null=True)
    translated_languages = models.JSONField(default=default_translated_languages, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.faq_title
