from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from post.models import ImageModel, PostModel, LikeModel, CommentModel, BookMarkModel, ReplyCommentModel
from story.models import Story
from user.models import FollowModel, UserModel
from story.views import get_storys_author

# def index(request):
#     if request.method=='GET':
#         return render(request, 'user/login.html')
    

@login_required(login_url='login')
def post_add(request):
    if request.method == 'POST':

        user = request.user
        content = request.POST.get('content', '')
        image = request.FILES.get('file')
        image_name = request.POST.get('image', '')

        my_post = PostModel.objects.create(author=user, content=content)
        my_image = ImageModel.objects.create(
            post=my_post, image=image, image_name=image_name)

        return render(request, 'index.html')

#login이라는 이름의 url로 이동시켜준다
@login_required(login_url='login')
def post_update(request, post_id):
    if request.method == 'POST':

        post = PostModel.objects.get(id=post_id)
        post.content = request.POST.get('content', '')
        post.save()
        if request.FILES.get('file') != None:
            image = ImageModel.objects.get(post_id=post_id)
            image.image = request.FILES.get('file')
            image.image_name = request.POST.get('image', '')
            image.save()

        return render(request, 'index.html')

#힌트일 뿐 post_list: list 없어도 된다 : list
def make_post(user, post_list: list):
    """
    Return post_list with detail informations
        Parameters:
            user (object) : request.user or user object
            post_list (query set) : postmodel object
    """
    post_dict_list = []

    for post in post_list:
        instance = {}
        if LikeModel.objects.filter(user=user, post=post).exists():
            instance['like'] = 1
        else:
            instance['like'] = 0

        if BookMarkModel.objects.filter(user=user, post=post).exists():
            instance['bookmark'] = 1
        else:
            instance['bookmark'] = 0

        instance['post'] = post
        instance['like_cnt'] = LikeModel.objects.filter(post=post).count()
        instance['comments'] = CommentModel.objects.filter(
            post=post).order_by('-created_at')

        post_dict_list.append(instance)

    return post_dict_list


@login_required(login_url='login')
def index(request):
    user = request.user
    if request.method == 'GET':

        user = request.user
        post_list = PostModel.objects.all().order_by('-id')
        followers = [f.follow for f in FollowModel.objects.filter(user=user)[
            :6]]
        all_story_author = get_storys_author(request)
        post_list = make_post(user, post_list)
        user_story = Story.objects.filter(author=user, is_end=False)

        reply_comment = ReplyCommentModel.objects.all()

        context = {
            'followers': followers,
            'post_list': post_list,
            'authors': all_story_author[0],
            'viewed_authors': all_story_author[1],
            'user_story': user_story,
            'recomments': reply_comment
        }
    return render(request, 'index.html', context)


@login_required
def profile(request, nickname):
    """
    개인 프로필의 상세 정보를 가져오는 함수
    """
    user = request.user
    author = UserModel.objects.get(nickname=nickname)
    author_post = PostModel.objects.filter(author=author)

    author_post = author.postmodel_set.all()
    user_followings = [men.follow for men in user.user.all()]
    author_bookmark_post = [
        mark.post for mark in author.bookmarkmodel_set.all()]

    author_following_1 = [
        men.follow for men in author.user.all() if men.follow in user_followings]
    author_following_0 = [
        men.follow for men in author.user.all() if men.follow not in user_followings]
    author_follower_1 = [
        men.user for men in author.follow.all() if men.user in user_followings]
    author_follower_0 = [
        men.user for men in author.follow.all() if men.user not in user_followings]
    follower_cnt = len(author_follower_0 + author_follower_1)
    following_cnt = len(author_following_0 + author_following_1)

    is_author = False

    if nickname == user.nickname:
        is_author = True

    context = {
        'author': author,
        'author_post': author_post,
        'author_bookmark_post': author_bookmark_post,
        'author_following_0': author_following_0,
        'author_following_1': author_following_1,
        'author_follower_0': author_follower_0,
        'author_follower_1': author_follower_1,
        'follower_cnt': follower_cnt,
        'following_cnt': following_cnt,
        'is_author': is_author,
    }
    return render(request, 'post/profile.html', context)


