from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from configurations.models import FileAttachment, FAQ


# Register your models here.
@admin.register(FileAttachment)
class Type(ImportExportModelAdmin):
    pass


@admin.register(FAQ)
class FAQ(ImportExportModelAdmin):
    pass
