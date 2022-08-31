from django.test import TestCase

from .models import Toy
from .forms import ToyForm
from . import views


class ToyModelTest(TestCase):
    """Тестирование модели игрушки."""

    @classmethod
    def setUpTestData(cls):
        """Настройка не модифицированных объектов, используемых всеми методами тестирования."""
        Toy.objects.create(title='elephant', price=100, description='Do u want to buy an elephant?', is_available=True)

    def test_title_max_length(self):
        toy = Toy.objects.get(id=1)
        title_max_length = toy._meta.get_field('title').max_length
        self.assertEqual(title_max_length, 50)

    def test_title_label(self):
        toy = Toy.objects.get(id=1)
        title_label = toy._meta.get_field('title').verbose_name
        self.assertEqual(title_label, 'Название')

    def test_title_help_text(self):
        toy = Toy.objects.get(id=1)
        title_help_text = toy._meta.get_field('title').help_text
        self.assertEqual(title_help_text, 'Название игрушки')

    def test_if_toy_is_available(self):
        toy = Toy.objects.get(id=1)
        self.assertTrue(toy.is_available)

    def test_toy_availability_help_text(self):
        toy = Toy.objects.get(id=1)
        availability_help_text = toy._meta.get_field('is_available').help_text
        self.assertEqual(availability_help_text, 'Имеется в наличии?')

    def test_date_added_auto_now_add(self):
        toy = Toy.objects.get(id=1)
        auto_now_add = toy._meta.get_field('date_added').auto_now_add
        self.assertTrue(auto_now_add)

    def test_if_description_may_be_blank(self):
        toy = Toy.objects.get(id=1)
        blank_description = toy._meta.get_field('description').blank
        self.assertTrue(blank_description)

    def test_description_help_text(self):
        toy = Toy.objects.get(id=1)
        description_help_text = toy._meta.get_field('description').help_text
        self.assertEqual(description_help_text, 'Описание игрушки')

    def test_description_label(self):
        toy = Toy.objects.get(id=1)
        description_label = toy._meta.get_field('description').verbose_name
        self.assertEqual(description_label, 'Описание')

    def test_price_max_digits(self):
        toy = Toy.objects.get(id=1)
        price_max_digits = toy._meta.get_field('price').max_digits
        self.assertEqual(price_max_digits, 10)

    def test_price_decimal_places(self):
        toy = Toy.objects.get(id=1)
        price_decimal_places = toy._meta.get_field('price').decimal_places
        self.assertEqual(price_decimal_places, 2)

    def test_price_help_text(self):
        toy = Toy.objects.get(id=1)
        price_help_text = toy._meta.get_field('price').help_text
        self.assertEqual(price_help_text, 'Цена игрушки')

    def test_price_label(self):
        toy = Toy.objects.get(id=1)
        price_label = toy._meta.get_field('price').verbose_name
        self.assertEqual(price_label, 'Цена')

    def test_image_1_directory_for_uploading(self):
        toy = Toy.objects.get(id=1)
        image_1_directory = toy._meta.get_field('image_1').upload_to
        self.assertEqual(image_1_directory, 'images/')

    def test_image_1_help_text(self):
        toy = Toy.objects.get(id=1)
        image_1_help_text = toy._meta.get_field('image_1').help_text
        self.assertEqual(image_1_help_text, 'Изображение 1')

    def test_if_image_1_may_be_blank(self):
        toy = Toy.objects.get(id=1)
        blank_image_1 = toy._meta.get_field('image_1').blank
        self.assertTrue(blank_image_1)

    def test_image_2_directory_for_uploading(self):
        toy = Toy.objects.get(id=1)
        image_2_directory = toy._meta.get_field('image_2').upload_to
        self.assertEqual(image_2_directory, 'images/')

    def test_image_2_help_text(self):
        toy = Toy.objects.get(id=1)
        image_2_help_text = toy._meta.get_field('image_2').help_text
        self.assertEqual(image_2_help_text, 'Изображение 2')

    def test_if_image_2_may_be_blank(self):
        toy = Toy.objects.get(id=1)
        blank_image_2 = toy._meta.get_field('image_2').blank
        self.assertTrue(blank_image_2)

    def test_image_3_directory_for_uploading(self):
        toy = Toy.objects.get(id=1)
        image_3_directory = toy._meta.get_field('image_3').upload_to
        self.assertEqual(image_3_directory, 'images/')

    def test_image_3_help_text(self):
        toy = Toy.objects.get(id=1)
        image_3_help_text = toy._meta.get_field('image_3').help_text
        self.assertEqual(image_3_help_text, 'Изображение 3')

    def test_if_image_3_may_be_blank(self):
        toy = Toy.objects.get(id=1)
        blank_image_3 = toy._meta.get_field('image_3').blank
        self.assertTrue(blank_image_3)

    def test_image_4_directory_for_uploading(self):
        toy = Toy.objects.get(id=1)
        image_4_directory = toy._meta.get_field('image_4').upload_to
        self.assertEqual(image_4_directory, 'images/')

    def test_image_4_help_text(self):
        toy = Toy.objects.get(id=1)
        image_4_help_text = toy._meta.get_field('image_4').help_text
        self.assertEqual(image_4_help_text, 'Изображение 4')

    def test_if_image_4_may_be_blank(self):
        toy = Toy.objects.get(id=1)
        blank_image_4 = toy._meta.get_field('image_4').blank
        self.assertTrue(blank_image_4)

    def test_object_name_is__title(self):
        toy = Toy.objects.get(id=1)
        expected_object_name = 'elephant'
        self.assertEqual(expected_object_name, toy.__str__())


class ToyFormTest(TestCase):
    """Тестирование формы игрушки."""

    def test_form_fields(self):
        form = ToyForm()
        self.assertTrue(form.fields['title'])
        self.assertTrue(form.fields['price'])
        self.assertTrue(form.fields['image_1'])
        self.assertTrue(form.fields['image_2'])
        self.assertTrue(form.fields['image_3'])
        self.assertTrue(form.fields['image_4'])
        self.assertTrue(form.fields['description'])
        self.assertTrue(form.fields['is_available'])

    def test_form_description_widget(self):
        form = ToyForm()
        description_cols = form._meta.widgets['description'].attrs['cols']
        self.assertEqual(description_cols, 100)

    def test_form_labels(self):
        form = ToyForm()
        self.assertTrue(form.fields['title'].label is None or form.fields['title'].label == 'Название')
        self.assertTrue(form.fields['price'].label is None or form.fields['price'].label == 'Цена')
        self.assertTrue(form.fields['description'].label is None or form.fields['description'].label == 'Описание')
        self.assertEqual(form.fields['image_1'].label, 'Изображение 1')
        self.assertEqual(form.fields['image_2'].label, 'Изображение 2')
        self.assertEqual(form.fields['image_3'].label, 'Изображение 3')
        self.assertEqual(form.fields['image_4'].label, 'Изображение 4')
        self.assertEqual(form.fields['is_available'].label, 'Имеется в наличии?')
