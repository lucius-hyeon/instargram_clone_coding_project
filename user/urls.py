from django.urls import path
from . import views
#로그아웃
from django.contrib.auth import views as auth_views

app_name='user'

urlpatterns = [
    path('join/', views.join, name='join'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('update/', views.update, name='update'),
    path('change_password/', views.change_password, name='change_password'),
    path('delete/', views.delete, name='delete'),
]