from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/recommand/', views.recommand_user, name='recommand_user'),

]
