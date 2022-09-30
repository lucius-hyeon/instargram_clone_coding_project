from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserModel(AbstractUser):
    class Meta:
        db_table = 'user'

    bio = models.CharField(max_length=50, null=True)
    profile_image = models.ImageField(
        upload_to='media', height_field=None, width_field=None, default='default.jpeg')


class FollowModel(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='user')
    follow = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='follow')
