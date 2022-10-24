"""instargram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user.views import switch_follow, kakao_social_login, kakao_social_login_callback
from django.conf import settings
from django.conf.urls.static import static
from . import views

# from django.conf import settings
# from django.conf.urls.static import static

#이메일 인증 오류방지

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('story/', include('story.urls')),

    # follow
    path('follow/<int:user_id>/', switch_follow, name="switch_follow"),

    # kakao_login
    path('account/login/kakao/', kakao_social_login, name='kakao_login'),
    path('account/login/kakao/callback/',
         kakao_social_login_callback, name='kakao_login_callback'),

    path('', include('post.urls')),

    #이메일 인증
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
