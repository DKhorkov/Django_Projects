from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


# Все, что ниже, необходимо для корректной работы админки после переопределения пользователя в users.models.
User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    pass
