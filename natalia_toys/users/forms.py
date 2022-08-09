from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import gettext_lazy as _
from natalia_toys.settings import DATE_INPUT_FORMATS

User = get_user_model()


class UserCreationForm(UserCreationForm):
    """Измененный класс из-за изменения модели пользователя"""
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )
    name = forms.CharField(max_length=30, label=_("Имя"))
    surname = forms.CharField(max_length=30, label=_('Фамилия'))
    birthday = forms.DateField(label=_('Дата рождения в формате "день-месяц-год"'), input_formats=DATE_INPUT_FORMATS)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "name", "surname", "birthday")

