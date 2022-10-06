from atexit import register
from email.mime import image
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from user.models import FollowModel, UserModel
from .models import Story, StoryViewed


@login_required(login_url='login')
def create_story(request):
    user = request.user
    image = request.FILES.get('image', '')
    print(request.FILES)
    print(request.POST)
    if image == '':
        return redirect('/')
    Story.objects.create(author = user, image = image)
    return redirect('/')


@login_required(login_url='login')
def view_story(request, nickname):
    author = UserModel.objects.get(nickname=nickname)
    user = request.user
    storys = Story.objects.filter(author=author, is_end=False)
    for story in storys:
        try:
            StoryViewed.objects.get(story=story, user=user)
        except StoryViewed.DoesNotExist:
            StoryViewed.objects.create(story=story, user=user)
    return render(request, 'story/story_view.html', {'storys': storys})


def get_storys_author(request):
    user = request.user
    followings = [f.follow for f in FollowModel.objects.filter(user=user)]
    story_authors = []
    viewed_story_authors = []
    for follow in followings:
        instance_list = []
        user_storys = Story.objects.filter(author=follow, is_end=False)
        for story in user_storys:
            if (timezone.now() - timedelta(days=1)) > story.created_at:
                story.is_end = True
                story.save()
                continue
            instance_list.append(story)
        if len(instance_list) != 0:
            for story in instance_list:
                try:
                    StoryViewed.objects.get(story=story, user=user)
                except StoryViewed.DoesNotExist:
                    story_authors.append(story.author)
                    break
            else:
                viewed_story_authors.append(story.author)

    return story_authors, viewed_story_authors


def simple_time(value):
    if 'hour' in value:
        value = value.split('hour')[0]
        return f'{value}시간'
    value = value.split(' ')[0]
    return f'{value}분'
