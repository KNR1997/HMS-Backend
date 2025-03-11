from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
            **kwargs,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email,
            password=password,
            **kwargs,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Permission(models.Model):
    class PermissionType(models.TextChoices):
        SUPER_ADMIN = 'super_admin', _('Super Admin')
        STORE_OWNER = 'store_owner', _('Store Owner')
        STAFF = 'staff', _('Staff')

    permission_type = models.CharField(
        max_length=20,
        choices=PermissionType.choices,
        unique=True,
        verbose_name=_('Permission Type')
    )

    def __str__(self):
        return self.get_permission_type_display()


class User(AbstractUser):
    permissions = models.ManyToManyField(
        Permission,
        related_name='users',
        blank=True,
        verbose_name=_('Permissions')
    )


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    address = models.CharField(verbose_name=_('Address'), max_length=255, blank=True, null=True)
    phone_number = models.CharField(verbose_name=_('Phone Number'), max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)

    def __str__(self):
        return f'{self.id} - {self.user.get_full_name()}'
