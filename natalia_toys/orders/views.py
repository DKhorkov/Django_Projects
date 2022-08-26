from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from yookassa import Payment

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from payment.utils import send_cheque, send_notification


@login_required(login_url='/users/login/')
def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user_id = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         toy=item['toy'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            return redirect('payment:yandex_payment', order_id=order.id)
    else:
        form = OrderCreateForm

    context = {'cart': cart, 'form': form}
    return render(request, 'orders/create_order.html', context=context)


@login_required(login_url='/users/login/')
def orders_history(request):
    params = {'limit': 100}
    payment_list = Payment.list(params)
    orders = Order.objects.filter(user_id=request.user)
    order_items = OrderItem.objects.all()
    for order in orders:
        if not order.paid:
            payment_id = ''
            for item in payment_list.items:
                if item.description == f"Заказ номер {order.id}":
                    payment_id = item.id
                    break
            payment = Payment.find_one(payment_id)
            if payment.paid:
                order.paid = True
                order.save()
                send_notification(request, request.user, order, payment.id)
                send_cheque(request, request.user, order)

    context = {'orders': orders, 'order_items': order_items}
    return render(request, 'orders/orders_history.html', context=context)

