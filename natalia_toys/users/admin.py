from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm

# Все, что ниже, необходимо для корректной работы админки после переопределения пользователя в users.models.
User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    """Доработка создания пользователя внутри админки.
    Если не использовать код ниже, то в админке будет стандартная модель пользователя."""
    add_form = UserCreationForm  # Название переменной формы должно быть именно таким (см. базовую модель админа)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username",
                           "email",
                           "email_verified",
                           "phone",
                           "first_name",
                           "last_name",
                           "birthday",
                           "password1",
                           "password2"),
            },
        ),
    )

