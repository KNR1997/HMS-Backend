from django.urls import path

from bookings.apis import booking_apis, booking_item_apis

urlpatterns = [
    path('web/process-booking',                     booking_apis.ProcessBookingApi.as_view()),

    path('bookings/',                               booking_apis.BookingListApi.as_view()),
    path('bookings/<slug:booking_number>/',         booking_apis.BookingDetailApi.as_view()),
    path('bookings/<slug:booking_number>/update',   booking_apis.BookingUpdateApi.as_view()),
    path('bookings/<slug:booking_id>/delete',       booking_apis.BookingDeleteApi.as_view()),

    path('booking-items/<slug:booking_item_id>/delete', booking_item_apis.BookingItemDeleteApi.as_view()),

]