import random
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

# Create your models here.
NULLABLE = {'blank': 'True', 'null': 'True'}

code = ''.join([str(random.randint(0, 9)) for _ in range(12)])


class UserRoles(models.TextChoices):
    """ Создание ролей пользователя """
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Почта')
    avatar = models.ImageField(upload_to='user/', verbose_name='Аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', **NULLABLE)
    country = models.CharField(max_length=35, verbose_name='Страна', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='Активность')
    ver_code = models.CharField(max_length=15, default=code, verbose_name='Проверочный код')
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f' {self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
