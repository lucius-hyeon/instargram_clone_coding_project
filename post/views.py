import os
from uuid import uuid4
from django.core.files.storage import FileSystemStorage  # 파일저장

import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from instargram.settings import MEDIA_ROOT
from post.models import ImageModel, PostModel
from user.models import FollowModel, UserModel
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
    post_list = PostModel.objects.all().order_by('-id')
    image_list = ImageModel.objects.all().order_by('-post_id')
    followers = FollowModel.objects.filter(user=user)[:6]
    context = {
        'followers': followers,
        'post_list': post_list,
        'image_list': image_list,
        # 'storys' : get_sorted_story(user),
    }
    return render(request, 'index.html', context)


def profile(request, username):
    context = {}
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
