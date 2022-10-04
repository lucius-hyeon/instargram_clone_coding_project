from django.contrib import admin
from .models import CommentModel, ImageModel, PostModel, LikeModel


# Register your models here.
admin.site.register(PostModel)
admin.site.register(ImageModel)
admin.site.register(LikeModel)
admin.site.register(CommentModel)

