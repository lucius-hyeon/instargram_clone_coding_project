from email.mime import image
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from user.models import FollowModel, UserModel
from .models import Story, StoryViewed
# Create your views here.
# 사용자와 팔로우 한사람들 가져온다
# 팔로우 한 사람들의 스토리가 24시간이 지난 것들은 업데이트 해준다
# 그 다음 스토리뷰 모델에 작성자의 스토리가 있다면 본 스토리에 넣는다
# 팔로우 한 사람들의 스토리를 담는다(시간 정보 작성자, 이미지)

# 나의 그림을 맨 앞으로 뺀다
# 봤을 경우 그 사람의 스토리뷰에 모두 추가한다
# 나의 스토리가 없다면 업데이트하게 만들어준다.
# 스토리 삭제의 경우 작성자가 현재의 유저와 같아야 삭제 가능하게 만든다.
@login_required(login_url='login')
def create_story(request):
    user = request.user
    image = request.POST.get('image', '')
    if image == '':
        return redirect('/')
    Story.objects.create(author = user, image =  image)


@login_required(login_url='login')
def view_story(request, username):
    author = UserModel.objects.get(username = username)
    user = request.user
    storys = Story.objects.filter(author = author, is_end = False)
    for story in storys:
        try:
            StoryViewed.objects.get(story = story, user = user)
        except StoryViewed.DoesNotExist:
            StoryViewed.objects.create(story = story, user = user)
    return render(request, 'story/story_view.html', {'storys' :storys})


def get_storys_author(request):
    user = request.user
    followings =[ f.follow for f in  FollowModel.objects.filter(user = user)]
    story_authors = []
    viewed_story_authors = []
    for follow in followings:
        instance_list = []
        user_storys = Story.objects.filter(author = follow, is_end = False)
        for story in user_storys:
            if (timezone.now() - timedelta(days=1)) > story.created_at:
                story.is_end = True
                story.save()
                continue
            instance_list.append(story)
        for story in instance_list:
            try:
                StoryViewed.objects.get(story = story, user = user)
                viewed_story_authors.append(story.author)
                # viewed_storys.append({ story.author : instance_list })
                break
            except StoryViewed.DoesNotExist:
                story_authors.append(story.author)
                # storys.append({ story.author :instance_list})
                break
    return story_authors, viewed_story_authors