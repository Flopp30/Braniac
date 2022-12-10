from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus

from authapp.models import User
from mainapp.models import News, Courses


class PagesSmokeTest(TestCase):
    '''
    Smoke тесты для mainapp
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

    def test_page_main_page_open(self):
        '''
        Доступность main page
        :return: 
        '''
        url = reverse('mainapp:main_page')
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_contacts_open(self):
        '''
        Доступность contacts
        :return: 
        '''
        url = reverse('mainapp:contacts')
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_news_open(self):
        '''
        Доступность news
        :return: 
        '''
        url = reverse('mainapp:news')
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_news_detail_open(self):
        '''
        Доступность news_detail
        :return: 
        '''
        url = reverse('mainapp:news_detail', args=['1'])
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_news_create_open(self):
        '''
        Доступность news_create superuser'om
        :return: 
        '''
        url = reverse('mainapp:news_create')
        result = self.client_auth_admin.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_news_update_open(self):
        '''
        Доступность news_update superuser'om
        :return: 
        '''
        url = reverse('mainapp:news_update', args=['1'])
        result = self.client_auth_admin.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_news_delete_open(self):
        '''
        Доступность news_delete superuser'om
        :return: 
        '''
        url = reverse('mainapp:news_delete', args=['1'])
        result = self.client_auth_admin.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_courses_open(self):
        '''
        Доступность courses
        :return: 
        '''
        url = reverse('mainapp:courses')
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_courses_detail_open(self):
        '''
        Доступность courses_detail
        :return: 
        '''
        url = reverse('mainapp:courses_detail', args=['1'])
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_doc_site_open(self):
        '''
        Доступность doc_site
        :return: 
        '''
        url = reverse('mainapp:doc_site')
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_logs_open(self):
        '''
        Доступность log_list superuser'om
        :return: 
        '''
        url = reverse('mainapp:log_list')
        result = self.client_auth_admin.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)


class NewsTestCase(TestCase):
    '''
    Тестирование функционала Новостей
    '''

    def setUp(self) -> None:
        for i in range(1, 11):
            News.objects.create(
                title=f'News{i}',
                preambule=f'Desk{i}',
                body=f'Body{i}'
            )
        User.objects.create_superuser(username='django', password='mypassword')

        self.client_auth_admin = Client()
        auth_url = reverse('authapp:login')

        self.client_auth_admin.post(
            auth_url,
            {'username': 'django', 'password': 'mypassword'},
        )

    def test_failed_create_add_by_anonym(self):
        '''
        Доступность news_create для неавторизированного пользователя
        :return:
        '''
        url = reverse('mainapp:news_create')

        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_read_add_by_anonym(self):
        '''
        Доступность news_detail для неавторизированного пользователя
        :return:
        '''
        url = reverse('mainapp:news_detail', args=['1'])

        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_failed_update_add_by_anonym(self):
        '''
        Доступность news_update для неавторизированного пользователя

        :return:
        '''
        url = reverse('mainapp:news_update', args=['1'])

        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_failed_delete_add_by_anonym(self):
        '''
        Доступность news_delete для неавторизированного пользователя

        :return:
        '''
        url = reverse('mainapp:news_delete', args=['1'])

        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_create_news_item_by_admin(self):
        '''
        Создание новости в news_create для superuser'a
        :return:
        '''
        news_count = News.objects.all().count()

        url = reverse('mainapp:news_create')

        result = self.client_auth_admin.post(
            url,
            data={
                'title': 'test news',
                'preambule': 'test desc',
                'body': 'test body'
            }
        )

        self.assertEqual(result.status_code, HTTPStatus.FOUND)
        self.assertEqual(news_count + 1, News.objects.all().count())

    def test_open_news_item_by_admin(self):
        '''
        Доступность новости в news_detail для superuser'a

        :return:
        '''
        url = reverse('mainapp:news_detail', args=['1'])

        result = self.client_auth_admin.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_update_news_item_by_admin(self):
        '''
        Обновление новости в news_update для superuser'a
        :return:
        '''
        new_body_before_upd = News.objects.get(pk=1).body

        url = reverse('mainapp:news_update', args=['1'])
        result = self.client_auth_admin.post(
            url,
            data={
                'title': 'News1',
                'preambule': 'Desc1',
                'body': 'updated body'
            }
        )
        new_body_after_upd = News.objects.get(pk=1).body

        self.assertEqual(result.status_code, HTTPStatus.FOUND)
        self.assertNotEqual(new_body_before_upd, new_body_after_upd)

    def test_delete_news_item_by_admin(self):
        '''
        Удаление новости в news_delete для superuser'a
        :return:
        '''
        news_count = News.objects.filter(deleted=True).count()

        url = reverse('mainapp:news_delete', args=['1'])

        result = self.client_auth_admin.post(url)

        self.assertEqual(result.status_code, HTTPStatus.FOUND)

        self.assertEqual(news_count + 1, News.objects.filter(deleted=True).count())
