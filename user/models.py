from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.


class UserModel(AbstractUser):
    class Meta:
        db_table = 'user'  # 유저 테이블
    bio = models.CharField(max_length=50, null=True)
    nickname = models.CharField(max_length=10, null=False)
    profile_image = models.ImageField(
        upload_to='media', height_field=None, width_field=None, default='default.jpeg'
    )
    kakao_id = models.CharField(max_length=256, null=True, blank=True)


class FollowModel(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='user')
    follow = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='follow')
