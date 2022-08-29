from django.contrib.auth.forms import (UserCreationForm as DjangoUserCreationForm,
                                       AuthenticationForm as DjangoAuthenticationForm)
from django.contrib.auth import get_user_model, authenticate
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .utils import send_email_for_verify
from natalia_toys.settings import DATE_INPUT_FORMATS

User = get_user_model()


class UserCreationForm(DjangoUserCreationForm):
    """Форма создания нового пользователя, наследуемая от стандартной формы создания пользователя, но с учетом
    обновленной модели пользователя (телефон, день рождения, email в качестве логина)."""
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )
    phone = forms.CharField(label=_('Номер телефона'), max_length=11, required=True)
    first_name = forms.CharField(max_length=30, label=_("Имя"))
    last_name = forms.CharField(max_length=30, label=_('Фамилия'))
    birthday = forms.DateField(label=_('Дата рождения в формате "день.месяц.год"'), input_formats=DATE_INPUT_FORMATS)

    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = ['username', 'email', "first_name", "last_name", "phone", "birthday"]


class UpdateUserForm(forms.ModelForm):
    """Форма обновления профиля пользователя, наследуемая от стандартной формы обновления пользователя, но с учетом
    обновленной модели пользователя (телефон, день рождения, email в качестве логина)."""
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label=_('Номер телефона'), max_length=11, required=True)
    first_name = forms.CharField(max_length=30, label=_("Имя"), widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, label=_('Фамилия'),
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    birthday = forms.DateField(label=_('Дата рождения в формате "день-месяц-год"'), input_formats=DATE_INPUT_FORMATS)

    class Meta:
        model = User
        fields = ['username', 'email', "first_name", "last_name", "phone", "birthday"]


class AuthenticationForm(DjangoAuthenticationForm):
    """Обновленная форма аутентификации пользователя, наследуемая от стандартной формы аутентификации пользователя,
     но с учетом обновленной модели пользователя, когда необходимо обрабатывать email в качестве логина."""

    def clean(self):
        """Переписываем метод стандартной формы аутентификации пользователя, чтобы обрабатывалась
        верификация почты."""
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)

            try:
                # Проверка верификации почты. Если нет, будет вызвана ошибка и сообщение для пользователя.
                if not self.user_cache.email_verified:
                    send_email_for_verify(self.request, self.user_cache)
                    raise ValidationError(
                        # Ниже написано сообщение об ошибке, которое получил юзер, если не прошел верификацию почты:
                        'Вы не подтвердили адрес электронной почты. '
                        'Пожалуйста, проверьте указанную при регистрации почту.',
                        code='invalid_login',
                    )

                # Стандартная часть базовой формы аутентификации Джанго:
                if self.user_cache is None:
                    raise self.get_invalid_login_error()
                else:
                    self.confirm_login_allowed(self.user_cache)

            # Проверка корректности заполнения полей электронной почты и пароля пользователя:
            except AttributeError:
                raise ValidationError(
                    # Ниже написано сообщение об ошибке, которое получил юзер, если не прошел верификацию почты:
                    'Ошибка авторизации: указан некорректный Email или пароль. Пожалуйста, попробуйте снова:',
                    code='invalid_login',
                )
        return self.cleaned_data
