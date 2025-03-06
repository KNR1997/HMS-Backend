from typing import Optional

from accounts.models import User
from common.utils import get_object


def user_get(user_id) -> Optional[User]:
    user = get_object(User, id=user_id)

    return user