from django.contrib import admin
from .models import ImageModel, PostModel

# Register your models here.
admin.site.register(PostModel)
admin.site.register(ImageModel)
