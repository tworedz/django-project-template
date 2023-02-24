from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q


class UserManager(BaseUserManager):
    """Custom user manager for User model with an email as a username"""

    use_in_migrations = True

    def _create_user(self, phone: str, password: str, **extra_fields):
        if not phone:
            raise ValueError("The given value must be set")
        user = self.model(phone_number=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)


class AppUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(Q(is_staff=True) | Q(is_superuser=True))


class User(AbstractUser):
    """Пользователь"""

    class Genders(models.TextChoices):
        FEMALE = "female", "Женский"
        MALE = "male", "Мужской"

    username = None
    email = None
    phone_number = models.CharField("номер телефона", max_length=30, unique=True)
    first_name = models.CharField("Имя", max_length=30, null=True)
    last_name = models.CharField("Фамилия", max_length=35, null=True, blank=True)
    father_name = models.CharField("Отчество", max_length=35, null=True, blank=True)
    birth_date = models.DateField("Дата рождения", null=True)
    gender = models.CharField("Пол", max_length=6, choices=Genders.choices, null=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = UserManager()
    app_users = AppUserManager()

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self) -> str:
        return self.phone_number
