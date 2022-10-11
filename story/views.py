from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from user.models import FollowModel, UserModel
from .models import Story, StoryViewed


@login_required(login_url='login')
def create_story(request):
    """
    create story
    """
    user = request.user
    image = request.FILES.get('image', '')
    if image == '':
        return redirect('/')
    Story.objects.create(author = user, image = image)
    return redirect('/')


@login_required(login_url='login')
def view_story(request, nickname):
    """
    특정 작성자의 유효한 스토리를 반환하고

    해당 작성자의 요한 스토리 모두를 시청 기록으로 저장
    """
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
    """
    Return tuple(시청하지않은_스토리_작성자 : list, 시청한_스토리_작성자 : list)

    팔로잉한 사람들의 스토리를 시청한 것, 시청하지 않은 것으로 나눈다.
    """
    user = request.user
    followings = [f.follow for f in user.user.exclude(follow = user)]
    new_story_authors = []
    viewed_story_authors = []

    for follow in followings:

        is_valid = False # 하나 이상의 유효한 스토리를 확인하는 플래그
        user_storys = Story.objects.filter(author=follow, is_end=False)

        for story in user_storys:
            if (timezone.now() - timedelta(days=1)) > story.created_at:
                story.is_end = True
                story.save()
                continue

            is_valid = True

            try:
                StoryViewed.objects.get(story=story, user=user)
            except StoryViewed.DoesNotExist:
                new_story_authors.append(story.author)
                break # 아직 시청하지 않은 스토리를 확인
        else:
            if is_valid:
                viewed_story_authors.append(story.author)
    return new_story_authors, viewed_story_authors