from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def check_user():
    users = User.objects.all()
    for user in users:
        if not user.is_superuser:
            print(user)
            if user.last_login < timezone.now() - timezone.timedelta(days=30):
                print(user)
                user.is_active = False
                user.save()
