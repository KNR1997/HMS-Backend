from django.urls import path

from bookings.apis import booking_apis, booking_item_apis
from bookings import reports

urlpatterns = [
    path('web/process-booking',                     booking_apis.ProcessBookingApi.as_view()),
    path('admin/process-booking',                   booking_apis.ProcessBookingFromAdminApi.as_view()),
    path('customer/process-booking',                booking_apis.ProcessBookingByCustomerApi.as_view()),

    path('bookings/',                               booking_apis.BookingListApi.as_view()),
    path('bookings/my-bookings/',                   booking_apis.MyBookingListApi.as_view()),
    path('bookings/<slug:booking_number>/',         booking_apis.BookingDetailApi.as_view()),
    path('bookings/<slug:booking_number>/update',   booking_apis.BookingUpdateApi.as_view()),
    path('bookings/<slug:booking_id>/delete',       booking_apis.BookingDeleteApi.as_view()),

    path('booking-items/<slug:booking_item_id>/delete', booking_item_apis.BookingItemDeleteApi.as_view()),

    path('analytics/total-rooms',                   reports.total_rooms_report),
    path('analytics/available-rooms',               reports.available_rooms_report),
    path('analytics/room-categories',               reports.room_categories_report),
    path('analytics/bookings',                      reports.bookings_report),
    path('analytics/revenue',                      reports.revenue_report),

]