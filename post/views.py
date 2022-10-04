import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from post.models import BookMarkModel, ImageModel, PostModel
from user.models import FollowModel, UserModel
from story.views import get_storys_author
# Create your views here.



def test_html(request):
    # return render(request, 'post/temp_home.html')
    return render(request, 'post/test.html')


@login_required(login_url='login')
def post_add(request):
    if request.method == 'POST':
        # author = request.POST.get('user_id', '')
        user = request.user
        content = request.POST.get('content', '')
        image = request.POST.get('image', '')

        my_post = PostModel.objects.create(author=user, content=content)
        my_image = ImageModel.objects.create(post=my_post, image=image)

        return render(request, 'index.html')


@login_required(login_url='login')
def index(request):
    user = request.user
    followers = [f.follow for f in FollowModel.objects.filter(user=user)[:6]]
    all_story_author = get_storys_author(request)
    context = {
        'followers': followers,
        'authors' : all_story_author[0],
        'viewed_authors' : all_story_author[1],
        # 'storys' : get_sorted_story(user),
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
