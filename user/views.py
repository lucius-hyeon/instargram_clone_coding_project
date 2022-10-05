from msilib.schema import ListView
from tkinter import PhotoImage
from django.shortcuts import render, redirect
# from django.contrib import messages
from .models import UserModel, FollowModel
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model

import re
import requests
import random
import string

# 비밀번호 변경
from django.contrib.auth.hashers import check_password
from django.contrib import messages, auth


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

        # nickname 중복체크 추가
        exist_user = get_user_model().objects.filter(nickname=nickname)
        if exist_user:
            return render(request, 'user/join.html', {'error': '이미 가입된 사용자 이름 입니다.'})

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
        username = UserModel.objects.get(email=email).username
        # User 인증 함수. 자격 증명이 유효한 경우 User 객체를, 그렇지 않은 경우 None을 반환
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:

            auth.login(request, user)  # 로그인 처리
            return redirect('/')

            user = request.user
            print(user.nickname, user, user.username)

            userinfo = {
                # 'followers': followers,

            }
            return redirect("/")
        else:
            return render(request, 'user/login.html', {'error': '유저 정보를 찾을 수 없습니다.'})


### 로그아웃 ###
@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')


def get_random_nickname():
    rand_str = ''
    while True:
        for _ in range(10):
            rand_str += str(random.choice(string.ascii_letters + string.digits))
        if UserModel.objects.filter(nickname=rand_str).exists():
            pass
        else:
            return rand_str


def get_random_password():
    rand_str = ''
    while True:
        for _ in range(30):
            rand_str += str(random.choice(string.ascii_letters + string.digits))
            return rand_str


def kakao_social_login(request):
    if request.method == 'GET':
        client_id = 'b69e5d10ed989fce828f23f98a5265d9'
        redirect_uri = 'http://127.0.0.1:8000/account/login/kakao/callback'
        return redirect(
            f'https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code'
        )


def kakao_social_login_callback(request):
    try:
        code = request.GET.get('code')
        client_id = 'b69e5d10ed989fce828f23f98a5265d9'
        redirect_uri = 'http://127.0.0.1:8000/account/login/kakao/callback'
        token_request = requests.post(
            'https://kauth.kakao.com/oauth/token', {'grant_type': 'authorization_code',
                                                    'client_id': client_id, 'redierect_uri': redirect_uri, 'code': code}
        )
        # token_request = requests.get(
        # f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}'
        # )
        token_json = token_request.json()

        error = token_json.get('error', None)

        if error is not None:
            print(error)
            return JsonResponse({"message": "INVALID_CODE"}, status=400)

        access_token = token_json.get("access_token")

    except KeyError:
        return JsonResponse({"message": "INVALID_TOKEN"}, status=400)

    except access_token.DoesNotExist:
        return JsonResponse({"message": "INVALID_TOKEN"}, status=400)

        #------get kakaotalk profile info------#

    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    kakao_id = profile_json.get('id')
    username = profile_json['properties']['nickname']

    if UserModel.objects.filter(kakao_id=kakao_id).exists():
        user = UserModel.objects.get(kakao_id=kakao_id)
        auth.login(request, user)  # 로그인 처리
    else:
        UserModel.objects.create(
            username=username,
            nickname=get_random_nickname(),  # usermodel에 없을 때 까지 생성 후 리턴
            password=get_random_password(),
            kakao_id=kakao_id,
        )
        user = UserModel.objects.get(kakao_id=kakao_id)
        auth.login(request, user)
    return redirect('/')


def get_profile(request, nickname):
    print(request)
    print(dir(request.user))
    context = {}
    return render(request, 'user/profile.html', context)


###user_update##

@login_required
def update(request):
    if request.method == 'GET':
        return render(request, 'user/update.html')
    elif request.method == 'POST':
        user = request.user
        bio = request.POST.get('bio')
        email = request.POST.get('email')
        username = request.POST.get('username')
        nickname = request.POST.get('nickname')
        exist_nickname = get_user_model().objects.filter(nickname=nickname)
        if exist_nickname and user.nickname == nickname:
            user.nickname = nickname
            user.bio = bio
            user.email = email
            user.username = username
            user.save()
            return redirect('/', user.username)
        elif exist_nickname and user.nickname != nickname:
            return render(request, 'user/update.html', {'error': '이미 사용중인 nickname 입니다.'})
        else:
            user.nickname = nickname
            user.bio = bio
            user.email = email
            user.username = username
            user.save()
            return redirect('/', user.username)

###비밀번호 변경###


@login_required
def change_password(request):
    if request.method == "POST":
        user = request.user
        origin_password = request.POST["origin_password"]
        if check_password(origin_password, user.password):
            new_password = request.POST["new_password"]
            confirm_password = request.POST["confirm_password"]
            if origin_password == confirm_password or new_password == origin_password:
                return render(request, 'user/change_password.html', {'error': '사용하고 있는 비밀번호를 입력하셨습니다.'})
            elif new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                auth.login(request, user,
                           backend='django.contrib.auth.backends.ModelBackend')
                return redirect('/')
            else:
                return render(request, 'user/change_password.html', {'error': '신규 비밀번호와 신규 비밀번호 확인을 똑같이 입력해주세요.'})
        else:
            return render(request, 'user/change_password.html', {'error': '현재 비밀번호가 틀렸습니다.'})
    else:
        return render(request, 'user/change_password.html')
