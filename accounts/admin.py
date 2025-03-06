from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from accounts.models import User, Customer


# Register your models here.
@admin.register(User)
class User(ImportExportModelAdmin):
    pass


@admin.register(Customer)
class Customer(ImportExportModelAdmin):
    pass
