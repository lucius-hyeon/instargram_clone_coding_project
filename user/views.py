from django.shortcuts import render, redirect
from .models import UserModel, FollowModel
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import re
import requests
import random
import string

# 회원탈퇴

# 비밀번호 변경
from django.contrib.auth.hashers import check_password
from django.contrib import auth


@login_required(login_url='login')
def switch_follow(request, user_id):
    """
    Switching follow & unfollow
        Parameters:
            user_id (int) : A specipical user's PK
    """
    # pk https://stackoverflow.com/questions/2165865/django-queries-id-vs-pk
    user = UserModel.objects.get(pk=request.user.id)
    follow = UserModel.objects.get(pk=user_id)

    try:
        follower = FollowModel.objects.get(user=user, follow=follow)
        follower.delete()
    except FollowModel.DoesNotExist:
        FollowModel.objects.create(user=user, follow=follow)
    return JsonResponse({'msg': 'success'})

# 회원가입


def join(request):
    if request.method == 'GET':
        return render(request, 'user/join.html')

    elif request.method == 'POST':

        check_email = re.compile(
            '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        # TODO
        username = request.POST.get('username', None)
        nickname = request.POST.get('nickname', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        email = request.POST.get('email', None)

        # 정규표현식으로 email check
        check_email = check_email.match(email)
        if check_email is None:
            return render(request, 'user/join.html', {'error': '이메일 양식이 올바르지 않습니다.'})

        # 입력칸이 빈칸일 때
        if username == '' or nickname == '' or password == '' or email == '':
            return render(request, 'user/join.html', {'error': '입력란을 모두 채워주세요'})

        # 입력한 패스워드 값이 맞지 않을때
        if password != password2:
            return render(request, 'user/join.html', {'error': '비밀번호가 일치하지 않습니다.'})

        # 이미 가입한 유저가 있을 때
        exist_user = get_user_model().objects.filter(email=email)
        if exist_user:
            return render(request, 'user/join.html', {'error': '이미 가입된 이메일 계정입니다.'})

        # nickname 중복체크 추가
        exist_user = get_user_model().objects.filter(nickname=nickname)
        if exist_user:
            return render(request, 'user/join.html', {'error': '이미 가입된 사용자 이름 입니다.'})

        # username 중복체크 추가
        exist_user = get_user_model().objects.filter(username=username)
        if exist_user:
            return render(request, 'user/join.html', {'error': '이미 가입된 성명 입니다.'})

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
        # 이메일 양식 체크
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

        # 존재하지 않는 이메일로 로그인 할 경우 에러가 발생하는걸 막기위한 코드
        exist_email = get_user_model().objects.filter(email=email)
        if exist_email:
            pass
        else:
            return render(request, 'user/login.html', {'error': '유저 정보를 찾을 수 없습니다.'})
        username = UserModel.objects.get(email=email.lower()).username

        # User 인증 함수. 자격 증명이 유효한 경우 User 객체를, 그렇지 않은 경우 None을 반환
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 로그인 처리
            user = request.user
            return redirect("/")
        else:
            return render(request, 'user/login.html', {'error': '유저 정보를 찾을 수 없습니다.'})



def get_random_nickname():
    """
    처음 소셜 로그인을 시도한 사용자의 임시 닉네임
    Return random nickname
    """
    rand_str = ''
    while True:
        for _ in range(10):
            # 모든 문자열 혹은 숫자를 랜덤으로 조합
            rand_str += str(random.choice(string.ascii_letters + string.digits))
        if UserModel.objects.filter(nickname=rand_str).exists():
            pass
        else:
            return rand_str


def get_random_password():
    """
    처음 소셜 로그인을 시도한 사용자의 임시 패스워드
    Return random password
    """
    rand_str = ''
    while True:
        for _ in range(30):
            rand_str += str(random.choice(string.ascii_letters + string.digits))
            return rand_str



def kakao_social_login(request):
    """
    카카오 소셜 로그인 요청 함수, https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api#before-you-begin-process
    카카오톡에 앱키를 담아 사용자에게 /oauth/authorize/에 카카오 로그인 요청
    """
    if request.method == 'GET':
        client_id = 'b69e5d10ed989fce828f23f98a5265d9'
        redirect_uri = 'http://127.0.0.1:8000/account/login/kakao/callback' # 인가 코드를 받을 URI
        return redirect(
            f'https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code'
        )



def kakao_social_login_callback(request):
    """
    카카오 소셜 로그인 콜백 함수
    받은 인가 코드, 애플리케이션 정보를 담아 /oath/token/에 post요청하여 접근코드를 받아 처리하는 함수
    """
    try:
        code = request.GET.get('code')
        client_id = 'b69e5d10ed989fce828f23f98a5265d9'
        redirect_uri = 'http://127.0.0.1:8000/account/login/kakao/callback' # 인가 코드가 리다이렉트된 URI
        token_request = requests.post(
            'https://kauth.kakao.com/oauth/token', {'grant_type': 'authorization_code',
                                                    'client_id': client_id, 'redierect_uri': redirect_uri, 'code': code}
        )
        
        token_json = token_request.json()

        error = token_json.get('error', None)

        if error is not None:
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

    #------회원 정보 조회 및 가입 처리------#

    if UserModel.objects.filter(kakao_id=kakao_id).exists():
        user = UserModel.objects.get(kakao_id=kakao_id)
        auth.login(request, user)
    else:
        UserModel.objects.create(
            username=username,
            nickname=get_random_nickname(),
            password=get_random_password(),
            kakao_id=kakao_id,
        )
        user = UserModel.objects.get(kakao_id=kakao_id)
        auth.login(request, user)
    return redirect('/')


###user_update##



@login_required
def update(request):
    # get 요청시 페이지를 보여준다.
    if request.method == 'GET':
        return render(request, 'user/update.html')
    elif request.method == 'POST':
        # 요청한 유저를 user로 정해준다.
        user = request.user
        bio = request.POST.get('bio')
        email = request.POST.get('email')
        username = request.POST.get('username')
        nickname = request.POST.get('nickname')
        # filter 를 활용해서 가져온 인스턴스와 입력한 인스턴스를 비교하는 변수를 만들어준다.
        exist_nickname = get_user_model().objects.filter(nickname=nickname)
        exist_username = get_user_model().objects.filter(username=username)
        # 닉네임은 중복이 불가한 컬럼이다. 회원정보 수정시 원래 닉네임과 같으면 변경이 안되는 걸 막기위한 코드다.

        # TODO
        # 입력한 닉네임과 db에 저장되어있는 닉네임이 중복되고 내 닉네임과 다르다면 에러창을 띄운다.
        if exist_nickname and user.nickname != nickname:
            return render(request, 'user/update.html', {'error': '이미 사용중인 nickname 입니다.'})
        elif exist_username and user.username != username:
            return render(request, 'user/update.html', {'error': '이미 사용중인 username 입니다.'})
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
        # 요청유저 인식
        user = request.user
        origin_password = request.POST["origin_password"]
        #장고가 제공한 기능을 통해서 현재 비밀번호와 신규 비밀번호를 비교한다.
        if check_password(origin_password, user.password):
            new_password = request.POST["new_password"]
            confirm_password = request.POST["confirm_password"]
            #현재 비밀번호와 신규 비밀번호를 비교하고 현재 비밀번호와 신규 비밀번호 확인을 비교하여 오류를 띄워준다.
            if origin_password == confirm_password or new_password == origin_password:
                return render(request, 'user/change_password.html', {'error': '사용하고 있는 비밀번호를 입력하셨습니다.'})
            #새 비밀번호와 새 비밀번호 확인이 같아야 비밀번호를 저장한다.
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

#회원탈퇴



def delete(request):
    if request.method == "POST":
        user=request.user
        email=request.POST.get('email')
        password=request.POST.get('password')

        #장고기능으로 입력비밀번호와 현재비밀번호를 확인
        if check_password(password, user.password):
            email==user.email
            user.delete()
            return redirect('/user/join/')
        elif email!=user.email or password!=user.password:
            return render(request, 'user/delete.html', {'error': '비밀번호와 이메일을 다시 확인하세요.'})

    else:
        return render(request, 'user/delete.html')

### 로그아웃 ###
@login_required
def logout(request):
    auth.logout(request)
    return redirect('/user/login/')


###이메일 인증
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from user.forms import PasswordResetForm


class PasswordResetView(auth_views.PasswordResetView):
    """
    비밀번호 초기화 - 사용자ID, email 입력
    """
    template_name = 'user/password_reset.html'
    # success_url = reverse_lazy('password_reset_done')
    form_class = PasswordResetForm
    # email_template_name = 'common/password_reset_email.html'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    """
    비밀번호 초기화 - 메일 전송 완료
    """
    template_name = 'user/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """
    비밀번호 초기화 - 새로운 비밀번호 입력
    """
    template_name = 'user/password_reset_confirm.html'
    success_url = reverse_lazy('login')