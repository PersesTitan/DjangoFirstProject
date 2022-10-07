from django.db import models

from users.models import User


# Create your models here.
class Board(models.Model):
    title = models.TextField(blank=False)
    content = models.TextField(blank=False)
    good = models.IntegerField(default=0)   # 좋아요
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, models.CASCADE)
