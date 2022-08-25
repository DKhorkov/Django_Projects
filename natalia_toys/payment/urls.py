from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('payment/<order_id>', views.yandex_payment, name='yandex_payment'),
    path('payment_completed/<order_id>', views.payment_completed, name='payment_completed'),
    path('pay_order/<order_id>', views.pay_order, name='pay_order'),
]
