from django.db.models import QuerySet

from configurations.models import FAQ


def faq_list(*, filters=None) -> QuerySet[FAQ]:
    filters = filters or {}

    qs = FAQ.objects.all()

    return qs