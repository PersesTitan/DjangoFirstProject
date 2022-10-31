import os.path
import re

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
def get_file_path(instance, filename):
    exi = filename.split(".")
    for file_name in os.listdir("media/image/profile"):
        if re.match(f"{instance.pk}\\.*", file_name):
            os.remove("media/image/profile/" + file_name)
    return os.path.join('image/profile', str(instance.pk) + "." + exi[-1])


class User(AbstractUser):
    username = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=256)
    good = models.ManyToManyField('board.Board', related_name='user_good')
    following = models.ManyToManyField('self', related_name='following')
    followers = models.ManyToManyField('self', related_name='followers')
    profile_image = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    first_name = None
    last_name = None

    def __str__(self):
        return self.username
