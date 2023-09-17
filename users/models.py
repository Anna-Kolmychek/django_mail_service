from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    register_key = models.CharField(max_length=15, verbose_name='Ключ подтверждения регистрации', default='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
