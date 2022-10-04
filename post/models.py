from email.policy import default
from django.db import models
from user.models import UserModel
from django.conf import settings

# Create your models here.


class PostModel(models.Model):
    class Meta:
        db_table = 'post'

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.TextField()
    liker = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='post_liker')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ImageModel(models.Model):
    class Meta:
        db_table = 'image'
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media')
    image_name = models.CharField(max_length=256, null=True)


class CommentModel(models.Model):
    class Meta:
        db_table = 'comment'

    content = models.CharField(max_length=256, null=False)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    liker = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='comment_liker')
    created_at = models.DateTimeField(auto_now_add=True)


class BookMarkModel(models.Model):
    class Meta:
        db_table = 'bookmark'
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
