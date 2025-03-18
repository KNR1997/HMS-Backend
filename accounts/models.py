from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group
from django.db import models

from common.models import BaseModel


# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth=None, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )
        user.set_password(password)
        user.save(using=self._db)

        # Assign user to the 'customer' group
        user.set_groups(is_superuser=False)

        return user

    def create_superuser(self, email, date_of_birth=None, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)

        # Assign user to the 'super_user' group
        user.set_groups(is_superuser=True)

        return user


class BaseUser(AbstractBaseUser, BaseModel, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # Change the related_name to avoid conflict
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_set",  # Change the related_name to avoid conflict
        blank=True,
    )

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def set_groups(self, is_superuser=False):
        """Assign user to the correct group."""
        group_name = "super_user" if is_superuser else "customer"
        group, _ = Group.objects.get_or_create(name=group_name)
        self.groups.add(group)
        self.save()
