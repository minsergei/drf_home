import smtplib
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail
from django.core.cache import cache

from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        send_mail(
            subject="Обновление курса",
            message=f'Курс обновлен',
            from_email="mindalev1@yandex.ru",
            recipient_list=["seregaaa19@mail.ru"]
        )
