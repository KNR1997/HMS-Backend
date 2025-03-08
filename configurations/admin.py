from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from configurations.models import FileAttachment


# Register your models here.
@admin.register(FileAttachment)
class Type(ImportExportModelAdmin):
    pass
