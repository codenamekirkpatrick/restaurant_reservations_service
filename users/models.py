from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    """Пользователь"""

    username = None

    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    phone = PhoneNumberField(default="+7", verbose_name="Номер телефона", **NULLABLE)
    country = CountryField(
        default="RU", verbose_name="Страна", blank_label="(select country)"
    )
    about_me = models.TextField(verbose_name="О себе", **NULLABLE)
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Фото",
        default="users/avatars/default.jpg",
        **NULLABLE,
    )

    token = models.CharField(max_length=100, verbose_name="Token", **NULLABLE)
    notes = models.TextField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return self.email
