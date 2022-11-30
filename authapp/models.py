from django.contrib.auth.models import AbstractUser
from django.db import models

from mainapp.models import NULLABLE


class User(AbstractUser):
    ''' Остальное наследуется от AbstractUser '''

    email = models.EmailField(blank=True, verbose_name='Email')
    age = models.PositiveSmallIntegerField(**NULLABLE, verbose_name='Age')
    avatar = models.ImageField(**NULLABLE, upload_to='users', verbose_name='Avatar path')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'