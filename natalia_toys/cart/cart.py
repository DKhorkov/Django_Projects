from decimal import Decimal
from django.conf import settings
from toys.models import Toy


class Cart(object):
    """Корзина для добавления в нее игрушек с целью дальнейшего оформления заказа."""

    def __init__(self, request):
        """Инициализация корзины."""

        # Запоминаем текущую сессию и пытаемся обратиться к данным корзины:
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        # Если нет товаров в корзине, сохраняем пустую корзину:
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        """Перебираем элементы корзины и получаем их из БД."""
        toy_ids = self.cart.keys()
        # Получаем товары и добавляем их в корзину:
        toys = Toy.objects.filter(id__in=toy_ids)

        cart = self.cart.copy()
        for toy in toys:
            cart[str(toy.id)]['toy'] = toy

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item  # Вместо return используем yield для постепенного подгружения на сайт информации об игрушке.

    def __len__(self):
        """Считаем количество товаров в корзине."""
        return sum(item['quantity'] for item in self.cart.values())

    def add_to_cart(self, toy, quantity=1, update_quantity=False):
        """Метод добавления игрушки в корзину. Добавляет по умолчанию +1 к товарам.
        Но можно обновить количество вручную."""
        toy_id = str(toy.id)  # В JSON ключами могут быть только строки, поэтому меняем тип.
        if toy_id not in self.cart:
            self.cart[toy_id] = {'quantity': 0, 'price': str(toy.price)}
        if update_quantity:
            self.cart[toy_id]['quantity'] = quantity
        else:
            self.cart[toy_id]['quantity'] += quantity
        self.save_the_cart()

    def save_the_cart(self):
        """Сохраняет товар в корзине."""
        self.session.modified = True

    def remove_from_cart(self, toy):
        """Удаляет игрушку из корзины."""
        toy_id = str(toy.id)
        if toy_id in self.cart:
            del self.cart[toy_id]
            self.save_the_cart()  # Сохраняем состояние корзины после удаления игрушки.

    def get_total_price(self):
        """Вычисление общей стоимости товаров в корзине."""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Очищает корзину в сессии."""
        del self.session[settings.CART_SESSION_ID]
        self.save_the_cart()
