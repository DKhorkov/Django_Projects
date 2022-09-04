from django.test import TestCase

from .models import Order, OrderItem
from users.models import User
from toys.models import Toy
from .forms import OrderCreateForm


class OrderModelTest(TestCase):

    def setUp(self):
        admin = User.objects.create(username='admin', email='admin@gmail.com', email_verified=True)
        admin.set_password('some_pswrd1')
        admin.save()
        toy_1 = Toy.objects.create(title='rat', price=100, is_available=True)
        toy_2 = Toy.objects.create(title='cat', price=200, is_available=True)
        order = Order.objects.create(user_id=admin, first_name='test', last_name='user', email='testuser@gmail.com',
                                     country='USA', city='some city', address='Some Street', postal_code=199456)
        order_item_1 = OrderItem.objects.create(order=order, toy=toy_1, quantity=2, price=toy_1.price)
        order_item_2 = OrderItem.objects.create(order=order, toy=toy_2, quantity=1, price=toy_2.price)

    def test_order_was_created_correctly(self):
        number_of_orders = len(Order.objects.all())
        number_of_order_items = len(OrderItem.objects.all())
        self.assertEqual(number_of_orders, 1)
        self.assertEqual(number_of_order_items, 2)

    def test_order_name_is_order_number_plus_id(self):
        order = Order.objects.get(id=1)
        expected_order_name = 'Заказ номер 1'
        self.assertEqual(expected_order_name, order.__str__())

    def test_order_total_cost(self):
        order = Order.objects.get(id=1)
        total_cost = order.get_total_cost()
        self.assertEqual(total_cost, 400)

    def test_number_of_bought_toys(self):
        order = Order.objects.get(id=1)
        number_of_toys = order.get_number_of_bought_toys()
        self.assertEqual(number_of_toys, 3)

    def test_ordering_desc(self):
        order = Order.objects.get(id=1)
        ordering = order._meta.ordering
        self.assertEqual(ordering, ('-created',))

    def test_order_verbose_name(self):
        order = Order.objects.get(id=1)
        name = order._meta.verbose_name
        self.assertEqual(name, 'Заказ')

    def test_order_plural_verbose_name(self):
        order = Order.objects.get(id=1)
        plural_name = order._meta.verbose_name_plural
        self.assertEqual(plural_name, 'Заказы')

    def test_first_name_field_max_length(self):
        order = Order.objects.get(id=1)
        first_name_max_length = order._meta.get_field('first_name').max_length
        self.assertEqual(first_name_max_length, 50)

    def test_first_name_field_label(self):
        order = Order.objects.get(id=1)
        first_name_label = order._meta.get_field('first_name').verbose_name
        self.assertEqual(first_name_label, 'Имя')

    def test_last_name_field_max_length(self):
        order = Order.objects.get(id=1)
        last_name_max_length = order._meta.get_field('last_name').max_length
        self.assertEqual(last_name_max_length, 50)

    def test_last_name_field_label(self):
        order = Order.objects.get(id=1)
        last_name_label = order._meta.get_field('last_name').verbose_name
        self.assertEqual(last_name_label, 'Фамилия')

    def test_country_field_max_length(self):
        order = Order.objects.get(id=1)
        country_max_length = order._meta.get_field('country').max_length
        self.assertEqual(country_max_length, 40)

    def test_country_field_label(self):
        order = Order.objects.get(id=1)
        country_label = order._meta.get_field('country').verbose_name
        self.assertEqual(country_label, 'Страна')

    def test_city_field_max_length(self):
        order = Order.objects.get(id=1)
        city_max_length = order._meta.get_field('city').max_length
        self.assertEqual(city_max_length, 100)

    def test_city_field_label(self):
        order = Order.objects.get(id=1)
        city_label = order._meta.get_field('city').verbose_name
        self.assertEqual(city_label, 'Город')

    def test_address_field_max_length(self):
        order = Order.objects.get(id=1)
        address_max_length = order._meta.get_field('address').max_length
        self.assertEqual(address_max_length, 250)

    def test_address_field_label(self):
        order = Order.objects.get(id=1)
        address_label = order._meta.get_field('address').verbose_name
        self.assertEqual(address_label, 'Адрес')

    def test_address_field_help_text(self):
        order = Order.objects.get(id=1)
        address_help_text = order._meta.get_field('address').help_text
        self.assertEqual(address_help_text, 'Улица, дом, квартира')

    def test_postal_code_field_label(self):
        order = Order.objects.get(id=1)
        postal_code_label = order._meta.get_field('postal_code').verbose_name
        self.assertEqual(postal_code_label, 'Почтовый индекс')

    def test_created_field_auto_now_add(self):
        order = Order.objects.get(id=1)
        auto_now_add = order._meta.get_field('created').auto_now_add
        self.assertTrue(auto_now_add)

    def test_paid_field_default(self):
        order = Order.objects.get(id=1)
        paid_default = order._meta.get_field('paid').default
        self.assertFalse(paid_default)


class OrderItemModelTest(TestCase):

    def setUp(self):
        admin = User.objects.create(username='admin', email='admin@gmail.com', email_verified=True)
        admin.set_password('some_pswrd1')
        admin.save()
        toy = Toy.objects.create(title='rat', price=140, is_available=True)
        order = Order.objects.create(user_id=admin, first_name='test', last_name='user', email='testuser@gmail.com',
                                     country='USA', city='some city', address='Some Street', postal_code=199456)
        order_item = OrderItem.objects.create(order=order, toy=toy, quantity=4, price=toy.price)

    def test_order_item_name_is_id(self):
        order_item = OrderItem.objects.get(id=1)
        expected_order_item_name = '1'
        self.assertEqual(expected_order_item_name, order_item.__str__())

    def test_order_item_cost(self):
        order_item = OrderItem.objects.get(id=1)
        item_cost = order_item.get_cost()
        self.assertEqual(item_cost, 560)

    def test_price_field_max_digits(self):
        order_item = OrderItem.objects.get(id=1)
        max_digits = order_item._meta.get_field('price').max_digits
        self.assertEqual(max_digits, 10)

    def test_price_field_decimal_places(self):
        order_item = OrderItem.objects.get(id=1)
        decimal_places = order_item._meta.get_field('price').decimal_places
        self.assertEqual(decimal_places, 2)

    def test_quantity_field_default_value(self):
        order_item = OrderItem.objects.get(id=1)
        quantity_default_value = order_item._meta.get_field('quantity').default
        self.assertEqual(quantity_default_value, 1)


class OrderCreateFormTest(TestCase):

    def test_form_fields(self):
        form = OrderCreateForm()
        self.assertTrue(form.fields['first_name'])
        self.assertTrue(form.fields['last_name'])
        self.assertTrue(form.fields['email'])
        self.assertTrue(form.fields['country'])
        self.assertTrue(form.fields['city'])
        self.assertTrue(form.fields['address'])
        self.assertTrue(form.fields['postal_code'])
