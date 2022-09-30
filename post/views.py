import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from post.models import ImageModel, PostModel
from user.models import FollowModel
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
    followers = FollowModel.objects.filter(user=user)

    context = {
        'follower': followers,
        # 'storys' : get_sorted_story(user),
    }
    return render(request, 'index.html', context)
