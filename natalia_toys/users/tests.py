from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user

from .models import User
from .forms import UpdateUserForm, UserCreationForm


class UserModelTest(TestCase):
    """Тестирование модели пользователя."""

    @classmethod
    def setUpTestData(cls):
        """Настройка не модифицированных объектов, используемых всеми методами тестирования."""
        user = User.objects.create(username='admin', email='admin@gmail.com', is_active=True)
        user.set_password('some_pswrd1')
        user.save()

    def test_object_name_is_email(self):
        user = User.objects.get(id=1)
        expected_object_name = 'admin@gmail.com'
        self.assertEqual(expected_object_name, user.__str__())

    def test_email_field_label(self):
        user = User.objects.get(id=1)
        email_label = user._meta.get_field('email').verbose_name
        self.assertEqual(email_label, 'email адрес')

    def test_email_field_unique(self):
        user = User.objects.get(id=1)
        email_unique = user._meta.get_field('email').unique
        self.assertTrue(email_unique)

    def test_phone_field_label(self):
        user = User.objects.get(id=1)
        phone_label = user._meta.get_field('phone').verbose_name
        self.assertEqual(phone_label, 'phone number')

    def test_phone_field_unique(self):
        user = User.objects.get(id=1)
        phone_unique = user._meta.get_field('phone').unique
        self.assertTrue(phone_unique)

    def test_phone_field_null(self):
        user = User.objects.get(id=1)
        phone_null = user._meta.get_field('phone').null
        self.assertTrue(phone_null)

    def test_phone_field_max_length(self):
        user = User.objects.get(id=1)
        phone_field_max_length = user._meta.get_field('phone').max_length
        self.assertEqual(phone_field_max_length, 11)

    def test_first_name_field_label(self):
        user = User.objects.get(id=1)
        first_name_label = user._meta.get_field('first_name').verbose_name
        self.assertEqual(first_name_label, 'имя')

    def test_first_name_field_max_length(self):
        user = User.objects.get(id=1)
        first_name_max_length = user._meta.get_field('first_name').max_length
        self.assertEqual(first_name_max_length, 30)

    def test_first_name_field_may_be_blank(self):
        user = User.objects.get(id=1)
        first_name_blank = user._meta.get_field('first_name').blank
        self.assertTrue(first_name_blank)

    def test_last_name_field_label(self):
        user = User.objects.get(id=1)
        last_name_label = user._meta.get_field('last_name').verbose_name
        self.assertEqual(last_name_label, 'фамилия')

    def test_last_name_field_max_length(self):
        user = User.objects.get(id=1)
        last_name_max_length = user._meta.get_field('last_name').max_length
        self.assertEqual(last_name_max_length, 50)

    def test_last_name_field_may_be_blank(self):
        user = User.objects.get(id=1)
        last_name_blank = user._meta.get_field('last_name').blank
        self.assertTrue(last_name_blank)

    def test_birthday_field_label(self):
        user = User.objects.get(id=1)
        birthday_label = user._meta.get_field('birthday').verbose_name
        self.assertEqual(birthday_label, 'birth_date')

    def test_birthday_field_may_be_blank(self):
        user = User.objects.get(id=1)
        birthday_blank = user._meta.get_field('birthday').blank
        self.assertTrue(birthday_blank)

    def test_birthday_field_default(self):
        user = User.objects.get(id=1)
        birthday_default = user._meta.get_field('birthday').default
        self.assertEqual(birthday_default, '1900-01-01')

    def test_email_verified_field_default(self):
        user = User.objects.get(id=1)
        email_verified_default = user._meta.get_field('email_verified').default
        self.assertFalse(email_verified_default)

    def test_username_field(self):
        user = User.objects.get(id=1)
        username_field = user.USERNAME_FIELD
        self.assertEqual(username_field, 'email')

    def test_required_fields(self):
        user = User.objects.get(id=1)
        required_fields = user.REQUIRED_FIELDS
        self.assertEqual(required_fields, ['username'])


class AuthenticationFormTest(TestCase):

    def setUp(self):
        self.user_not_verified = User.objects.create(username='some_user', email='user@gmail.com', email_verified=False)
        self.user_not_verified.set_password('some_pswrd2')
        self.user_not_verified.save()

    def test_authenticate_user_with_not_correct_password(self):
        self.assertFalse(get_user(self.client).is_authenticated)
        self.client.login(username='some_user', password='some_pswrd1')
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_authenticate_user_with_correct_password(self):
        self.assertFalse(get_user(self.client).is_authenticated)
        self.client.login(username='some_user', password='some_pswrd2')
        self.assertTrue(get_user(self.client).is_authenticated)


