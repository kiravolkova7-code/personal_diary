from django.contrib.auth import get_user_model
from .models import Entry
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

User = get_user_model()


class UserFactory:
    @staticmethod
    def create(**kwargs):
        # Используем email как основной идентификатор
        defaults = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        defaults.update(kwargs)

        # ВАЖНО: Убедитесь, что ваш метод create_user принимает email первым позиционным аргументом,
        # либо передавайте его явно через defaults.
        return User.objects.create_user(email=defaults['email'], password=defaults['password'],
                                        **{k: v for k, v in defaults.items() if k not in ['email', 'password']})


class EntryFactory:
    @staticmethod
    def create(**kwargs):
        user = kwargs.pop('user', None) or UserFactory.create()
        defaults = {
            'title': 'Тестовая запись',
            'content': 'Содержимое записи.',
            'subject': 'personal',
            'user': user
        }
        defaults.update(kwargs)
        return Entry.objects.create(**defaults)


class EntryWebViewsTest(TestCase):

    def setUp(self):
        self.user = UserFactory.create(email='webuser@example.com', password='secret')
        self.other_user = UserFactory.create(email='other@example.com', password='secret')

        # Создаем записи без ручной даты, берем те, что создала фабрика
        self.my_entry = EntryFactory.create(user=self.user, title='Моя веб-запись')
        self.other_entry = EntryFactory.create(user=self.other_user, title='Чужая веб-запись')

    def test_list_view_requires_login(self):
        url = reverse('entries:entry-list')
        response = self.client.get(url)
        # Redirect to login page
        self.assertEqual(response.status_code, 302)

    def test_list_view_shows_only_users_entries(self):
        self.client.login(email='webuser@example.com', password='secret')
        url = reverse('entries:entry-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # В контексте ListView объекты лежат в 'object_list' или просто в цикле шаблона
        entry_titles = list(response.context['object_list'].values_list('title', flat=True))

        self.assertIn('Моя веб-запись', entry_titles)
        self.assertNotIn('Чужая веб-запись', entry_titles)

    def test_detail_view_permissions(self):
        detail_url = reverse('entries:entry-detail', args=[self.my_entry.pk])
        other_detail_url = reverse('entries:entry-detail', args=[self.other_entry.pk])

        self.client.force_login(self.user)

        resp_mine = self.client.get(detail_url)
        self.assertEqual(resp_mine.status_code, 200)

        resp_other = self.client.get(other_detail_url)
        self.assertEqual(resp_other.status_code, 404)

    def test_create_entry_via_web_form(self):
        self.client.login(email='webuser@example.com', password='secret')
        create_url = reverse('entries:entry-create')

        # Сначала GET-запрос, чтобы получить форму и CSRF-токен
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200)

        # Теперь POST
        post_data = {
            'title': 'Запись через сайт',
            'subject': 'work',
            'content': 'Текст из браузера'
        }
        response = self.client.post(create_url, data=post_data)

        # После успешного создания generic CreateView делает redirect (302)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Entry.objects.filter(title='Запись через сайт').exists())

