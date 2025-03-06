from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from products.models import Type, Product, Category, Attribute, AttributeValue, ProductVariation, \
    ProductVariationOption, Batch, Tag


# Register your models here.
@admin.register(Type)
class Type(ImportExportModelAdmin):
    pass


@admin.register(Category)
class Category(ImportExportModelAdmin):
    pass


@admin.register(Tag)
class Tag(ImportExportModelAdmin):
    pass


@admin.register(Attribute)
class Attribute(ImportExportModelAdmin):
    pass


@admin.register(AttributeValue)
class AttributeValue(ImportExportModelAdmin):
    pass


@admin.register(Product)
class Product(ImportExportModelAdmin):
    pass


@admin.register(ProductVariation)
class ProductVariation(ImportExportModelAdmin):
    pass


@admin.register(ProductVariationOption)
class ProductVariationOption(ImportExportModelAdmin):
    pass


@admin.register(Batch)
class Batch(ImportExportModelAdmin):
    pass
