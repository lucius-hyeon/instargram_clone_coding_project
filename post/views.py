import os
from uuid import uuid4
from django.core.files.storage import FileSystemStorage  # 파일저장

import re
from xml.etree.ElementTree import Comment
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from instargram.settings import MEDIA_ROOT
from post.models import ImageModel, PostModel, LikeModel, CommentModel, BookMarkModel
from user.models import FollowModel, UserModel
from story.views import get_storys_author

# Create your views here.


def test_html(request):
    # return render(request, 'post/temp_home.html')
    return render(request, 'post/test.html')


@login_required(login_url='login')
def post_add(request):
    if request.method == 'POST':

        user = request.user
        content = request.POST.get('content', '')
        image = request.FILES.get('file')
        image_name = request.POST.get('image', '')

        # image_name = uuid4().hex
        # save_path = os.path.join(MEDIA_ROOT, image_name)
        # with open(save_path, 'wb+') as destination:
        #     for chunk in image.Chunk():
        #         destination.write(chunk)

        # for image in request.FILES.getlist(key):
        #     section = get_object_or_404(Section, pk = section_id[key])
        #     ig = Image(section = section, image = image)
        #     ig.save()

        my_post = PostModel.objects.create(author=user, content=content)
        my_image = ImageModel.objects.create(
            post=my_post, image=image, image_name=image_name)

        return render(request, 'index.html')


@login_required(login_url='login')
def index(request):
    user = request.user
    if request.method == 'GET':

        user = request.user
        post_list = PostModel.objects.all().order_by('-id')
        image_list = ImageModel.objects.all().order_by('-post_id')
        # followers = FollowModel.objects.filter(user=user)[:6]
        followers = [f.follow for f in FollowModel.objects.filter(user=user)[:6]]
        all_story_author = get_storys_author(request)

        cm = CommentModel.objects.all()
        context = {
            'followers': followers,
            'post_list': post_list,
            'image_list': image_list,
            'comments': cm,
            'authors' : all_story_author[0],
            'viewed_authors' : all_story_author[1],
        }
    return render(request, 'index.html', context)


def profile(request, nickname):
    user = request.user
    print(dir(user))
    print(user.follow)
    author = UserModel.objects.get(nickname = nickname)
    author_post = PostModel.objects.filter(author = author)
    author_bookmark_post = [mark.post for mark in BookMarkModel.objects.filter(user = author)]
    author_following = [men.follow for men in FollowModel.objects.filter(user = author)]
    author_follower = [men.user for men in FollowModel.objects.filter(follow = author)]
    is_author = False
    if nickname == user.nickname:
        is_author = True
    for post in author_post:

        post_dict = {"thumbnail":'', 'post' : ''}
    context = {
        'author' : author,
        'author_post' : author_post,
        'author_bookmark_post' : author_bookmark_post,
        'author_following' : author_following,
        'author_follower' : author_follower,
        'is_author' : is_author,
    }
    return render(request, 'post/profile.html', context)


def recommand_user(request, username):
    user = request.user
    print(user)
    unfollowers = []
    followers_set = [f.follow for f in FollowModel.objects.filter(user=user)]
    followers = FollowModel.objects.filter(user=user)[:5]
    for f in followers:
        f_list = FollowModel.objects.filter(
            user=f.follow).exclude(user=user)[:5]
        for r in f_list:
            if r in followers_set:
                print('zz')
                continue
            unfollowers.append(r.follow)
    if len(unfollowers) <= 30:
        ufl = 30 - len(unfollowers)
        fl = UserModel.objects.all().exclude(username=user.username)[:ufl]
        unfollowers += fl
    unfollowers = set(unfollowers) - set(followers_set)
    context = {'unfollowers': unfollowers}
    print(list(set(unfollowers)))
    return render(request, 'post/recommand.html', context)


@login_required
def comment(request, post_id):
    if request.method == 'POST':

        content = request.POST.get('content')

        if content == '':
            return redirect('/')

        user = request.user
        post = PostModel.objects.get(id=post_id)

        cm = CommentModel()
        cm.content = content
        cm.author = user
        # cm.liker = liker.set()
        cm.post = post
        cm.save()

        return redirect('/')


@login_required
def comments_list(request, post_id):
    if request.method == 'GET':
        print('댓글 get 실행')
        # post = PostModel.objects
        # cm = CommentModel.objects.filter(post_id = post_id)

        # return render(request, 'index.html', {'comment':cm})
        return render(request, 'index.html')


@login_required
def is_like(request, post_id):
    if request.method == 'GET':
        like_model = LikeModel()  # 라이크 모델 인스턴스
        user = request.user  # 유저 불러오기

        post = PostModel.objects.get(id=post_id)  # 포스트 아이디 참조

        print(post)
        print(like_model)

        try:
            is_like = LikeModel.objects.get(post=post, user=user)
            is_like.delete()

            return render(request, 'index.html', {'like': False})

        except LikeModel.DoesNotExist:
            like_model.is_like = True
            like_model.post = post
            like_model.user = user
            like_model.save()

            print(like_model)

            return render(request, 'index.html', {'like': True})