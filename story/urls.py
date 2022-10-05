from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_story, name='create_story'),
    #클릭 한 번으로 해당 유저의 스토리는 다 보는 것으로 구현예정
    path('<str:nickname>/', views.view_story, name='view_story'),
]
