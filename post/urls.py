from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test_html, name='test'),
    path('post/', views.post_add, name='post'),
    path('<str:nickname>/', views.profile, name='profile'),
    path('<str:username>/recommand/', views.recommand_user, name='recommand_user'),
    path('comment/<int:post_id>/', views.comment, name='comment'),
    path('<int:post_id>/', views.comments_list, name='comment_list'),
    path('like/<int:post_id>/', views.is_like, name='like')

]
