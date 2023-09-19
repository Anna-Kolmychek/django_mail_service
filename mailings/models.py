import datetime

from django.db import models

from main.models import NULLABLE
from users.models import User


class Mailing(models.Model):
    PERIOD_ONCE = 'once'
    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'

    PERIODS = (
        (PERIOD_ONCE, 'Один раз'),
        (PERIOD_DAILY, 'Раз в день'),
        (PERIOD_WEEKLY, 'Раз в неделю'),
        (PERIOD_MONTHLY, 'Раз в месяц'),
    )

    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_DONE = 'done'
    STATUSES = (
        (STATUS_CREATED, 'Создана'),
        (STATUS_STARTED, 'Запущена'),
        (STATUS_DONE, 'Завершена'),
    )

    title = models.CharField(max_length=150, verbose_name='Название')
    desription = models.TextField(verbose_name='Описание', **NULLABLE)

    sending_time_start = models.TimeField(verbose_name='Время отправки (с)', default=datetime.time(10, 0))
    sending_time_end = models.TimeField(verbose_name='Время отправки (до)', default=datetime.time(11, 0))
    periodicity = models.CharField(max_length=20, choices=PERIODS, verbose_name='Периодичность',
                                   default=PERIOD_ONCE)
    status = models.CharField(max_length=20, choices=STATUSES, verbose_name='Статус',
                              default=STATUS_CREATED)

    mail_title = models.CharField(max_length=300, verbose_name='Тема письма')
    mail_content = models.TextField(verbose_name='Содержание письма')

    user_admin = User.objects.get(email='admin@mail.com').pk
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.CASCADE, default=user_admin)
    # связь с клиентами



    def __str__(self):
        return f'{self.title} ({self.desription[:20]}…)'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
