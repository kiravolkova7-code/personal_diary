from django.test import TestCase
from django.contrib.auth import get_user_model
import pytest
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from users.forms import RegistrationForm, LoginForm
from users.serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class UserFactory:
    @staticmethod
    def create(**kwargs):
        defaults = {
            'email': 'factory@example.com',
            'password': 'factorypass123'
        }
        # Обновляем словарь значений по умолчанию переданными аргументами
        defaults.update(kwargs)

        return User.objects.create_user(
            email=defaults['email'],
            password=defaults['password'],  # Передаем именно named argument
            first_name='Factory',
            phone=None,
            city=None,
            # Распаковываем остальные поля (например, avatar), если они пришли в kwargs
            **{k: v for k, v in defaults.items() if k not in ['email', 'password']}
        )


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email='test@example.com', password='testpass123')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(email='admin@example.com', password='adminpass')
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class RegisterSerializerTest(APITestCase):
    def test_create_valid_user(self):
        data = {"email": "newuser@example.com", "password": "strongpassword"}
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)
        user = serializer.save()
        self.assertTrue(user.check_password(data['password']))

    def test_duplicate_email_fails_validation(self):
        existing_user = UserFactory.create(email='taken@example.com')
        data = {"email": "taken@example.com", "password": "anypass"}
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        self.assertEqual(serializer.errors['email'][0].code, 'unique')


class UserSerializerTest(APITestCase):
    def test_read_only_fields(self):
        user = UserFactory.create(email='readonly@example.com')
        serializer = UserSerializer(instance=user)
        data = serializer.data
        self.assertEqual(data['email'], 'readonly@example.com')
        self.assertIsNotNone(data['id'])


class RegistrationFormTest(TestCase):
    def test_form_valid_data(self):
        form = RegistrationForm(data={
            'first_name': 'Иван',
            'email': 'ivan@test.ru',
            'phone': '+79112223344',
            'city': 'Москва',
            'password1': 'verysecret',
            'password2': 'verysecret'
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(user.check_password('verysecret'))

    def test_duplicate_email_in_form(self):
        User.objects.create_user(email='dup@test.ru', password='pass')
        form = RegistrationForm(data={
            'email': 'dup@test.ru',
            'password1': 'pass1',
            'password2': 'pass1'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class LoginFormTest(TestCase):
    def test_login_form_accepts_email(self):
        form = LoginForm(data={'username': 'login@test.ru', 'password': 'somepass'})
        self.assertIn('username', form.fields)
        self.assertEqual(form.fields['username'].label, '')


class AuthViewsTest(TestCase):
    def setUp(self):
        # Создаем базового пользователя для всех тестов этого класса
        self.user = User.objects.create_user(
            email='loggedin@example.com',
            password='logpass'
        )

    def test_register_view_get(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_success(self):
        data = {
            'first_name': 'Петр',
            'email': 'newreg_unique@example.com',  # Уникальная почта
            'password1': 'newpass123',
            'password2': 'newpass123',
            'phone': '',
            'city': ''
        }
        response = self.client.post(reverse('users:register'), data, follow=False)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:login'))

        # Проверяем факт создания записи напрямую в БД
        self.assertTrue(User.objects.filter(email='newreg_unique@example.com').exists())

    def test_register_view_existing_email(self):
        # Используем фабрику, она создаст другого пользователя, не трогая self.user
        UserFactory.create(email='busy@example.com')
        data = {'email': 'busy@example.com', 'password1': '123', 'password2': '123'}
        response = self.client.post(reverse('users:register'), data)

        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)




