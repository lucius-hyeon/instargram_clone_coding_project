from atexit import register
from email.mime import image
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from user.models import FollowModel, UserModel
from .models import Story, StoryViewed

# 스토리 생성 함수


@login_required(login_url='login')
def create_story(request):
    user = request.user
    image = request.FILES.get('image', '')
    if image == '':
        return redirect('/')
    Story.objects.create(author = user, image = image)
    return redirect('/')

# 특정 작성자의 스토리 렌더 함수
# 특정 작성자가 쓴 스토리를 모두 가져오고(24시간이 지나지 않은)
# 특정 작성자의 스토리를 요청 사용자가 모두 본 것으로 처리한다.


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

# 로그인한 사용자의 팔로잉한 사람들의 스토리를 안 본 것과 본 것을 나눠보네는 함수


# 로그인한 사용자의 팔로잉한 사람들의 스토리를 안 본 것과 본 것을 나눠보네는 함수


def get_storys_author(request):
    user = request.user
    # 현재 로그인한 사람이 팔로잉한 사람들
    followings = [f.follow for f in FollowModel.objects.filter(user=user).exclude(follow = user)]
    new_story_authors = []
    viewed_story_authors = []
    for follow in followings:
        # 유효한 스토리(24시간이 지나지 않은 스토리)가 하나라도 있는지 판별할 변수이다.
        is_valid = False
        # 팔로잉한 사람의 스토리를 한명씩 가져옴
        user_storys = Story.objects.filter(author=follow, is_end=False)
        for story in user_storys:
            # 그 스토리의 시간이 24시간이 지났다면 유효성이 끝났음을 처리한다.
            if (timezone.now() - timedelta(days=1)) > story.created_at:
                story.is_end = True
                story.save()
                continue
            # 유효하다면 해당 스토리 작성자는 유효함을 남긴다.
            is_valid = True
            try:
                StoryViewed.objects.get(story=story, user=user)
            except StoryViewed.DoesNotExist:
                # 본 스토리가 아니라면 보지않은 스토리 작성자에 넣어준다.
                new_story_authors.append(story.author)
                break
        # 유효기간이 지난 스토리 혹은 다 봤던 스토리
        else:
            # 유효기간이 지나지 않은 스토리가 하나라도 있나
            if is_valid:
                viewed_story_authors.append(story.author)
    return new_story_authors, viewed_story_authors


# 템플릿 태그 함수를 만드려는 함수(미완)
def simple_time(value):
    if 'hour' in value:
        value = value.split('hour')[0]
        return f'{value}시간'
    value = value.split(' ')[0]
    return f'{value}분'
