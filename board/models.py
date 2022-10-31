from django.db import models

from users.models import User


# Create your models here.
class Board(models.Model):
    title = models.TextField(blank=False)
    content = models.TextField(blank=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    username = models.TextField(blank=False)
    good = models.ManyToManyField('users.User', related_name='board_good')
    good_count = models.IntegerField(default=0)
    user = models.ForeignKey(User, models.CASCADE)
    command = models.ManyToManyField('Command', related_name='command')
    visit = models.IntegerField(default=0)


class Command(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=False)
    user = models.ForeignKey(User, models.CASCADE)
