from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from toys.models import Toy
from .cart import Cart
from .forms import CartAddToyForm


@require_POST
def cart_add(request, toy_id):
    """Представление для добавления игрушки (с учетом выбранного количества штук данной игрушки) в корзину пользователя
    на вкладке каталог. Если пользователь обновляет количество уже находящейся в корзине игрушки на вкладке детальной
    информации о корзине, то происходит обновление данной вкладки, а не редирект на каталог."""
    cart = Cart(request)
    toy = get_object_or_404(Toy, id=toy_id)
    form = CartAddToyForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add_to_cart(toy=toy, quantity=cd['quantity'], update_quantity=cd['update'])
        if cd['update']:
            return redirect('cart:cart_detail')
    return redirect('toys:toys')


def cart_remove(request, toy_id):
    """Представление для удаления выбранной игрушки из корзины пользователя и обновление страницы детального содержимого
    корзины."""
    cart = Cart(request)
    toy = get_object_or_404(Toy, id=toy_id)
    cart.remove_from_cart(toy)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """Представление для просмотра содержимого корзины, где пользователь также может обновлять количество выбранных
    игрушек или вовсе удалить выбранную игрушку из корзины, а также начать процесс оформления заказа."""
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddToyForm(initial={'quantity': item['quantity'], 'update': True})

    context = {'cart': cart}
    return render(request, 'cart/detail.html', context)
