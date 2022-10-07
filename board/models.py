from django.db import models


# Create your models here.
class Board(models.Model):
    title = models.TextField(blank=False)
    content = models.TextField(blank=False)
    
