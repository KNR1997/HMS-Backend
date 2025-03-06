from typing import List

from django.db import transaction

from common.services import model_update
from common.utils import get_object
from products.models import Product


@transaction.atomic
def product_create(*, name: str,
                   slug: str = None,
                   description: str = None,
                   price: int = None,
                   sale_price: int = None,
                   min_price: int = None,
                   max_price: int = None,
                   sku: int = None,
                   quantity: int = None,
                   image: str = None,
                   gallery: str = None,
                   unit: str = None,
                   product_type: str = None,
                   categories: list = None,
                   tags: list = None,

                   type_id: str,
                   ) -> Product:
    product = Product.objects.create(name=name,
                                     slug=slug,
                                     description=description,
                                     price=price,
                                     sale_price=sale_price,
                                     min_price=min_price,
                                     max_price=max_price,
                                     sku=sku,
                                     quantity=quantity,
                                     status='publish',
                                     product_type=product_type,
                                     unit=unit,
                                     image=image,
                                     gallery=gallery,

                                     type_id=type_id,
                                     )
    # Add categories to the product
    if categories:
        for category in categories:
            product.categories.add(category)  # Assuming categories are instances or IDs

    # Add tags to the product
    if tags:
        for tag in tags:
            product.tags.add(tag)  # Assuming tags are instances or IDs

    return product


@transaction.atomic
def product_update(*, product: Product, data) -> Product:
    non_side_effect_fields: List[str] = [
        "name",
        "slug",
        "description",
        "price",
        "sale_price",
        "min_price",
        "max_price",
        "sku",
        "quantity",
        "in_stock",
        "is_taxable",
        "status",
        "product_type",
        "unit",
        "image",
        "gallery",
    ]

    product, has_updated = model_update(instance=product, fields=non_side_effect_fields, data=data)

    return product


@transaction.atomic
def product_delete(*, product_id: str) -> None:
    product = get_object(Product, id=product_id)
    product.delete()
    return None
