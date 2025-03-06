from django.urls import path

from .views import settings_views

urlpatterns = [
    path('settings/', settings_views.get_settings, name='get_settings'),

]
