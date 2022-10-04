from django.shortcuts import render, redirect
# from django.contrib import messages

from .models import UserModel, FollowModel
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import re


# def join(request):
#     return render(request, 'user/join.html')


# @login_required(login_url='user:signin')
# def switch_follow(request):
#     follow_id = request.GET.get('followId', '')
#     user = UserModel.objects.get(pk=request.user.id)
#     follow = UserModel.objects.get(pk=follow_id)


#     try:
#         follower = FollowModel.objects.get(user=user, follow=follow)
#         follower.delete()
#     except FollowModel.DoesNotExist:
#         FollowModel.objects.create(user=user, follow=follow)

@login_required(login_url='login')
def switch_follow(request, user_id):
    user = UserModel.objects.get(pk=request.user.id)
    follow = UserModel.objects.get(pk=user_id)

    try:
        follower = FollowModel.objects.get(user=user, follow=follow)
        follower.delete()
    except FollowModel.DoesNotExist:
        FollowModel.objects.create(user=user, follow=follow)
    return JsonResponse({'msg': 'success'})


def join(request):
    if request.method == 'GET':
        return render(request, 'user/join.html')

    elif request.method == 'POST':

        check_email = re.compile(
            '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

        username = request.POST.get('username', None)
        nickname = request.POST.get('nickname', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        email = request.POST.get('email', None)

        # 정규표현식으로 email check
        check_email = check_email.match(email)

        if check_email is None:
            return render(request, 'user/join.html', {'error': '이메일 양식이 올바르지 않습니다.'})

        if username == '' or nickname == '' or password == '' or email == '':
            return render(request, 'user/join.html', {'error': '입력란을 모두 채워주세요'})

        if password != password2:
            return render(request, 'user/join.html', {'error': '비밀번호가 일치하지 않습니다.'})

        exist_user = get_user_model().objects.filter(email=email)
        if exist_user:
            return render(request, 'user/join.html', {'error': '이미 가입된 이메일 계정입니다.'})

        else:

            UserModel.objects.create_user(
                username=username,
                nickname=nickname,
                password=password,
                email=email,
            )
            return render(request, 'user/login.html')

### 로그인 ###

def login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')

    elif request.method == 'POST':
        check_email = re.compile(
            '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        check_email = check_email.match(email)

        if check_email is None:
            return render(request, 'user/login.html', {'error': '이메일 양식이 올바르지 않습니다.'})

        # 입력란 빈칸일때
        if email == '':
            return render(request, 'user/login.html', {'error': '메일을 입력해주세요.'})
        elif password == '':
            return render(request, 'user/login.html', {'error': '패스워드를 입력해주세요.'})

        # authenticate is only allowed username.
        # find username
        username = UserModel.objects.get(email = email).username

        print(username)
        #User 인증 함수. 자격 증명이 유효한 경우 User 객체를, 그렇지 않은 경우 None을 반환
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)  # 로그인 처리


            user = request.user
            print(user.nickname, user, user.username)

            userinfo ={
                # 'followers': followers,

            }
            return render(request, 'index.html' )
        else:
            print('로그인 실패')
            return render(request, 'user/login.html', {'error': '유저 정보를 찾을 수 없습니다.'})


### 로그아웃 ###
@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

