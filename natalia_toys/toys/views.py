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
    """Функция для проверки, является ли пользователь владельцем сайта. Используется в представлениях для редактирования
    и удаления экземпляров игрушек в каталоге. Если пользователь не админ или владелец, будет вызвана ошибка 404."""
    if not (request.user.username == 'NGuliaeva' or request.user.username == 'admin'):
        raise Http404


def main_page(request):
    """Представление для обработки шаблона главной (домашней) страницы сайта."""
    return render(request, 'toys/main_page.html')


class Toys(ListView):
    """Представление для обработки шаблона "toys", являющегося каталогом игрушек, где пользователь может посмотреть все
    доступные для приобретения игрушки."""
    model = Toy
    template_name = 'toys/toys.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        """Метод для поиска игрушек в каталоге согласно заданным критериям фильтрации."""
        context = super().get_context_data()
        context['filter'] = ToysFilter(self.request.GET, queryset=self.get_queryset())
        return context


def toy_info(request, toy_id):
    """Представление для обработки шаблона "toy_info" - подробной информации о каждой игрушке. Если игрушка имеется
    в наличии, пользователь может посмотреть детальную информацию об игрушке, а также добавить в корзину необходимое
    кол-во игрушек (1-5 согласно настройкам корзины). Если игрушки нет в наличии, а пользователь пытается добавить ее в
    корзину путем ручного ввода URL, то будет выведена ошибка 404."""
    toy = Toy.objects.get(id=toy_id)

    if not toy.is_available:
        raise Http404

    cart_toy_form = CartAddToyForm()
    context = {'toy': toy, 'cart_toy_form': cart_toy_form}
    return render(request, 'toys/toy_info.html', context)


@login_required()
def new_toy(request):
    """Представление для создания нового экземпляра игрушки на основе формы "ToyForm", если авторизованный пользователь
    является владельцем или админом. Если форма заполнена корректно, то экземпляр игрушки сохраняется в БД, а
    пользователь будет переадресован в каталог, где сразу сможет увидеть новую игрушку, которую только что создал."""
    check_owner(request)

    if request.method != 'POST':
        form = ToyForm()
    else:
        form = ToyForm(request.POST, request.FILES)  # Обязательно добавить request.FILES для корректной работы формы.

        if form.is_valid():
            form.save()
            return redirect('toys:toys')

    context = {'form': form}
    return render(request, 'toys/new_toy.html', context)


@login_required()
def delete_toy(request, toy_id):
    """Представление для удаления существующего в БД экземпляра игрушки, если
    авторизованный пользователь является владельцем или админом. При удалении игрушки также удаляются изображения
    (с целью оптимизации памяти), относящиеся к данной игрушке и хранящиеся в отдельном директории."""
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
    """Представление для редактирования существующего в БД экземпляра игрушки на основе формы "ToyForm", если
    авторизованный пользователь является владельцем или админом. Если форма заполнена корректно, то обновленный
    экземпляр игрушки сохраняется в БД, а пользователь будет переадресован в каталог, где сразу сможет увидеть
    обновленную игрушку."""
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
    """Представление для обработки шаблона "contacts", где пользователи смогут увидеть контактную информацию для связи
    с владельцем или разработчиком сайта по возникающим вопросам."""
    return render(request, 'toys/contacts.html')

