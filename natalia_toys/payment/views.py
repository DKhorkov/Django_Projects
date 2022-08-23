from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import Http404, HttpResponseRedirect
from yookassa import Configuration, Payment
import stripe
import requests
import uuid

from cart.cart import Cart


Configuration.account_id = "935824"
Configuration.secret_key = "test_ijOeXonVYolMY8TuL4a0CJh-inaw33phNeqo-T7Lxtk"


def yandex_payment(request):
    cart = Cart(request)
    total_price = int(cart.get_total_price())
    payment = Payment.create({
        "amount": {
            "value": f'{total_price}.00',
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://127.0.0.1:8000"
        },
        "capture": True,
        "description": "Заказ №1"
    }, uuid.uuid4())

    cart.clear()  # очистка корзины
    return HttpResponseRedirect(payment.confirmation.confirmation_url)


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
