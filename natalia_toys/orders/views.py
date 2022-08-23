from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


@login_required(login_url='/users/login/')
def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         toy=item['toy'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            return redirect('payment:yandex_payment')
    else:
        form = OrderCreateForm

    context = {'cart': cart, 'form': form}
    return render(request, 'orders/create_order.html', context=context)
