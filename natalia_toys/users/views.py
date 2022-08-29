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
    """Представление для обработки ссылки на подтверждение электронной почты, отправленной в рамках представления
    "register"."""

    def get(self, request, uidb64, token):
        """Функция для проверки токена пользователя, если он прошел проверку наличия в БД с помощью функции "get_user".
        Если все корректно, производится верификация email данного пользователя и его авторизация на сайте, после чего
        пользователь будет переадресован на страницу с уведомлением о том, что регистрация успешно завершена. В случае,
        если токен некорректный, пользователь получит уведомление об этом с помощью переадресации на представление
        "invalid_verify"."""
        user = self.get_user(uidb64)
        if user is not None and default_token_generator.check_token(user, token):
            user.email_verified = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('users:registration_complete')
        return redirect('users:invalid_verify')

    @staticmethod
    def get_user(uidb):
        """Функция для обработки "uid" из ссылки и возврат пользователя, если он есть в БД, либо ничего,
         если такого пользователя в БД нет."""
        try:
            uid = urlsafe_base64_decode(uidb).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user


def register(request):
    """Представление для регистрации нового пользователя на основе формы "UserCreationForm". Если форма заполнена
    корректно, производится аутентификация пользователя по email и паролю, а затем отправляется письмо на указанную
    пользователем почту для верификации и окончания регистрации. После отправки письма пользователь будет переадресован
    на страницу с уведомлением о том, что для завершения регистрации необходимо перейти по ссылке в письме."""
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
    """Представление для обработки шаблона "profile_changed" для уведомления пользователя об успешном изменении
    профиля"""
    return render(request, 'registration/profile_changed.html')


@login_required()
def password_changed(request):
    """Представление для обработки шаблона "password_changed" для уведомления пользователя об успешном изменении
    пароля"""
    return render(request, 'registration/password_changed.html')


@login_required()
def profile(request):
    """Представление для перехода на страничку профиля, в которой пользователь может увидеть и изменить свои данные
    учетной записи. Если форма заполнена корректно, то обновленные данные будут сохранены и обновлены в БД,
    а пользователь будет переадресован на страницу с уведомлением об успешном изменении профиля."""
    user = request.user

    if request.method != 'POST':
        user_form = UpdateUserForm(instance=user)
    else:
        user_form = UpdateUserForm(instance=user, data=request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('users:profile_changed')

    context = {'user_form': user_form}
    return render(request, 'registration/profile.html', context)


@login_required()
def change_password(request):
    """Представление для смены пароля пользователя на основе формы "PasswordChangeForm", в которую передается
    текущий пользователь. Если форма заполнена корректно, сохраняется новый пароль и производится авторизация
    пользователя на сайте на основе обновленных данных учетной записи, а также переадресация на представление об
    успешной смене пароля."""
    user = request.user

    if request.method != 'POST':
        form = PasswordChangeForm(user)
    else:
        form = PasswordChangeForm(user, data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('users:password_changed')

    context = {'form': form}
    return render(request, 'registration/change_password.html', context)


def registration_complete(request):
    """Представление для обработки шаблона "registration_complete" для уведомления пользователя об успешном
     завершении регистрации аккаунта на сайте."""
    return render(request, 'registration/registration_complete.html')


def invalid_verify(request):
    """Представление для обработки шаблона "invalid_verify" в случае, если ссылка с токеном для верификации,
    отправленная на почту пользователя при регистрации, уже устарела или была использована ранее."""
    return render(request, 'registration/invalid_verify.html')


def confirm_email(request):
    """Представление для обработки шаблона "confirm_email" после регистрации нового пользователя
    для уведомления данного пользователя о том, что для окончания регистрации ему необходимо пройти по ссылке,
    отправленной на электронную почту, указанную при регистрации."""
    return render(request, 'registration/confirm_email.html')
