from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.create_order, name='create_order'),
    path('orders_history', views.orders_history, name='orders_history')
]