def post_detail(request, post_id):
    user = request.user
    post = PostModel.objects.get(pk=post_id)
    context = dict(make_post(user, [post])[0])
    print(context)
    return render(request, 'post/post_detail.html', context)


def recommand_user(request, nickname):
    """
    사용자가 팔로우한 사람들(친구)의 친구를 추천
    총 추천인(30)을 넘지 않는다면 전체 사용자에서 추가
    총 추천인에서 내가 팔로우한 사람은 제외하여 반환
    """
    user = request.user
    unfollowers = []
    followers_set = [f.follow for f in FollowModel.objects.filter(user=user)]
    followers = FollowModel.objects.filter(user=user)[:5]

    for f in followers:
        f_list = FollowModel.objects.filter(
            user=f.follow).exclude(user=user)[:5]

        for r in f_list:
            if r in followers_set:
                continue

            unfollowers.append(r.follow)

    if len(unfollowers) <= 30:
        ufl = 30 - len(unfollowers)
        fl = UserModel.objects.all().exclude(nickname=user.nickname)[:ufl]
        unfollowers += fl

    unfollowers = set(unfollowers) - set(followers_set)
    context = {'unfollowers': unfollowers}

    return render(request, 'post/recommand.html', context)


@login_required
def comment(request, post_id):
    if request.method == 'POST':

        content = request.POST.get('content')

        if content == '':
            return redirect('/')

        user = request.user
        post = PostModel.objects.get(id=post_id)

        cm = CommentModel()
        cm.content = content
        cm.author = user
        # cm.liker = liker.set()
        cm.post = post
        cm.save()

        return redirect('/')


@login_required
def is_like(request, post_id):
    if request.method == 'GET':
        like_model = LikeModel()  # 라이크 모델 인스턴스
        user = request.user  # 유저 불러오기

        post = PostModel.objects.get(id=post_id)  # 포스트 아이디 참조

        try:
            is_like = LikeModel.objects.get(post=post, user=user)
            is_like.delete()

            return redirect('/')

        except LikeModel.DoesNotExist:
            like_model.is_like = True
            like_model.post = post
            like_model.user = user
            like_model.save()

            return redirect('/')


@login_required
def switch_bookmark(request, post_id):
    if request.method == 'GET':
        bookmark = BookMarkModel()  # 라이크 모델 인스턴스
        user = request.user  # 유저 불러오기

        post = PostModel.objects.get(id=post_id)  # 포스트 아이디 참조

        try:
            is_bookmark = BookMarkModel.objects.get(post=post, user=user)
            is_bookmark.delete()

            return redirect('/')

        except BookMarkModel.DoesNotExist:
            bookmark.post = post
            bookmark.user = user
            bookmark.save()

            return redirect('/')


@login_required
def post_delete(request, post_id):
    user = request.user
    post = PostModel.objects.get(id=post_id)
    if user == post.author:
        post.delete()
    return redirect('/')


@login_required
def comment_delete(request, comment_id):
    user = request.user
    comment = CommentModel.objects.get(id=comment_id)

    if user == comment.author or user == comment.post.author:
        comment.delete()
    return redirect('/')


# 대댓글 삭제
@login_required
def replycomment_delete(request, post_id, comment_id):
    user = request.user
    reply_comment = ReplyCommentModel.objects.get(id=comment_id)

    # 게시글 작성자, 게시글의 댓글 작성자 , 댓글의 댓글 작성자가 맞다면 삭제할 수 있다
    if user == reply_comment.author or user == reply_comment.post.author or user == reply_comment.comment.author:
        reply_comment.delete()
    return redirect('/')


# 대댓글 생성
@ login_required
def replycomment(request, post_id, comment_id):
    if request.method == "POST":
        user = request.user
        post = PostModel.objects.get(id=post_id)
        comment = CommentModel.objects.get(id=comment_id)
        content = request.POST.get('relpy')

        ReplyCommentModel.objects.create(
            content=content,
            author=user,
            comment=comment,
            post=post
        )
    return redirect('/')
