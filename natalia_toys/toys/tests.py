from django.test import TestCase
from django.urls import reverse

from .models import Toy
from .forms import ToyForm
from users.models import User


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


# Ниже расположены тесты для представлений.
class ToysViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/toys')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get('/toys')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/toys')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'toys/toys.html')


class CheckOwnerViewTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='test_user', email='someemail@gmail.com')

    def test_http404_raise_if_user_does_not_corresponds(self):
        user = User.objects.get(id=1)
        response = self.client.get('check_owner', kwargs={'request.user.username': user.username})
        self.assertEqual(response.status_code, 404)


class MainPageViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('toys:main_page'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('toys:main_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'toys/main_page.html')


class ContactsViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/contacts')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('toys:contacts'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('toys:contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'toys/contacts.html')


class ToyInfoViewTest(TestCase):

    def setUp(self):
        Toy.objects.create(title='elephant', price=100, description='Do u want to buy an elephant?', is_available=False)
        Toy.objects.create(title='turtle', price=200, is_available=True)

    def test_http404_raise_if_toy_is_not_available(self):
        toy = Toy.objects.get(id=1)
        response = self.client.get(reverse('toys:toy_info', kwargs={'toy_id': toy.id}))
        self.assertEqual(response.status_code, 404)

    def test_view_url_exists_at_desired_location(self):
        toy = Toy.objects.get(id=2)
        response = self.client.get(f'/toy_info/{toy.id}')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        toy = Toy.objects.get(id=2)
        response = self.client.get(reverse('toys:toy_info', kwargs={'toy_id': toy.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        toy = Toy.objects.get(id=2)
        response = self.client.get(reverse('toys:toy_info', kwargs={'toy_id': toy.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'toys/toy_info.html')


class NewToyViewTest(TestCase):

    def setUp(self):
        admin = User.objects.create(username='admin', email='admin@gmail.com', is_active=True)
        admin.set_password('some_pswrd1')
        admin.save()
        user = User.objects.create(username='random-user', email='some_user@gmail.com', is_active=True)
        user.set_password('user_pswrd1')
        user.save()

    def test_view_url_exists_at_desired_location(self):
        admin = User.objects.get(id=1)
        login = self.client.login(username='admin@gmail.com', password='some_pswrd1')
        response = self.client.get('/new_toy')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        admin = User.objects.get(id=1)
        login = self.client.login(username='admin@gmail.com', password='some_pswrd1')
        response = self.client.get(reverse('toys:new_toy'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        admin = User.objects.get(id=1)
        login = self.client.login(username='admin@gmail.com', password='some_pswrd1')
        response = self.client.get(reverse('toys:new_toy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'toys/new_toy.html')

    def test_valid_form(self):
        form = ToyForm(data={'title': 'elephant', 'price': 120, 'is_available': True})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = ToyForm(data={})
        self.assertFalse(form.is_valid())

    def test_login_user(self):
        admin = User.objects.get(id=1)
        login = self.client.login(username='admin@gmail.com', password='some_pswrd1')
        self.assertTrue(login)

    def test_saving_valid_form_with_post_method(self):
        admin = User.objects.get(id=1)
        login = self.client.login(username='admin@gmail.com', password='some_pswrd1')
        form_data = {'title': 'elephant', 'price': 120}
        form = ToyForm(data=form_data)
        response = self.client.post(reverse('toys:new_toy'))
        self.assertEqual(response.status_code, 200)

    def test_that_created_toy_was_saved(self):
        number_of_toys = len(Toy.objects.all())
        form_data = {'title': 'elephant', 'price': 120}
        form = ToyForm(data=form_data)
        form.save()
        number_of_toys = len(Toy.objects.all())
        self.assertEqual(number_of_toys, 1)

    def test_redirection_after_valid_form_post(self):
        admin = User.objects.get(id=1)
        login = self.client.login(username='admin@gmail.com', password='some_pswrd1')
        form_data = {'title': 'elephant', 'price': 120}
        form = ToyForm(data=form_data)
        response = self.client.post(reverse('toys:new_toy'), data=form_data)
        self.assertRedirects(response, expected_url='/toys')

    def test_raise_http404_if_user_not_correct(self):
        user = User.objects.get(id=2)
        login = self.client.login(username='some_user@gmail.com', password='user_pswrd1')
        form_data = {'title': 'elephant', 'price': 120}
        form = ToyForm(data=form_data)
        response = self.client.post(reverse('toys:new_toy'), data=form_data)
        self.assertEqual(response.status_code, 404)


class DeleteToyViewTest(TestCase):

    def setUp(self):
        admin = User.objects.create(username='admin', email='admin@gmail.com', is_active=True)
        admin.set_password('some_pswrd1')
        admin.save()
        user = User.objects.create(username='random-user', email='some_user@gmail.com', is_active=True)
        user.set_password('user_pswrd1')
        user.save()
        toy = Toy.objects.create(title='elephant', price=120, is_available=True)
        toy.save()

    def test_view_url_exists_at_desired_location(self):
        admin = User.objects.get(id=1)
        login = self.client.login(username='admin@gmail.com', password='some_pswrd1')
        toy = Toy.objects.get(id=1)
        response = self.client.get(f'/delete_toy/{toy.id}')
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        admin = User.objects.get(id=1)
        login = self.client.login(username='admin@gmail.com', password='some_pswrd1')
        toy = Toy.objects.get(id=1)
        response = self.client.get(reverse('toys:delete_toy', kwargs={'toy_id': toy.id}))
        self.assertEqual(response.status_code, 302)

    def test_that_toy_was_deleted(self):
        admin = User.objects.get(id=1)
        login = self.client.login(username='admin@gmail.com', password='some_pswrd1')
        toy = Toy.objects.get(id=1)
        response = self.client.post(reverse('toys:delete_toy', kwargs={'toy_id': toy.id}))
        number_of_toys = len(Toy.objects.all())
        self.assertEqual(number_of_toys, 0)

    def test_raise_http404_if_user_not_correct(self):
        user = User.objects.get(id=2)
        login = self.client.login(username='some_user@gmail.com', password='user_pswrd1')
        toy = Toy.objects.get(id=1)
        response = self.client.post(reverse('toys:delete_toy', kwargs={'toy_id': toy.id}))
        self.assertEqual(response.status_code, 404)


class EditToyViewTest(TestCase):

    def setUp(self):
        admin = User.objects.create(username='admin', email='admin@gmail.com', is_active=True)
        admin.set_password('some_pswrd1')
        admin.save()
        user = User.objects.create(username='random-user', email='some_user@gmail.com', is_active=True)
        user.set_password('user_pswrd1')
        user.save()
        toy = Toy.objects.create(title='elephant', price=120, is_available=True)
        toy.save()

    def test_view_url_exists_at_desired_location(self):
        admin = User.objects.get(id=1)
        login = self.client.login(username='admin@gmail.com', password='some_pswrd1')
        toy = Toy.objects.get(id=1)
        response = self.client.get(f'/edit_toy/{toy.id}')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        admin = User.objects.get(id=1)
        login = self.client.login(username='admin@gmail.com', password='some_pswrd1')
        toy = Toy.objects.get(id=1)
        response = self.client.get(reverse('toys:edit_toy', kwargs={'toy_id': toy.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        admin = User.objects.get(id=1)
        login = self.client.login(username='admin@gmail.com', password='some_pswrd1')
        toy = Toy.objects.get(id=1)
        response = self.client.get(reverse('toys:edit_toy', kwargs={'toy_id': toy.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'toys/edit_toy.html')

    def test_login_user(self):
        admin = User.objects.get(id=1)
        login = self.client.login(username='admin@gmail.com', password='some_pswrd1')
        self.assertTrue(login)

    def test_saving_form_with_no_changes(self):
        admin = User.objects.get(id=1)
        login = self.client.login(username='admin@gmail.com', password='some_pswrd1')
        toy = Toy.objects.get(id=1)
        form_data = {'date_added': toy.date_added, 'title': toy.title, 'price': toy.price,
                     'id': toy.id, 'is_available': toy.is_available}
        form = ToyForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('toys:edit_toy', kwargs={'toy_id': toy.id}))
        self.assertEqual(response.status_code, 200)

    def test_saving_edited_toy_with_valid_form(self):
        admin = User.objects.get(id=1)
        login = self.client.login(username='admin@gmail.com', password='some_pswrd1')
        toy = Toy.objects.get(id=1)
        form_data = {'date_added': toy.date_added, 'title': 'new elephant', 'price': toy.price,
                     'id': toy.id, 'is_available': False}
        form = ToyForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('toys:edit_toy', kwargs={'toy_id': toy.id}))
        self.assertEqual(response.status_code, 200)

    def test_redirect_after_editing_toy_with_valid_form(self):
        admin = User.objects.get(id=1)
        login = self.client.login(username='admin@gmail.com', password='some_pswrd1')
        toy = Toy.objects.get(id=1)
        form_data = {'date_added': toy.date_added, 'title': 'new elephant', 'price': toy.price,
                     'id': toy.id, 'is_available': False}
        form = ToyForm(data=form_data)
        response = self.client.post(reverse('toys:new_toy'), data=form_data)
        self.assertRedirects(response, expected_url='/toys')

    def test_invalid_form(self):
        admin = User.objects.get(id=1)
        login = self.client.login(username='admin@gmail.com', password='some_pswrd1')
        toy = Toy.objects.get(id=1)
        form_data = {'date_added': toy.date_added, 'title': [], 'price': toy.price,
                     'id': toy.id, 'is_available': False}
        form = ToyForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_raise_http404_if_user_not_correct(self):
        user = User.objects.get(id=2)
        login = self.client.login(username='some_user@gmail.com', password='user_pswrd1')
        toy = Toy.objects.get(id=1)
        response = self.client.post(reverse('toys:edit_toy', kwargs={'toy_id': toy.id}))
        self.assertEqual(response.status_code, 404)
