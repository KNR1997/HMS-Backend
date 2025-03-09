from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from bookings.models import Booking, BookingItem


# Register your models here.
@admin.register(Booking)
class Booking(ImportExportModelAdmin):
    pass


@admin.register(BookingItem)
class BookingItem(ImportExportModelAdmin):
    pass
