from email.mime import image
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
from story.models import Story
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

        my_post = PostModel.objects.create(author=user, content=content)
        my_image = ImageModel.objects.create(
            post=my_post, image=image, image_name=image_name)

        return render(request, 'index.html')


@login_required(login_url='login')
def post_update(request, post_id):
    if request.method == 'POST':

        post = PostModel.objects.get(id=post_id)
        # image = ImageModel.objects.get(post_id=post_id)
        post.content = request.POST.get('content', '')
        # image.image = request.FILES.get('file')
        # image.image_name = request.POST.get('image', '')
        post.save()
        # image.save()

        # my_post = PostModel.objects.create(author=user, content=content)
        # my_image = ImageModel.objects.create(
        #     post=my_post, image=image, image_name=image_name).update(available=False)

        return render(request, 'index.html')


def make_post(user, post_list):
    post_dict_list = []
    # instance = {
    #     'like': 0 or 1,
    #     'post': PostModel...,
    #     'comments': ,
    #     'bookmark' : 0 or 1
    # }
    for post in post_list:
        instance = {}
        if LikeModel.objects.filter(user=user, post=post).exists():
            instance['like'] = 1
        else:
            instance['like'] = 0

        if BookMarkModel.objects.filter(user=user, post=post).exists():
            instance['bookmark'] = 1
        else:
            instance['bookmark'] = 0

        instance['post'] = post
        instance['like_cnt'] = LikeModel.objects.filter(post=post).count()
        instance['comments'] = CommentModel.objects.filter(
            post=post).order_by('-created_at')

        post_dict_list.append(instance)

    return post_dict_list



@login_required(login_url='login')
def index(request):
    user = request.user
    if request.method == 'GET':

        user = request.user
        post_list = PostModel.objects.all().order_by('-id')
        followers = [f.follow for f in FollowModel.objects.filter(user=user)[:6]]
        all_story_author = get_storys_author(request)
        post_list = make_post(user, post_list)
        user_story = Story.objects.filter(author = user, is_end = False)

        context = {
            'followers': followers,
            'post_list': post_list,
            'authors': all_story_author[0],
            'viewed_authors': all_story_author[1],
            'user_story' : user_story,
        }
    return render(request, 'index.html', context)


def profile(request, nickname):
    user = request.user
    author = UserModel.objects.get(nickname=nickname)
    author_post = PostModel.objects.filter(author=author)
    author_bookmark_post = [
        mark.post for mark in BookMarkModel.objects.filter(user=author)]
    author_following = [
        men.follow for men in FollowModel.objects.filter(user=author)]
    author_follower = [
        men.user for men in FollowModel.objects.filter(follow=author)]

    is_author = False
    if nickname == user.nickname:
        is_author = True

    context = {
        'author': author,
        'author_post': author_post,
        'author_bookmark_post': author_bookmark_post,
        'author_following': author_following,
        'author_follower': author_follower,
        'is_author': is_author,
    }
    return render(request, 'post/profile.html', context)


def post_detail(request, post_id):
    # instance = {
    #     'like': 0 or 1,
    #     'post': PostModel...,
    #     'comments': ,
    #     'bookmark' : 0 or 1
    # }
    user = request.user
    post = PostModel.objects.get(pk=post_id)
    context = dict(make_post(user, [post])[0])
    print(context)
    return render(request, 'post/post_detail.html', context)


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

        try:
            is_like = LikeModel.objects.get(post=post, user=user)
            is_like.delete()

            return redirect('/')

        except LikeModel.DoesNotExist:
            like_model.is_like = True
            like_model.post = post
            like_model.user = user
            like_model.save()

            return redirect('/')


@login_required
def switch_bookmark(request, post_id):
    if request.method == 'GET':
        bookmark = BookMarkModel()  # 라이크 모델 인스턴스
        user = request.user  # 유저 불러오기

        post = PostModel.objects.get(id=post_id)  # 포스트 아이디 참조

        try:
            is_bookmark = BookMarkModel.objects.get(post=post, user=user)
            is_bookmark.delete()

            return redirect('/')

        except BookMarkModel.DoesNotExist:
            bookmark.post = post
            bookmark.user = user
            bookmark.save()

            return redirect('/')


@login_required
def post_delete(request, post_id):
    user = request.user
    post = PostModel.objects.get(id=post_id)
    if user == post.author:
        post.delete()
    return redirect('/')


@login_required
def comment_delete(request, comment_id):
    user = request.user
    comment = CommentModel.objects.get(id=comment_id)

    if user == comment.author or user == comment.post.author:
        comment.delete()
    return redirect('/')
