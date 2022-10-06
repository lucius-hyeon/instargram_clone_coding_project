from django.db import models
from user.models import UserModel
# Create your models here.


class Story(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='story')
    created_at = models.DateTimeField(auto_now_add=True)
    is_end = models.BooleanField(default=False)


class StoryViewed(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
