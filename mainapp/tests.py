from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus

from authapp.models import User
from mainapp.models import News


class StaticPagesSmokeTest(TestCase):

    def test_page_main_page_open(self):
        url = reverse('mainapp:main_page')
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_contacts_open(self):
        url = reverse('mainapp:contacts')
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)


class NewsTestCase(TestCase):

    def setUp(self) -> None:
        for i in range(1, 11):
            News.objects.create(
                title=f'News{i}',
                preambule=f'Desk{i}',
                body=f'Body{i}'
            )
        User.objects.create_superuser(username='django', password='mypassword')
        self.client_with_auth = Client()
        auth_url = reverse('authapp:login')
        self.client_with_auth.post(
            auth_url,
            {'username': 'django', 'password': 'mypassword'},
        )

    def test_open_page(self):
        url = reverse('mainapp:news')
        result = self.client.get(url)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_failed_open_add_by_anonym(self):
        url = reverse('mainapp:news_create')

        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_create_news_item_by_admin(self):
        news_count = News.objects.all().count()

        url = reverse('mainapp:news_create')

        result = self.client_with_auth.post(
            url,
            data={
                'title': 'test news',
                'preambule': 'test desc',
                'body': 'test body'
            }
        )

        self.assertEqual(result.status_code, HTTPStatus.FOUND)
        self.assertEqual(news_count + 1, News.objects.all().count())
