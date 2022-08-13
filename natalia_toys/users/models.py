from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """"""
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            "unique": _("Пользователь с таким email уже существует.")
        }
    )
    phone = models.CharField(_('phone number'), max_length=11, unique=True, error_messages={
            "unique": _("Пользователь с таким номером телефона уже существует.")
        })
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=50, blank=True)
    birthday = models.DateField(_("birth_date"), blank=True, default='1900-01-01')

    email_verified = models.BooleanField(default=False)  # Верификация почты через отправку письма.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
