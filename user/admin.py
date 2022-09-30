from django.contrib import admin
from .models import UserModel, FollowModel
# Register your models here.
admin.site.register(UserModel)
admin.site.register(FollowModel)
