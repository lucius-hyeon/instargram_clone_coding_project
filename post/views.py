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
from post.models import ImageModel, PostModel, LikeModel, CommentModel, BookMarkModel, ReplyCommentModel
from story.models import Story
from user.models import FollowModel, UserModel
from story.views import get_storys_author

# Create your views here.

# 게시글 추가하기


@login_required(login_url='logn')
def post_add(request):
    if request.method == 'POST':
        # TODO 이미지 없어도 되는지 확인해보기.
        user = request.user
        content = request.POST.get('content', '')

        image = request.FILES.get('file')
        image_name = request.POST.get('image', '')

        my_post = PostModel.objects.create(author=user, content=content)
        my_image = ImageModel.objects.create(
            post=my_post, image=image, image_name=image_name)

        return render(request, 'index.html')

# 게시글 수정하기


@login_required(login_url='login')
def post_update(request, post_id):
    if request.method == 'POST':

        post = PostModel.objects.get(id=post_id)
        post.content = request.POST.get('content', '')
        post.save()
        # 이미지가 변경되었을 때만 이미지 새로 저장
        if request.FILES.get('file') != None:
            image = ImageModel.objects.get(post_id=post_id)
            image.image = request.FILES.get('file')
            image.image_name = request.POST.get('image', '')
            image.save()

        return render(request, 'index.html')

# 게시글 필요 정보 모아서 저장하기


def make_post(user, post_list):
    post_dict_list = []
    # instance = {
    #     'like': 0 or 1,
    #     'like_cnt': 0 or 1,
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

# index.html 게시글 목록 가지고 오기


