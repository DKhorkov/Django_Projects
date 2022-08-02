import os

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Toy
from .forms import ToyForm

# Create your views here.


def check_owner(request):
    """Проверка, что пользователь является владельцев сайта"""
    if not request.user.username == 'NGuliaeva':
        raise Http404


def main_page(request):
    """Домашняя страница сайта"""
    return render(request, 'toys/main_page.html')


def toys(request):
    """Страница с каталогом игрушек"""
    toys = Toy.objects.all()
    context = {'toys': toys}
    return render(request, 'toys/toys.html', context)


@login_required()
def new_toy(request):
    """Размещение новой игрушки"""
    check_owner(request)

    if request.method != 'POST':
        form = ToyForm()
    else:
        form = ToyForm(request.POST, request.FILES)  # Обязательно добавить request.FILES для корректной рабоыт формы

        if form.is_valid():
            form.save()
            return redirect('toys:toys')

    context = {'form': form}
    return render(request, 'toys/new_toy.html', context)


@login_required()
def delete_toy(request, toy_id):
    """Удаление блога"""
    check_owner(request)

    toy = Toy.objects.get(id=toy_id)
    os.remove(toy.image.path)  # Удаляет изображение из БД, когда удаляется запись, к которой привязано это изображение.
    toy.delete()
    return redirect('toys:toys')


@login_required()
def edit_toy(request, toy_id):
    check_owner(request)

    toy = Toy.objects.get(id=toy_id)
    if request.method != 'POST':
        form = ToyForm(instance=toy)
    else:
        form = ToyForm(instance=toy, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('toys:toys')
    context = {'form': form, 'toy': toy}
    return render(request, 'toys/edit_toy.html', context)
