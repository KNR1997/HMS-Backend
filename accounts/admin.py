from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from accounts.models import User, Customer, Permission


# Register your models here.
@admin.register(Permission)
class Permission(ImportExportModelAdmin):
    pass


@admin.register(User)
class User(ImportExportModelAdmin):
    pass


@admin.register(Customer)
class Customer(ImportExportModelAdmin):
    pass
