from django.contrib.auth.models import AbstractUser
from django.db import models
import os
def user_profile_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'user_{instance.id}.{ext}'
    return os.path.join('profile_images', filename)

class User(AbstractUser):
    # 유저 닉네임
    nickname = models.CharField(max_length=50)
    # 포인트, 페이지
    total_points = models.PositiveIntegerField(default=0)
    total_pages_read = models.PositiveIntegerField(default=0)
    # 음식 창고
    basic_food = models.IntegerField(default=0)
    premium_food = models.IntegerField(default=0)
    # 팔로우
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )
    # 프로필이미지
    profile_image = models.ImageField(upload_to=user_profile_image_path, blank=True, null=True)

    