from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user.models import FollowModel
# Create your views here.


@login_required(login_url='user:login')
def index(request):
    user = request.user
    followers = FollowModel.objects.filter(user=user)

    context = {
        'follower': followers,
        # 'storys' : get_sorted_story(user),
    }
    return render(request, 'index.html', context)
