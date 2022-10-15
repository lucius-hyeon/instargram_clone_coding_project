from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserModel(AbstractUser):
    class Meta:
        db_table = 'user'  # 유저 테이블
    bio = models.CharField(max_length=50, blank=True)
    # 문자열에 null 을 사용하면 null이라는 빈 문자열이 들어간다. 프로필에 Null이 떠서 수정
    nickname = models.CharField(max_length=10, blank=True)
    profile_image = models.ImageField(
        upload_to='media', height_field=None, width_field=None, default='default.jpeg'
    )
    kakao_id = models.CharField(max_length=256, null=True, blank=True)



class FollowModel(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='user')
    follow = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='follow')
