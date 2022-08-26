from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http.response import Http404, HttpResponseRedirect
from yookassa import Configuration, Payment
import stripe
import requests
import uuid

from cart.cart import Cart
from orders.models import Order, OrderItem
from .utils import send_cheque, send_notification


Configuration.account_id = "935824"
Configuration.secret_key = "test_ijOeXonVYolMY8TuL4a0CJh-inaw33phNeqo-T7Lxtk"


def yandex_payment(request, order_id):
    cart = Cart(request)
    order_id = order_id
    total_price = int(cart.get_total_price())
    if total_price == 0:
        raise Http404

    payment = Payment.create({
        "amount": {
            "value": f'{total_price}.00',
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"https://127.0.0.1:8000/payment/payment_completed/{order_id}",
            "kwargs": {'order_id': order_id}
        },
        "capture": True,
        "description": f"Заказ номер {order_id}"
    }, uuid.uuid4())

    cart.clear()  # очистка корзины
    return HttpResponseRedirect(payment.confirmation.confirmation_url)


@login_required(login_url='/users/login/')
def pay_order(request, order_id):
    order = Order.objects.get(id=order_id)
    total_price = order.get_total_cost()

    payment = Payment.create({
        "amount": {
            "value": total_price,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"https://127.0.0.1:8000/payment/payment_completed/{order_id}",
            "kwargs": {'order_id': order.id}
        },
        "capture": True,
        "description": f"Заказ номер {order.id}"
    }, uuid.uuid4())

    return HttpResponseRedirect(payment.confirmation.confirmation_url)


@login_required(login_url='/users/login/')
def payment_completed(request, order_id):
    order = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(id=order_id)
    params = {'limit': 100}
    payment_list = Payment.list(params)
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

    context = {'order': order}
    return render(request, 'payment/payment_completed.html', context=context)

# @login_required(login_url='/users/login/')
# def basket_view(request):
#     """Создание оплаты на основе платежной системы stripe."""
#     basket = Cart(request)
#     total_price = int(basket.get_total_price())
#     if total_price != 0:
#         # Используем API ЦБ РФ, чтобы получить текущий курс доллара для нашей оплаты.
#         data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
#         usd_exrate = data['Valute']['USD']['Value']
#
#         total_price = round(total_price / usd_exrate, 2)
#         total_price = str(total_price)
#         total_price = total_price.replace('.', '')
#         total_price = int(total_price)
#
#         stripe.api_key = \
#             'sk_test_51LZDREBE1Lvh7o47t4UKTiM7J2E2CN95n8yN4kYBT7oaHYRRC2d8hEqdJzeRibswD5tFjkeTYKE5hLcSWxlguLLU00PxQHqTE0'
#         intent = stripe.PaymentIntent.create(
#             amount=total_price,
#             currency='usd',
#             metadata={'userid': request.user.id}  # Необходимо для определения, какой пользователь совершил заказ.
#         )
#
#         context = {'client_secret': intent.client_secret}
#         return render(request, 'payment/create_order.html', context=context)
#
#     else:
#         raise Http404
