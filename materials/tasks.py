from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from materials.models import Subscribe


@shared_task
def send_email(course_pk):
    subscribes = Subscribe.objects.filter(course_id=course_pk)
    for subscribe in subscribes:
        send_mail(
            subject="Обновление курса",
            message=f'Курс обновлен - {subscribe.course.title}',
            from_email="mindalev1@yandex.ru",
            recipient_list=["seregaaa19@mail.ru"]
        )
