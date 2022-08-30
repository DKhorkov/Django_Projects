from django import forms

# Пользователь может купить не более 5 игрушек одного типа:
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 6)]


class CartAddToyForm(forms.Form):
    """Форма для добавления игрушки в корзину с учетом выбранного количества штук данной игрушки."""
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)

    # Скрытое поле для обновления и изменения количества игрушек пользователем:
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
