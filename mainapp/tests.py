import django.core.mail
from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus

from selenium.webdriver.chrome.options import Options

from authapp.models import User
from mainapp import tasks
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


import pickle
from unittest import mock


class TestCoursesWithMock(TestCase):
    fixtures = (
        "mainapp/fixtures/002_courses.json",
        "mainapp/fixtures/003_lessons.json",
        "mainapp/fixtures/004_teachers.json",
    )

    def test_page_open_detail(self):
        course_obj = Courses.objects.get(pk=2)
        url = reverse("mainapp:courses_detail", args=[course_obj.pk])
        with open(f"mainapp/fixtures/005_feedback_list_{course_obj.pk}.bin", "rb") as f, mock.patch(
                "django.core.cache.cache.get"
        ) as mocked_cache:
            mocked_cache.return_value = str(pickle.load(f))
            result = self.client.get(url)
            self.assertTrue(mocked_cache.called)
            self.assertEqual(result.status_code, HTTPStatus.OK)


class TestTaskMailSend(TestCase):

    def setUp(self) -> None:
        User.objects.create_user(username='django_user', password='mypassword')

        self.client_auth = Client()
        auth_url = reverse('authapp:login')

        self.client_auth.post(
            auth_url,
            {'username': 'django_user', 'password': 'mypassword'},
        )

    def test_mail_send(self):
        message_text = 'text'
        user = User.objects.first()
        tasks.send_feedback_to_email(message_from=user.email, message_body=message_text)
        self.assertEqual(django.core.mail.outbox[0].body, message_text)


from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from Braniac.settings import SELENIUM_DRIVER_PATH_CHROME


class TestNewsSelenium(StaticLiveServerTestCase):
    fixtures = (
        'mainapp/fixtures/001_news.json',
    )

    def setUp(self) -> None:
        User.objects.create_superuser(username='django', password='password')
        super().setUp()

        # headless mode for browser
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        self.selenium = WebDriver(
            executable_path=SELENIUM_DRIVER_PATH_CHROME,
            options=chrome_options,
        )
        self.selenium.implicitly_wait(10)
        # login
        self.selenium.get(f"{self.live_server_url}{reverse('authapp:login')}")
        button_enter = WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[type="submit"]')
            )
        )
        self.selenium.find_element(by='id', value="id_username").send_keys("django")
        self.selenium.find_element(by='id', value="id_password").send_keys("password")
        button_enter.click()

        # Wait for footer
        WebDriverWait(self.selenium, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "mt-auto")))

    def test_create_button_clickable(self):
        path_list = f'{self.live_server_url}{reverse("mainapp:news")}'
        path_add = reverse('mainapp:news_create')
        self.selenium.get(path_list)
        button_create = WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, f'[href="{path_add}"]')
            )
        )
        button_create.click()  # Test that button clickable
        WebDriverWait(self.selenium, 1).until(
            EC.visibility_of_element_located((By.ID, "id_title"))
        )
        # With no element - test will be failed
        # WebDriverWait(self.selenium, 1).until(
        #     EC.visibility_of_element_located((By.ID, "id_title111"))
        # )

    def test_pick_color(self):
        path = f"{self.live_server_url}{reverse('mainapp:main_page')}"

        self.selenium.get(path)
        navbar_el = WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "navbar"))
        )
        try:
            self.assertEqual(
                navbar_el.value_of_css_property("background-color"),
                "rgba(255, 255, 255, 1)",
            )
        except AssertionError:
            with open(
                    "img_for_github/screenshots/001_navbar_el_scrnsht.png", "wb"
            ) as outf:
                outf.write(navbar_el.screenshot_as_png)
            raise

    def tearDown(self):
        # Close browser
        self.selenium.quit()
        super().tearDown()
