from django.test import TestCase
from django.urls import reverse
from django import forms

from toys.models import Toy
from.cart import Cart
from .forms import CartAddToyForm


class CartTest(TestCase):

    def setUp(self):
        toy_1 = Toy.objects.create(title='elephant', price=120, is_available=True)
        toy_2 = Toy.objects.create(title='rat', price=100, is_available=True)
        self.request = self.client.request()
        self.request.session = self.client.session

    def test_initialize_cart_clean_session(self):
        """
        The cart is initialized with a session that contains no cart.
        In the end it should have a variable cart which is an empty dict.
        """
        cart = Cart(self.request)
        self.assertEqual(cart.cart, {})

    def test_initialize_cart_filled_session(self):
        """
        The cart is initialized with a session that contains a cart.
        In the end it should have a variable cart which equal to the cart that
        is in the initial session.
        """
        existing_cart = {
            '1': {
                'price': 120,
                'quantity': 2
            },
        }
        self.request.session['cart'] = existing_cart
        cart = Cart(self.request)
        self.assertEqual(cart.cart, existing_cart)

    def test_cart_add_new_toy(self):
        toy = Toy.objects.get(id=1)
        cart = Cart(self.request)
        cart.add_to_cart(toy=toy, quantity=2, update_quantity=False,)
        new_cart = {
            '1': {
                'price': '120.00',
                'quantity': 2,
            },
        }
        self.assertEqual(cart.cart, new_cart)

    def test_cart_add_to_existing_quantity(self):
        """
        Test adding a quantity to an existing quantity.
        """
        toy = Toy.objects.get(id=1)
        cart = Cart(self.request)
        cart.add_to_cart(toy=toy, quantity=2, update_quantity=False, )
        cart_status = {
            '1': {
                'price': '120.00',
                'quantity': 2,
            },
        }
        self.assertEqual(cart.cart, cart_status)
        cart.add_to_cart(toy=toy, quantity=3, update_quantity=False, )
        new_cart = {
            '1': {
                'price': '120.00',
                'quantity': 5,
            },
        }
        self.assertEqual(cart.cart, new_cart)

    def test_cart_add_update_existing_quantity(self):
        """
        Test updating existing item quantity.
        """
        toy = Toy.objects.get(id=1)
        cart = Cart(self.request)
        cart.add_to_cart(toy=toy, quantity=2, update_quantity=False, )
        cart_status = {
            '1': {
                'price': '120.00',
                'quantity': 2,
            },
        }
        self.assertEqual(cart.cart, cart_status)
        cart.add_to_cart(toy=toy, quantity=5, update_quantity=True, )
        new_cart = {
            '1': {
                'price': '120.00',
                'quantity': 5,
            },
        }
        self.assertEqual(cart.cart, new_cart)

    def test_cart_len_function(self):
        toy_1 = Toy.objects.get(id=1)
        toy_2 = Toy.objects.get(id=2)
        cart = Cart(self.request)
        cart.add_to_cart(toy=toy_1, quantity=2, update_quantity=False, )
        cart.add_to_cart(toy=toy_2, quantity=1, update_quantity=False, )
        cart_length = cart.__len__()
        self.assertEqual(cart_length, 3)

    def test_cart_get_total_price_function(self):
        toy_1 = Toy.objects.get(id=1)
        toy_2 = Toy.objects.get(id=2)
        cart = Cart(self.request)
        cart.add_to_cart(toy=toy_1, quantity=2, update_quantity=False, )
        cart.add_to_cart(toy=toy_2, quantity=1, update_quantity=False, )
        cart_total_price = cart.get_total_price()
        self.assertEqual(cart_total_price, 340)

    def test_cart_remove_function(self):
        toy_1 = Toy.objects.get(id=1)
        toy_2 = Toy.objects.get(id=2)
        cart = Cart(self.request)
        cart.add_to_cart(toy=toy_1, quantity=2, update_quantity=False, )
        cart.add_to_cart(toy=toy_2, quantity=1, update_quantity=False, )
        cart_status = {
            '1': {
                'price': '120.00',
                'quantity': 2,
            },
            '2': {
                'price': '100.00',
                'quantity': 1,
            },
        }
        self.assertEqual(cart.cart, cart_status)
        cart.remove_from_cart(toy_2)
        new_cart = {
            '1': {
                'price': '120.00',
                'quantity': 2,
            },
        }
        self.assertEqual(cart.cart, new_cart)


class CartFormTest(TestCase):

    def test_form_quantity_choices(self):
        form = CartAddToyForm()
        quantity_choices = form.fields['quantity'].choices
        expected_choices = [(i, str(i)) for i in range(1, 6)]
        self.assertEqual(quantity_choices, expected_choices)

    def test_form_quantity_coerce(self):
        form = CartAddToyForm()
        quantity_coerce = form.fields['quantity'].coerce
        self.assertEqual(quantity_coerce, int)

    def test_form_update_required(self):
        form = CartAddToyForm()
        update_required = form.fields['update'].required
        self.assertFalse(update_required)

    def test_form_update_initial(self):
        form = CartAddToyForm()
        update_initial = form.fields['update'].initial
        self.assertFalse(update_initial)


class CartDetailViewTest(TestCase):

    def setUp(self):
        self.request = self.client.request()
        self.request.session = self.client.session

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')


class CartRemoveViewTest(TestCase):

    def setUp(self):
        toy_1 = Toy.objects.create(title='elephant', price=120, is_available=True)
        toy_2 = Toy.objects.create(title='rat', price=100, is_available=True)
        self.request = self.client.request()
        self.request.session = self.client.session

    def test_view_url_accessible_by_name_plus_redirection(self):
        toy = Toy.objects.get(id=1)
        cart = Cart(self.request)
        cart.add_to_cart(toy=toy, quantity=2, update_quantity=False, )
        response = self.client.get(reverse('cart:cart_remove', kwargs={'toy_id': toy.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart:cart_detail'))

    def test_http404_raise_if_not_correct_toy(self):
        response = self.client.get(reverse('cart:cart_remove', kwargs={'toy_id': 3}))
        self.assertEqual(response.status_code, 404)


class CartAddViewTest(TestCase):

    def setUp(self):
        toy_1 = Toy.objects.create(title='elephant', price=120, is_available=True)
        toy_2 = Toy.objects.create(title='rat', price=100, is_available=True)
        self.request = self.client.request()
        self.request.session = self.client.session

    def test_to_add_toy_with_not_correct_method(self):
        toy = Toy.objects.get(id=1)
        cart = Cart(self.request)
        cart.add_to_cart(toy=toy, quantity=2, update_quantity=False, )
        response = self.client.get(reverse('cart:cart_add', kwargs={'toy_id': toy.id}))
        self.assertEqual(response.status_code, 405)

    def test_view_url_accessible_by_name_plus_redirection(self):
        toy = Toy.objects.get(id=1)
        cart = Cart(self.request)
        cart.add_to_cart(toy=toy, quantity=2, update_quantity=False, )
        response = self.client.post(reverse('cart:cart_add', kwargs={'toy_id': toy.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('toys:toys'))

