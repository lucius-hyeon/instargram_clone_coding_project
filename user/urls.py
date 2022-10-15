from django.urls import path, include
from . import views

#로그아웃
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('join/', views.join, name='join'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('update/', views.update, name='update'),
    path('change_password/', views.change_password, name='change_password'),
    path('delete/', views.delete, name='delete'),

    # path('password_reset/', auth_views.PasswordChangeView.as_view(),name='reset'),
    # path('accounts/', include('django.contrib.auth.urls')),

    #이메일 인증
    # path('password_reset/',auth_views.PasswordChangeView.as_view(template_name='password_reset.html'), name='password_reset'),
    # path('password_reset/done/',auth_views.PasswordChangeView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/',auth_views.PasswordChangeView.as_view(template_name='reset_token.html'), name='reset_token'),
    # path('reset/done/',auth_views.PasswordChangeView.as_view(template_name='reset_done.html'), name='reset_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]