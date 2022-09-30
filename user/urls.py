from django.urls import path
from . import views

urlpatterns = [
    path('join/', views.join, name='join'),
    path('login/', views.login, name='login'),

    #     path('login/kakao', views.kakao_login, name='kakao-login'),
    #     path(
    #         "login/kakao/callback/",
    #         views.kakao_login_callback,
    #         name="kakao-callback",
    #     ),
    path('logout/', views.logout, name='logout'),

]
