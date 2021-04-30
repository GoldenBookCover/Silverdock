from celery import shared_task
from django.contrib.auth.models import User
from time import sleep


@shared_task
def count_users():
    sleep(5)
    return User.objects.count()


@shared_task
def rename_user(user_id, name):
    w = User.objects.get(id=user_id)
    w.first_name = name
    w.save()
