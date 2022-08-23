from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.yandex_payment, name='yandex_payment')
]
