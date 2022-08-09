from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import PasswordChangeForm


from .forms import UserCreationForm


def register(request):
    """Регистрация нового пользователя"""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('toys:toys')

    context = {'form': form}
    return render(request, 'registration/register.html', context)


def profile_changed(request):
    """Переадресация на страницу с инфой об успешном изменении профиля"""
    return render(request, 'registration/profile_changed.html')


def password_changed(request):
    """Переадресация на страницу с инфой об успешном изменении пароля"""
    return render(request, 'registration/password_changed.html')


def profile(request):
    """Профиль пользователя, где он может редактировать свои данные."""
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
    return render(request, 'registration/profile.html', context)
