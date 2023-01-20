# BraniacLMS
Современная платформа для обучения. Прогрессивный взгляд на простые вещи.
Развернутый на сервере проект можно посмотреть *[тут](http://95.163.242.42/)*
### Цель проекта
Разработать SSR MPA на Django с использованием инструмента очередей Celery 

### Стек
- Python > 3.10  
  - isort, black, autoflake
  - Django 4.1  
  - Celery [Redis]
- Ubuntu 20.04
  - Nginx  
  - Gunicorn
- PostgreSQL

### Общая схема компонентов сервера
![server components](for_github/server_components.png)

### Запуск проекта
1) Сделать fork репозитория и склонировать его на локальную машину
```git clone *ssh from your repo*```
2) Создать виртуальное окружение и запустить его

```python3 -m venv env```
```source env/bin/activate```
3) Установить зависимости ```pip install -r requirements.txt```
4) Создать файл ```.env``` в корне проекта и заполнить его по примеру ```.env.sample```. 
Поля электронной почты - опциональны. 
   - ```ENV_TYPE``` -- тип окружения. ```local``` - если локально
   - ```DEBUG``` -- режим отладки Django framework. ```True```/```False```
   - ```DEBUG``` -- режим отладки Django framework. ```True```/```False```
   - api_keys -- переменные для ключей api. Опционально, без них не будет работать авторизация через соц. сети.
   - Данные почты -- опционально. Без них не будет работать отправка форм обратной связи

```python
ENV_TYPE=
DEBUG=
DEBUG_TOOLBAR=

# vk_api_keys
SOCIAL_AUTH_VK_OAUTH2_KEY=
SOCIAL_AUTH_VK_OAUTH2_SECRET=

# github_api_keys
SOCIAL_AUTH_GITHUB_KEY=
SOCIAL_AUTH_GITHUB_SECRET=

# Yandex mail
EMAIL_HOST_USER_YANDEX=
EMAIL_HOST_PASSWORD_YANDEX=
```
5) Выполнить миграции ```python3 manage.py migrate```
6) Заполнить базу тестовыми данными ```python3 manage.py loaddata mainapp/fixtures/*json```
7) Установить gettext ```sudo apt install gettext ```
8) Скомпилировать locale (файл интернационализации) ```python3 manage.py compilemessages -i env ```
9) Запустить ```python3 manage.py runserver```

### Реализованный функционал
- Интернационализация (через locale)
- Описание ORM для сущностей базы
- Наследование шаблонов, страницы с динамикой
- Авторизация пользователей через сторонние ресурсы (vk, github)
- Отправка форм обратной связи на почту с помощью Celery
- Разделенная система прав для пользователей.  
- Возможность радектирования/ удаление объектов новостей со страницы сайта в зависимости от группы пользователя
  - Возможность оставлять отзывы о курсе. 
  - Доступ к разделу модерирования / администрирования сайта
- Кастомная настройка админки
- Логгирование
- Деплой проекта на сервер
## Лицензия
MIT