@login_required(login_url='login')
def index(request):
    user = request.user
    if request.method == 'GET':

        user = request.user
        post_list = PostModel.objects.all().order_by('-id')
        followers = [f.follow for f in FollowModel.objects.filter(user=user)[
            :6]]
        all_story_author = get_storys_author(request)
        post_list = make_post(user, post_list)
        user_story = Story.objects.filter(author=user, is_end=False)

        reply_comment = ReplyCommentModel.objects.all()

        context = {
            'followers': followers,
            'post_list': post_list,
            'authors': all_story_author[0],
            'viewed_authors': all_story_author[1],
            'user_story': user_story,
            'recomments': reply_comment
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
    author_follower_1 = [
<<<<<<< HEAD
        men.user for men in FollowModel.objects.filter(follow=author) if FollowModel.objects.filter(user = user, follow = men.user).exists()
    ]
    author_follower_0 = [
        men.user for men in FollowModel.objects.filter(follow=author) if not FollowModel.objects.filter(user = user, follow = men.user).exists()
=======
        men.user for men in FollowModel.objects.filter(follow=author) if FollowModel.objects.filter(user=user, follow=men.user).exists() is not None
    ]
    author_follower_0 = [
        men.user for men in FollowModel.objects.filter(follow=author) if FollowModel.objects.filter(user=user, follow=men.user).exists() is None
>>>>>>> f1a5d025612f54740b3a8b9345b71106bc934d35
    ]
    follower_cnt = len(author_follower_0 + author_follower_1)
    print(FollowModel.objects.filter(user = user, follow = user).exists())

    # 해당주인의 팔로워가 내가 팔로잉 한 사람인지 판단하는 방법은?
    # 생각 1. followmodel에서 user = user follow = 계정주인팔로워
    # 생각 2. 나의 팔로잉모델(follow추출)에서 계정 주인 팔로워가 있냐 판단

    is_author = False
    if nickname == user.nickname:
        is_author = True

    context = {
        'author': author,
        'author_post': author_post,
        'author_bookmark_post': author_bookmark_post,
        'author_following': author_following,
        'author_follower_0': author_follower_0,
        'author_follower_1': author_follower_1,
        'follower_cnt': follower_cnt,
        'is_author': is_author,
    }
    return render(request, 'post/profile.html', context)

# 게시글 상세페이지


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

#경민 - 변경예정
# 내가 팔로잉한 사람의 친구를 추천하려는 함수 (30명)
# 부족하다면 모든 사용자에서 부족한 만큼 채워서 보낸다.
# 나의 친구의 친구를 추천하고 부족한 만큼 채워서 보여줄 때, 친구의 친구와 겹치지 않게 시도했다.


def recommand_user(request, username):
    user = request.user
    unfollowers = []
    followers_set = [f.follow for f in FollowModel.objects.filter(user=user)]
    followers = FollowModel.objects.filter(user=user)[:5]
    for f in followers:
        f_list = FollowModel.objects.filter(
            user=f.follow).exclude(user=user)[:5]
        for r in f_list:
            if r in followers_set:
                continue
            unfollowers.append(r.follow)
    if len(unfollowers) <= 30:
        ufl = 30 - len(unfollowers)
        fl = UserModel.objects.all().exclude(nickname=user.nickname)[:ufl]
        unfollowers += fl
    unfollowers = set(unfollowers) - set(followers_set)
    context = {'unfollowers': unfollowers}
    print(list(set(unfollowers)))
    return render(request, 'post/recommand.html', context)

# 댓글


@login_required
def comment(request, post_id):
    if request.method == 'POST':

        content = request.POST.get('content')

        # 입력칸이 빈칸이라면 처리 안됨.
        if content == '':
            return redirect('/')

        user = request.user
        # 포스트  아이디를 통해 포스트 모델 가져온다.
        post = PostModel.objects.get(id=post_id)

        # 받아온 데이터들을 CommentModel에 저장
        cm = CommentModel()
        cm.content = content
        cm.author = user
        cm.post = post
        cm.save()

        return redirect('/')


# 좋아요
@login_required
def is_like(request, post_id):
    if request.method == 'GET':
        like_model = LikeModel()  # 라이크 모델 인스턴스
        user = request.user  # 유저 불러오기

        post = PostModel.objects.get(id=post_id)  # 포스트 아이디 참조

        # 라이크 모델이 있을 경우 (라이크 모델 삭제)
        try:
            is_like = LikeModel.objects.get(post=post, user=user)
            is_like.delete()

            return redirect('/')

        # 라이크 모델이 없을 경우 (라이크 모델 생성)
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

        # 북마크 있을경우 삭제
        try:
            is_bookmark = BookMarkModel.objects.get(post=post, user=user)
            is_bookmark.delete()

            return redirect('/')
        # 북마크 없을 경우 생성
        except BookMarkModel.DoesNotExist:
            bookmark.post = post
            bookmark.user = user
            bookmark.save()

            return redirect('/')

# 게시글 삭제


@login_required
def post_delete(request, post_id):
    user = request.user
    post = PostModel.objects.get(id=post_id)
    if user == post.author:
        post.delete()
    return redirect('/')

# 댓글 삭제


@login_required
def comment_delete(request, comment_id):
    user = request.user
    comment = CommentModel.objects.get(id=comment_id)

    # 코멘트를 쓴 사람과 유저과 같거나 포스트를 쓴 사람이 유저라면 삭제 가능
    if user == comment.author or user == comment.post.author:
        comment.delete()
    return redirect('/')


# 대댓글 삭제
@login_required
def replycomment_delete(request, post_id, comment_id):
    user = request.user
    reply_comment = ReplyCommentModel.objects.get(id=comment_id)

    # 게시글 작성자, 게시글의 댓글 작성자 , 댓글의 댓글 작성자가 맞다면 삭제할 수 있다
    if user == reply_comment.author or user == reply_comment.post.author or user == reply_comment.comment.author:
        reply_comment.delete()
    return redirect('/')


# 대댓글 생성
@ login_required
def replycomment(request, post_id, comment_id):
    if request.method == "POST":
        user = request.user
        post = PostModel.objects.get(id=post_id)
        comment = CommentModel.objects.get(id=comment_id)
        content = request.POST.get('relpy')

        ReplyCommentModel.objects.create(
            content=content,
            author=user,
            comment=comment,
            post=post
        )
    return redirect('/')
