from typing import Optional

import django_filters

from common.utils import get_object
from products.models import Product, Tag, Category


class BaseProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ('id', 'name')

def product_get(product_id) -> Optional[Product]:
    product = get_object(Product, id=product_id)

    return product

def product_get_by_slug(slug) -> Optional[Product]:
    product = get_object(Product, slug=slug)

    return product


def product_list(*, filters=None):
    filters = filters or {}

    qs = Product.objects.all()

    return BaseProductFilter(filters, qs).qs


def tag_list(*, filters=None):
    filters = filters or {}

    qs = Tag.objects.all()

    return BaseProductFilter(filters, qs).qs


def tag_get_by_slug(slug) -> Optional[Tag]:
    tag = get_object(Tag, slug=slug)

    return tag


def category_list(*, filters=None):
    filters = filters or {}

    qs = Category.objects.all()

    return BaseProductFilter(filters, qs).qs
