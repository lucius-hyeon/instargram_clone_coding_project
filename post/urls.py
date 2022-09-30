from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test_html, name='test'),
    path('post/', views.post_add, name='post'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/recommand/', views.recommand_user, name='recommand_user'),
]
