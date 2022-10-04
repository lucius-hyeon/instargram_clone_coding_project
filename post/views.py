import re
from xml.etree.ElementTree import Comment
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from post.models import ImageModel, PostModel,UserModel,CommentModel,LikeModel
from user.models import FollowModel
from django.http import JsonResponse
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
    if request.method == 'GET':

        #post_id로 comment걸러야 하는데 그걸 못하고 있음.

        #임의로 넣어준 username
        user = UserModel.objects.get(username ='su' )


        cm = CommentModel.objects.all()
        
        
        return render(request, 'index.html', {'comments':cm})
        
    user = request.user
    followers = FollowModel.objects.filter(user=user)[:6]
    context = {
        'followers': followers,
        # 'storys' : get_sorted_story(user),
    }
    return render(request, 'index.html')


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



@login_required
def comment(request , post_id):
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
def comments_list(request, post_id):
    if request.method == 'GET':
        print('댓글 get 실행')
            # post = PostModel.objects
            # cm = CommentModel.objects.filter(post_id = post_id)

            # return render(request, 'index.html', {'comment':cm})
        return render(request, 'index.html')

# @login_required
# def is_like(request, post_id):
#     if request.method =='GET':
#         like_model = LikeModel() #라이크 모델 인스턴스
#         user = request.user #유저 불러오기       
       
#         post = PostModel.objects.get(id = post_id) # 포스트 아이디 참조

        
#         try:
#             is_like = LikeModel.objects.get(post = post, user = user)
            
#             if is_like =='True' :
#                 print('True')
#             else:
#                 print('false')
           
#             like_model.save()
        
#             return render(request, 'index.html', {'like':is_like})
            
#         except LikeModel.DoesNotExist:
#             print('예예외')
#             #데이터가 없으면 true로 바꿔준다ㅣ.
#             like_model.is_like = True
#             like_model.post = post
#             like_model.user = user
#             like_model.save()
        
#             return render(request, 'index.html', {'like':is_like})



@login_required
def is_like(request, post_id):
    if request.method =='GET':
        like_model = LikeModel() #라이크 모델 인스턴스
        user = request.user #유저 불러오기       
       
        post = PostModel.objects.get(id = post_id) # 포스트 아이디 참조

        print(post)
        print(like_model)
        
        try:
            is_like = LikeModel.objects.get(post = post, user = user)
            is_like.delete()
            
            return render(request, 'index.html', {'like':False})
            
        except LikeModel.DoesNotExist:
            like_model.is_like = True
            like_model.post = post
            like_model.user = user
            like_model.save()

            print(like_model)


            return render(request, 'index.html', {'like':True})


@login_required
def post_like(request, post_id):
    if request.method =='GET':
        user = request.user #유저 불러오기
       
        post = PostModel.objects.get(pk = post_id) # 포스트 아이디 참조
        
        try:
            like = LikeModel.objects.get(post = post, user = user)
            like.delete()
            return JsonResponse({ 'msg' : 'unlike'} )
        except LikeModel.DoesNotExist:
            print('예예외')

            LikeModel.objects.create(user = user, post = post, is_like = True)
            return JsonResponse({'msg' : 'like'})