from django.db import models
from django.db.models import F, Q
from django.utils import timezone

# from accounts.models import BaseUser


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SimpleModel(models.Model):
    """
    This is a basic model used to illustrate a many-to-many relationship
    with RandomModel.
    """

    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)


class RandomModel(BaseModel):
    """
    This is an example model, to be used as reference in the Styleguide,
    when discussing model validation via constraints.
    """

    start_date = models.DateField()
    end_date = models.DateField()

    simple_objects = models.ManyToManyField(
        SimpleModel, blank=True, related_name="random_objects"
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="start_date_before_end_date", check=Q(start_date__lt=F("end_date"))
            )
        ]


# class AuditableModel(models.Model):
#     """
#     Abstract model that tracks who created and last updated a record.
#     Inherits timestamp fields from BaseModel.
#     """
#
#     created_by = models.ForeignKey(
#         BaseUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_%(class)s"
#     )
#     updated_by = models.ForeignKey(
#         BaseUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_%(class)s"
#     )
#
#     class Meta:
#         abstract = True
