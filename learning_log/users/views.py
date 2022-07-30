from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def register(request):
    """Регистрация нового пользователя."""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():

            # Сохранение нового пользователя и дальнейшая авторизация:
            new_user = form.save()
            login(request, new_user)

            return redirect('learning_logs:topics')

    context = {'form': form}

    # Если указать путь шаблона "users/register.html" - будет ошибка, ибо шаблон не в папке пользователей.
    return render(request, 'registration/register.html', context)
