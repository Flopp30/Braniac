from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus

from authapp.models import User
from mainapp.models import News, Courses


class PagesSmokeTest(TestCase):
    '''
    Smoke тесты для authapp
    '''

    def setUp(self) -> None:
        for i in range(1, 11):
            News.objects.create(
                title=f'News{i}',
                preambule=f'Desk{i}',
                body=f'Body{i}'
            )
            Courses.objects.create(
                name=f'Course{i}',
                description=f'Desk{i}',
                cost=f'{i}'
            )

        # Create superuser
        User.objects.create_superuser(username='django_admin', password='mypassword')
        self.client_auth_admin = Client()
        auth_url = reverse('authapp:login')
        self.client_auth_admin.post(
            auth_url,
            {'username': 'django_admin', 'password': 'mypassword'},
        )

    def test_page_login(self):
        '''
        Доступность страницы login для неавторизированного пользователя
        :return:
        '''
        url = reverse('authapp:login')

        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_login_auth(self):
        '''
        Авторизация через страницу login
        :return:
        '''
        User.objects.create_user(username='django_user', password='mypassword')
        client_auth_user = Client()
        auth_url = reverse('authapp:login')
        result = client_auth_user.post(
            auth_url,
            {'username': 'django_user', 'password': 'mypassword'},
        )

        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_page_logout(self):
        '''
        Доступность logout
        :return:
        '''
        url = reverse('authapp:logout')
        result = self.client.get(url)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_page_edit(self):
        '''
        Доступность edit
        :return:
        '''
        url = reverse('authapp:edit', args=['1'])
        result = self.client_auth_admin.get(url)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_register(self):
        '''
        Доступность register
        :return:
        '''
        url = reverse('authapp:register')
        result = self.client.get(url)
        self.assertEqual(result.status_code, HTTPStatus.OK)
