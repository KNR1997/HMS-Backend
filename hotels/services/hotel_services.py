from typing import List

from django.db import transaction

from common.services import model_update
from hotels.models import Hotel


@transaction.atomic
def hotel_update(*, hotel: Hotel, data) -> Hotel:
    non_side_effect_fields: List[str] = [
        "name",
        "location",
        "description",
    ]

    # all_fields = non_side_effect_fields + ["type", "department", "parent"]
    hotel, has_updated = model_update(instance=hotel, fields=non_side_effect_fields, data=data)

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...
    # if "updated_by" not in non_side_effect_fields:
    #     room.save(update_fields=["updated_by"])

    return hotel