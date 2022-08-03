from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from toys.models import Toy
from .cart import Cart
from .forms import CartAddToyForm


@require_POST
def cart_add(request, toy_id):
    """Форма для добавления товара в корзину и редирект на просмотр корзины."""
    cart = Cart(request)
    toy = get_object_or_404(Toy, id=toy_id)
    form = CartAddToyForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add_to_cart(toy=toy, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('toys:toys')


def cart_remove(request, toy_id):
    """Удаление из корзины игрушки, айди которой было получено, и дальнейший редирект на просмотр корзины."""
    cart = Cart(request)
    toy = get_object_or_404(Toy, id=toy_id)
    cart.remove_from_cart(toy)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """Просмотр содержимого корзины."""
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddToyForm(initial={'quantity': item['quantity'], 'update': True})

    context = {'cart': cart}
    return render(request, 'cart/detail.html', context)
