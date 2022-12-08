from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from mainapp.models import NULLABLE


class User(AbstractUser):
    # Остальное наследуется от AbstractUser

    email = models.EmailField(blank=True, verbose_name=_('Email'))
    age = models.PositiveSmallIntegerField(**NULLABLE, verbose_name=_('age'))
    avatar = models.ImageField(**NULLABLE, upload_to='users', verbose_name=_('avatar'))

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
