from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    """Форма для оформления заказа, когда пользователь в корзине начинает процесс оформления и оплаты выбранных
    игрушек."""
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'country', 'city', 'address', 'postal_code']
        