from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user.models import FollowModel, UserModel
# Create your views here.


@login_required(login_url='login')
def index(request):
    user = request.user
    followers = FollowModel.objects.filter(user=user)[:6]
    context = {
        'followers': followers,
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
        f_list = FollowModel.objects.filter(user=f.follow).exclude(user=user)[:5]
        for r in f_list:
            if r in followers_set:
                print('zz')
                continue
            unfollowers.append(r.follow)
    if len(unfollowers) <= 30:
        ufl = 30 - len(unfollowers)
        fl  = UserModel.objects.all().exclude(username=user.username)[:ufl]
        unfollowers += fl
    unfollowers = set(unfollowers) - set(followers_set)
    context = {'unfollowers' : unfollowers}
    print(list(set(unfollowers)))
    return render(request, 'post/recommand.html', context)