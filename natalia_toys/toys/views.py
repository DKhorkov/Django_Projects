import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.generic import ListView

from .models import Toy
from .forms import ToyForm
from cart.forms import CartAddToyForm
from .filters import ToysFilter


def check_owner(request):
    """Проверка, что пользователь является владельцев сайта"""
    if not (request.user.username == 'NGuliaeva' or request.user.username == 'admin'):
        raise Http404


def main_page(request):
    """Домашняя страница сайта"""
    return render(request, 'toys/main_page.html')


class Toys(ListView):
    """Страница с каталогом игрушек и поиском по игрушкам с помощью фильтра."""
    model = Toy
    template_name = 'toys/toys.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['filter'] = ToysFilter(self.request.GET, queryset=self.get_queryset())
        return context


def toy_info(request, toy_id):
    """Подробная информация об игрушке."""
    toy = Toy.objects.get(id=toy_id)

    if not toy.is_available:
        raise Http404

    cart_toy_form = CartAddToyForm()
    context = {'toy': toy, 'cart_toy_form': cart_toy_form}
    return render(request, 'toys/toy_info.html', context)


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
    # Удаляет изображения из БД, когда удаляется запись, к которой привязано эти изображения.
    if toy.image_1:
        os.remove(toy.image_1.path)
    if toy.image_2:
        os.remove(toy.image_2.path)
    if toy.image_3:
        os.remove(toy.image_3.path)
    if toy.image_4:
        os.remove(toy.image_4.path)
    toy.delete()
    return redirect('toys:toys')


@login_required()
def edit_toy(request, toy_id):
    check_owner(request)

    toy = Toy.objects.get(id=toy_id)
    if request.method != 'POST':
        form = ToyForm(instance=toy)
    else:
        form = ToyForm(request.POST, request.FILES, instance=toy)
        if form.is_valid():
            form.save()
            return redirect('toys:toys')
    context = {'form': form, 'toy': toy}
    return render(request, 'toys/edit_toy.html', context)


def contacts(request):
    """Переход на страницу с контактной информацией"""
    return render(request, 'toys/contacts.html')

