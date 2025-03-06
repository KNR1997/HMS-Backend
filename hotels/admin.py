from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from hotels.models import Room, Hotel, RoomCategory


# Register your models here.
@admin.register(Hotel)
class Hotel(ImportExportModelAdmin):
    pass


@admin.register(RoomCategory)
class RoomCategory(ImportExportModelAdmin):
    pass


@admin.register(Room)
class Room(ImportExportModelAdmin):
    pass
