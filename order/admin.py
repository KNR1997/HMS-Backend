from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from order.models import Order, OrderItem, OrderAddress


# Register your models here.


@admin.register(Order)
class Order(ImportExportModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItem(ImportExportModelAdmin):
    pass


@admin.register(OrderAddress)
class OrderAddress(ImportExportModelAdmin):
    pass
