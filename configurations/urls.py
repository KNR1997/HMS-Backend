from django.urls import path

from .apis import faq_apis
from .views import settings_views, file_upload_views

urlpatterns = [
    path('settings/', settings_views.get_settings, name='get_settings'),
    path('attachments', file_upload_views.upload_file, name='upload_file'),

    path('faqs/',                           faq_apis.FAQListApi.as_view()),
    path('faqs/create',                     faq_apis.FAQCreateApi.as_view()),
    # path('faqs/<slug:slug>',                faq_apis.RoomDetailApi.as_view()),
    # path('faqs/<str:slug>/update',          faq_apis.RoomUpdateApi.as_view()),
    # path('faqs/<str:slug>/delete',          faq_apis.RoomDeleteApi.as_view()),

]
