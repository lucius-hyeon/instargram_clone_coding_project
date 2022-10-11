from django.urls import path
from . import views
#이메일 인증


urlpatterns = [
    path('join/', views.join, name='join'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update, name='update'),
    path('change_password/', views.change_password, name='change_password'),
]