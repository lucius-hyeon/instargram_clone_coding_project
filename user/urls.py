from django.urls import path
from . import views
# 이메일 인증
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('join/', views.join, name='join'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    ###update###
    path('update/', views.update, name='update'),
    path('change_password/', views.change_password, name='change_password'),
    # 이메일 인증### 공사중
]
