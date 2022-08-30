from decimal import Decimal
from django.conf import settings
from toys.models import Toy


class Cart(object):
    """Корзина пользователя для добавления в нее игрушек с целью дальнейшего оформления заказа и приобретения выбранных
     игрушек пользователем."""

    def __init__(self, request):
        """Метод инициализации основных аттрибутов корзины пользователя."""

        # Запоминаем текущую сессию и пытаемся обратиться к данным корзины:
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        # Если нет товаров в корзине, сохраняем пустую корзину:
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        """Метод итерации по элементам корзины (перебор игрушек в корзине) и получения игрушек из БД. В данном методе
        мы извлекаем экземпляры продукта, присутствующие в корзине, чтобы включить их в номенклатуры корзины.
        Далее мы проходим по элементам корзины, преобразуя цену номенклатуры обратно в десятичное число и
        добавляя атрибут "total_price" к каждому элементу."""
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
        """Метод для подсчета общего количества игрушек в корзине для отображения на навигационной панели."""
        return sum(item['quantity'] for item in self.cart.values())

    def add_to_cart(self, toy, quantity=1, update_quantity=False):
        """Метод для добавления пользователем игрушки в корзину. По умолчанию добавляет одну единицу товара
        (выбранной игрушки) в корзину, если пользователь не выбирал количество, а также, если в корзине нет данной
        номенклатуры (игрушки). Если такая номенклатура уже есть в корзине, то при повторном добавлении просто обновится
        количество выбранной игрушки."""
        toy_id = str(toy.id)  # В JSON ключами могут быть только строки, поэтому меняем тип.
        if toy_id not in self.cart:
            self.cart[toy_id] = {'quantity': 0, 'price': str(toy.price)}
        if update_quantity:
            self.cart[toy_id]['quantity'] = quantity
        else:
            self.cart[toy_id]['quantity'] += quantity
        self.save_the_cart()

    def save_the_cart(self):
        """Метод для корректного сохранения игрушки в корзине и ее отображения в т.ч. при обновлении текущей вкладки."""
        self.session.modified = True

    def remove_from_cart(self, toy):
        """Метод для удаления игрушки из корзины, если пользователь передумал приобретать данную игрушку."""
        toy_id = str(toy.id)
        if toy_id in self.cart:
            del self.cart[toy_id]
            self.save_the_cart()  # Сохраняем состояние корзины после удаления игрушки.

    def get_total_price(self):
        """Метод для подсчета общей суммы всех игрушек в корзине, необходимый для оформления заказа и дальнейшей
        оплаты выбранных игрушек пользователем."""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Метод для очистки содержимого корзины на основе текущей сессии пользователя."""
        del self.session[settings.CART_SESSION_ID]
        self.save_the_cart()
