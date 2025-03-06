from typing import List

from django.db import transaction

from common.services import model_update
from common.utils import get_object
from products.models import Tag


@transaction.atomic
def tag_create(*, name: str,
               slug: str = None,
               details: str = None,
               image: str = None,
               icon: str = None,
               ) -> Tag:
    tag = Tag.objects.create(name=name,
                             slug=slug,
                             details=details,
                             image=image,
                             icon=icon,
                             )

    return tag


@transaction.atomic
def tag_update(*, tag: Tag, data) -> Tag:
    non_side_effect_fields: List[str] = [
        "name",
        "slug",
        "details",
        "image",
        "icon",
    ]

    tag, has_updated = model_update(instance=tag, fields=non_side_effect_fields, data=data)

    return tag


@transaction.atomic
def tag_delete(*, tag_id: str) -> None:
    tag = get_object(Tag, id=tag_id)
    tag.delete()
    return None
