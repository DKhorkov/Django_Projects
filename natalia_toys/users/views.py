from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model, authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views import View
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ValidationError


from .forms import UserCreationForm, UpdateUserForm, AuthenticationForm
from .utils import send_email_for_verify


User = get_user_model()


class MyLoginView(LoginView):
    """Переопределенное представление пользователя на основе переопределенной формы аутентификации."""
    form_class = AuthenticationForm


class EmailVerify(View):
    """Обработка ссылки для подтверждения электронной почты."""

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        # Проверка токена пользователя, если он прошел проверку наличия в БД.
        # Если все ок, подтверждаем почту, сохраняем изменения пользователя и авторизуем его:
        if user is not None and default_token_generator.check_token(user, token):
            user.email_verified = True
            user.save()
            login(request, user)
            return redirect('users:registration_complete')
        return redirect('users:invalid_verify')

    @staticmethod
    def get_user(uidb):
        """Обработка uid из ссылки и возврат пользователя и возвращать пользователя, если он есть в БД,
         либо ничего, если такого пользователя в БД нет."""
        try:
            uid = urlsafe_base64_decode(uidb).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user


def register(request):
    """Регистрация нового пользователя"""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()

            # Ниже происходит аутентификация пользователя в системе:
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            new_user = authenticate(email=email, password=password)

            send_email_for_verify(request, new_user)
            return redirect('users:confirm_email')

    context = {'form': form}
    return render(request, 'registration/register.html', context)


@login_required()
def profile_changed(request):
    """Переадресация на страницу с инфой об успешном изменении профиля"""
    return render(request, 'registration/profile_changed.html')


@login_required()
def password_changed(request):
    """Переадресация на страницу с инфой об успешном изменении пароля"""
    return render(request, 'registration/password_changed.html')


@login_required()
def profile(request):
    """Профиль пользователя, где он может редактировать свои данные."""
    user = request.user

    if request.method != 'POST':
        user_form = UpdateUserForm(instance=user)
    else:
        user_form = UpdateUserForm(instance=user, data=request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            login(request, new_user)
            return redirect('users:profile_changed')

    context = {'user_form': user_form}
    return render(request, 'registration/profile.html', context)


@login_required()
def change_password(request):
    """Представление для смены пароля пользователя."""
    user = request.user

    if request.method != 'POST':
        form = PasswordChangeForm(user)
    else:
        form = PasswordChangeForm(user, data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('users:password_changed')

    context = {'form': form}
    return render(request, 'registration/change_password.html', context)


def registration_complete(request):
    """Переадресация на страницу с инфой об успешном завершении регистрации"""
    return render(request, 'registration/registration_complete.html')


def invalid_verify(request):
    """Переадресация на страницу с инфой о том, что ссылка с токеном для верификации почты устарела."""
    return render(request, 'registration/invalid_verify.html')


def confirm_email(request):
    """Переадресация после регистрации нового пользователя на страницу с инфой о том,
     что для окончания регистрации ему необходимо пройти по ссылке, отправленной на электронную почту,
     указанную при регистрации."""
    return render(request, 'registration/confirm_email.html')
