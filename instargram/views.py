from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from user.models import FollowModel

def test_html(request):
    return render(request, 'post.html')
