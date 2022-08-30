from django.db import models
from django.conf import settings

from toys.models import Toy


class Order(models.Model):
    """Модель для заказа, который пользователь оформляет, когда выбрал все необходимые игрушки и хочет их приобрести."""

    #  Чтобы работал внешний ключ на пользователя, нужно создавать его именно таким образом, а не через импорт модели:
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)

    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField()
    country = models.CharField(max_length=40, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    address = models.CharField(max_length=250, verbose_name='Адрес', help_text='Улица, дом, квартира')
    postal_code = models.IntegerField(verbose_name='Почтовый индекс')
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ номер {self.id}'

    def get_total_cost(self):
        """Метод для определения общей суммы заказа. Необходим для отправки чека покупателю и уведомления владельцу о
        размере совершенного покупателем заказа. Также данный метод необходим, если заказ уже был оформлен, но не
        оплачен: в таком случае, он будет виден для пользователя в истории заказов и пользователь сможет завершить
        процедуру покупки игрушек (вместо стоимости игрушек в корзине будет использована сумма заказа с помощью этого
        метода)."""
        return sum(item.get_cost() for item in self.items.all())

    def get_number_of_bought_toys(self):
        """Метод для определения кол-ва игрушек в заказе. Необходим для отправки чека покупателю и уведомления владельцу
        о количестве приобретенных покупателем игрушек."""
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    """Модель для игрушки в заказе, который собирается оформить пользователь."""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    toy = models.ForeignKey(Toy, related_name='order_items', on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        """Метод для определения стоимости по одной номенклатуре (типу игрушки)."""
        return self.price * self.quantity
