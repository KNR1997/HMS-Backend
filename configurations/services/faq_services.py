from typing import List

from django.db import transaction

from accounts.models import BaseUser
from common.services import model_update
from common.utils import get_object
from configurations.models import FAQ


@transaction.atomic
def faq_create(*, faq_title: str,
               slug: str = None,
               faq_description: str = None,
               faq_type: str = None,
               issued_by: str = None,
               ) -> FAQ:
    faq = FAQ.objects.create(faq_title=faq_title,
                             slug=slug,
                             faq_description=faq_description,
                             faq_type=faq_type,
                             issued_by=issued_by,
                             )

    return faq


@transaction.atomic
def faq_update(*, faq: FAQ, data, updated_by: BaseUser) -> FAQ:
    non_side_effect_fields: List[str] = [
        "faq_title",
        "slug",
        "faq_description",
        "faq_type",
        "issued_by",
    ]

    # all_fields = non_side_effect_fields + ["type", "department", "parent"]
    faq, has_updated = model_update(instance=faq, fields=non_side_effect_fields, data=data)

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...
    # if "updated_by" not in non_side_effect_fields:
    #     room.save(update_fields=["updated_by"])

    return faq


@transaction.atomic
def faq_delete(*, slug: str) -> None:
    faq = get_object(FAQ, slug=slug)
    faq.delete()
    return None
