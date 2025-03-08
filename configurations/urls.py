from django.urls import path

from .views import settings_views, file_upload_views

urlpatterns = [
    path('settings/', settings_views.get_settings, name='get_settings'),
    path('attachments', file_upload_views.upload_file, name='upload_file'),

]
