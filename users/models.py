from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=256)
    good = models.ManyToManyField('board.Board', related_name='user_good')
    first_name = None
    last_name = None

    def __str__(self):
        return self.username
