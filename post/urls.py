from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('post/', views.post_add, name='post'),
    path('post/update/<int:post_id>/', views.post_update, name='post_update'),
    path('detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('delete/<int:post_id>/', views.post_delete, name='post_delete'),
    path('<str:nickname>/', views.profile, name='profile'),
    path('<str:nickname>/recommand/', views.recommand_user, name='recommand_user'),
    path('comment/<int:post_id>/', views.comment, name='comment'),
    path('comment/delete/<int:comment_id>/',
         views.comment_delete, name='comment_delete'),

    path('like/<int:post_id>/', views.is_like, name='like'),
    path('bookmark/<int:post_id>/', views.switch_bookmark, name='bookmark'),

    path('replycomment/<int:post_id>/<int:comment_id>/',
         views.replycomment, name="replycomment"),
    path('replycomment/delete/<int:post_id>/<int:comment_id>/',
         views.replycomment_delete, name="replycomment_delete"),

]
