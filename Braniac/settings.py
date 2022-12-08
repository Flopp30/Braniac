import os
from pathlib import Path

from dotenv import load_dotenv
import django

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-2n76^#%paai=k^n@h*y02-zigv0oj8@#+ut7v*c-avh6z@&9d0"

# Load dot_env
dot_env = BASE_DIR / '.env'
load_dotenv(dotenv_path=dot_env)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "markdownify.apps.MarkdownifyConfig",

    'crispy_forms',
    'debug_toolbar',
    'social_django',

    "mainapp",
    'authapp',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = "Braniac.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ['templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = "Braniac.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Параметры развертывания на сервере / локальные параметры для БД и пути до статики

if os.getenv('ENV_TYPE') != 'local':
    STATIC_ROOT = BASE_DIR / 'static'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'geekshop',
            'USER': 'postgres',
        }
    }
else:
    STATICFILES_DIRS = (
        BASE_DIR / 'static/',
    )

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    INTERNAL_IPS = [
        '127.0.0.1'
    ]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Путь до медиа файлов

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Модель пользователей при сохранении (переопределение стандартной модели из django)

AUTH_USER_MODEL = 'authapp.User'

# Редиректы после входа/выхода с аккаунта

LOGIN_REDIRECT_URL = 'mainapp:main_page'
LOGOUT_REDIRECT_URL = 'mainapp:main_page'

# Хранение сообщений уведомлений

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Подключение стороннего модуля аутентификации

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.vk.VKOAuth2',
)

# Ключи авторизации ВК

SOCIAL_AUTH_VK_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_VK_OAUTH2_KEY')
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_VK_OAUTH2_SECRET')

# Ключи авторизации GitHub

SOCIAL_AUTH_GITHUB_KEY = os.getenv('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = os.getenv('SOCIAL_AUTH_GITHUB_SECRET')

# Пак шаблонов для crispy
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Определение
CASHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        }
    }
}

# Celery config (url ссылка на редиce и место, куда складывать результат выполнения задач)
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
# Конфиги для рассылки

if os.getenv('ENV_TYPE') != 'local':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = False
    EMAIL_USE_SSL = True
    EMAIL_HOST = 'smtp.yandex.ru'
    EMAIL_PORT = 465
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER_YANDEX')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD_YANDEX')
    SERVER_EMAIL = EMAIL_HOST_USER
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
else:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = 'emails_tmp'
    EMAIL_HOST_USER = 'support@branac.local'

# Путь до лог файла
LOG_FILE = BASE_DIR / 'log' / 'main_log.log'

# Настройка логгирования

# TODO: Почитать про sentry
LOGGING = {
    'version': 1,
    'disable_exciting_loggers': False,  # Отключить сторонние логгеры
    'formatters': {  # Формат логов. Название + формат
        'console': {
            'format': '[%(asctime)s] %(levelname)s %(name)s (%(lineno)d) %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',  # Максимальный уровень логов. Все, что отсюда и ниже до error
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
            'formatter': 'console'
        },
        'console': {'class': 'logging.StreamHandler', 'formatter': 'console'},
    },
    'loggers': {
        'django': {'level': 'INFO', 'handlers': ['file', 'console']}
    }
}

# Путь до файла интернационализации
LOCALE_PATHS = (BASE_DIR / 'locale',)
