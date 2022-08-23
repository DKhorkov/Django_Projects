from django.db import models

from toys.models import Toy
from users.models import User


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
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
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    toy = models.ForeignKey(Toy, related_name='order_items', on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity


