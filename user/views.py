from django.shortcuts import render, redirect
from .models import UserModel, FollowModel
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.


def join(request):
    return render(request, 'user/join.html')


@login_required(login_url='user:login')
def switch_follow(request,user_id):
    user = UserModel.objects.get(pk=request.user.id)
    follow = UserModel.objects.get(pk=user_id)

    try:
        follower = FollowModel.objects.get(user=user, follow=follow)
        follower.delete()
    except FollowModel.DoesNotExist:
        FollowModel.objects.create(user=user, follow=follow)
    return JsonResponse({'msg':'success'})

"""
def sign_up_view(request):
    if request.method=='GET':
        return render(request, 'user/signup.html')
    elif request.method=='POST':
        name=request.POST.get('name', None)
        password=request.POST.get('password', None)
        password2=request.POST.get('password2', None)
        email=request.POST.get('email',None)
        user_id=request.POST.get('user_id',None)
        
        if password != password2:
            return render(request, 'user/signup.html')
        else:
            new_user = UserModel()
            new_user.name=name
            new_user.password=password
            new_user.email=email
            new_user.user_id
"""


### 로그인 ###

def login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(request, email=email, password=password)

        if user is not None:
            auth.login(request, user)  # 로그인 처리
            return render(request, 'index.html')

        else:
            return render(request, 'join.html')


### 로그아웃 ###
@login_required
def logout(request):
    auth.logout(request)
    return redirect('/user/login')
