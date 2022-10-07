from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    nick_name = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=256)
    is_superuser = None
    groups = None
    last_login = None
    first_name = None
    last_name = None