class UserCreationFormTest(TestCase):

    def test_form_fields(self):
        form = UserCreationForm()
        self.assertTrue(form.fields['username'])
        self.assertTrue(form.fields['email'])
        self.assertTrue(form.fields['first_name'])
        self.assertTrue(form.fields['last_name'])
        self.assertTrue(form.fields['phone'])
        self.assertTrue(form.fields['birthday'])

    def test_email_field_label(self):
        form = UserCreationForm()
        email_label = form.fields['email'].label
        self.assertEqual(email_label, 'Адрес электронной почты')

    def test_email_field_max_length(self):
        form = UserCreationForm()
        email_max_length = form.fields['email'].max_length
        self.assertEqual(email_max_length, 254)

    def test_email_field_widget(self):
        form = UserCreationForm()
        email_autocomplete = form.fields['email'].widget.attrs['autocomplete']
        self.assertEqual(email_autocomplete, "email")

    def test_phone_field_label(self):
        form = UserCreationForm()
        phone_label = form.fields['phone'].label
        self.assertEqual(phone_label, 'Номер телефона')

    def test_phone_field_max_length(self):
        form = UserCreationForm()
        phone_max_length = form.fields['phone'].max_length
        self.assertEqual(phone_max_length, 11)

    def test_phone_field_widget(self):
        form = UserCreationForm()
        phone_required = form.fields['phone'].required
        self.assertTrue(phone_required)

    def test_first_name_field_label(self):
        form = UserCreationForm()
        first_name_label = form.fields['first_name'].label
        self.assertEqual(first_name_label, 'Имя')

    def test_first_name_field_max_length(self):
        form = UserCreationForm()
        first_name_max_length = form.fields['first_name'].max_length
        self.assertEqual(first_name_max_length, 30)

    def test_last_name_field_label(self):
        form = UserCreationForm()
        last_name_label = form.fields['last_name'].label
        self.assertEqual(last_name_label, 'Фамилия')

    def test_last_name_field_max_length(self):
        form = UserCreationForm()
        last_name_max_length = form.fields['last_name'].max_length
        self.assertEqual(last_name_max_length, 50)

    def test_birthday_field_label(self):
        form = UserCreationForm()
        birthday_label = form.fields['birthday'].label
        self.assertEqual(birthday_label, 'Дата рождения в формате "день.месяц.год"')

    def test_birthday_field_max_length(self):
        form = UserCreationForm()
        birthday_input_formats = form.fields['birthday'].input_formats
        self.assertEqual(birthday_input_formats, ['%d.%m.%Y'])


class UpdateUserFormTest(TestCase):

    def test_form_fields(self):
        form = UpdateUserForm()
        self.assertTrue(form.fields['username'])
        self.assertTrue(form.fields['email'])
        self.assertTrue(form.fields['first_name'])
        self.assertTrue(form.fields['last_name'])
        self.assertTrue(form.fields['phone'])
        self.assertTrue(form.fields['birthday'])

    def test_email_field_required(self):
        form = UpdateUserForm()
        email_required = form.fields['email'].required
        self.assertTrue(email_required)

    def test_email_field_widget(self):
        form = UpdateUserForm()
        email_widget = form.fields['email'].widget.attrs['class']
        self.assertEqual(email_widget, "form-control")

    def test_phone_field_required(self):
        form = UpdateUserForm()
        phone_required = form.fields['phone'].required
        self.assertTrue(phone_required)

    def test_phone_field_max_length(self):
        form = UpdateUserForm()
        phone_max_length = form.fields['phone'].max_length
        self.assertEqual(phone_max_length, 11)

    def test_phone_field_label(self):
        form = UpdateUserForm()
        phone_label = form.fields['phone'].label
        self.assertEqual(phone_label, 'Номер телефона')

    def test_username_field_required(self):
        form = UpdateUserForm()
        username_required = form.fields['username'].required
        self.assertTrue(username_required)

    def test_username_field_max_length(self):
        form = UpdateUserForm()
        username_max_length = form.fields['username'].max_length
        self.assertEqual(username_max_length, 50)

    def test_username_field_widget(self):
        form = UpdateUserForm()
        username_widget = form.fields['username'].widget.attrs['class']
        self.assertEqual(username_widget, "form-control")

    def test_first_name_field_label(self):
        form = UpdateUserForm()
        first_name_label = form.fields['first_name'].label
        self.assertEqual(first_name_label, 'Имя')

    def test_first_name_field_max_length(self):
        form = UpdateUserForm()
        first_name_max_length = form.fields['first_name'].max_length
        self.assertEqual(first_name_max_length, 30)

    def test_first_name_field_widget(self):
        form = UpdateUserForm()
        first_name_widget = form.fields['first_name'].widget.attrs['class']
        self.assertEqual(first_name_widget, "form-control")

    def test_last_name_field_label(self):
        form = UpdateUserForm()
        last_name_label = form.fields['last_name'].label
        self.assertEqual(last_name_label, 'Фамилия')

    def test_last_name_field_max_length(self):
        form = UpdateUserForm()
        last_name_max_length = form.fields['last_name'].max_length
        self.assertEqual(last_name_max_length, 50)

    def test_last_name_field_widget(self):
        form = UpdateUserForm()
        last_name_widget = form.fields['last_name'].widget.attrs['class']
        self.assertEqual(last_name_widget, "form-control")

    def test_birthday_field_label(self):
        form = UpdateUserForm()
        birthday_label = form.fields['birthday'].label
        self.assertEqual(birthday_label, 'Дата рождения в формате "день.месяц.год"')

    def test_birthday_field_max_length(self):
        form = UpdateUserForm()
        birthday_input_formats = form.fields['birthday'].input_formats
        self.assertEqual(birthday_input_formats, ['%d.%m.%Y'])
