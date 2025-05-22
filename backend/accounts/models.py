from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    nickname = models.CharField(max_length=50)
    total_points = models.PositiveIntegerField(default=0)
    total_pages_read = models.PositiveIntegerField(default=0)
