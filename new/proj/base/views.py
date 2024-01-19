from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail,BadHeaderError
from django.conf import settings
from . import models
from itertools import chain
import random
import subprocess
# Create your views here.
def index(request):
    return render(request,'index.html')

def log_in(request):
    if request.method=="POST":
        username=request.POST['email']
        password=request.POST['password']
        try:
            check=auth.authenticate(username=User.objects.get(email=username),password=password)
        except:
            check=auth.authenticate(username=username,password=password)
        if check is not None:
            auth.login(request,check)
            return redirect('home')
        else:
            messages.info(request,'Credentials Invalid')
            return redirect('login')
        
    return render(request,'login.html')

def register(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        cnfpassword=request.POST['cnfPassword']
        name=request.POST['name']
        if password==cnfpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already Registered')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username Already Taken')
                return redirect('register')
            else:
                new_user=User.objects.create_user(username=username,email=email,password=password)
                new_user.save()
                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                user_model=User.objects.get(username=username)
                new_prof=models.Profile.objects.create(user=user_model,id_user=user_model.id,name=name)
                new_prof.save()
                return redirect('home')
        else:
            messages.info(request,'Password does not match with Confirm password')
            return redirect('register')
    return render(request,'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    user_obj=User.objects.get(username=request.user.username)
    user_profile=models.Profile.objects.get(user=user_obj)
    posts=models.Post.objects.all()
    user_following=models.FollowerCount.objects.filter(follower=request.user.username)
    
    all_user=User.objects.all()
    user_following_all=[]
    for user in user_following:
        user_list=User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestion = [x for x in (all_user) if (x not in (user_following_all))]
    print(new_suggestion)
    current_user=User.objects.filter(username=request.user.username)
    final_list=[x for x in (new_suggestion) if (x not in (current_user))]
    random.shuffle(final_list)
    print(final_list)
    username_profile=[]
    username_profile_list=[]
    for users in final_list:
        username_profile.append(users.id)
    for ids in username_profile:
        profile_lists=models.Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)
        
    suggestions_username_profile_list = list(chain(*username_profile_list))
    print(len(suggestions_username_profile_list))
    return render(request,'home.html',{'posts':posts,'user_profile':user_profile,'suggestions':suggestions_username_profile_list[:4]})

def profile(request,pk):
    user=pk
    user_obj=User.objects.get(username=pk)
    user_prof=models.Profile.objects.get(user=user_obj)
    posts=models.Post.objects.filter(user=user_prof)
    follower=request.user.username
    if models.FollowerCount.objects.filter(follower=follower,user=user):
        button='unfollow'
    else:
        button='follow'

    user_followers=len(models.FollowerCount.objects.filter(user=user))
    user_following_length=len(models.FollowerCount.objects.filter(follower=pk))
    length=len(posts)
    user_following=models.FollowerCount.objects.filter(follower=pk)
    

    all_user=User.objects.all()
    user_following_all=[]
    for user in user_following:
        user_list=User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestion = [x for x in (all_user) if (x not in (user_following_all))]
    print(new_suggestion)
    current_user=User.objects.filter(username=request.user.username)
    final_list=[x for x in (new_suggestion) if (x not in (current_user))]
    random.shuffle(final_list)
    print(final_list)
    username_profile=[]
    username_profile_list=[]
    for users in final_list:
        username_profile.append(users.id)
    for ids in username_profile:
        profile_lists=models.Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)
        
    suggestions_username_profile_list = list(chain(*username_profile_list))
    can_delete=False
    if user_prof.user.username == request.user.username:
        can_delete=True
    context={
        'user_obj':user_obj,
        'user_prof':user_prof,
        'posts':posts,
        'button':button,
        'user_following':user_following_length,
        'user_followers':user_followers,
        'length':length,
        'suggestions':suggestions_username_profile_list[:4],
        'can_delete':can_delete
    }
    return render(request,'profile.html',context)
@login_required(login_url='login')
def post(request):
    user_obj = User.objects.get(username=request.user.username)
    user_prof = models.Profile.objects.get(user=user_obj)
    if request.method=="POST":
        user=request.user.username
        image=request.FILES.get('image')
        caption=request.POST['caption']
        
        new_post=models.Post.objects.create(user=user,image=image,caption=caption,user_profile=user_prof)
        new_post.save()
        return redirect('home')
    else:
        return redirect('home')
    

def community(request):
    if request.method=="POST":
        username=request.POST['username']
        bio=request.POST['bio']
        image=request.FILES.get('image')
        new_community=models.CommunityUser.objects.create(username=username,about=bio,image=image)
        new_community.save()
        new_community_profile=models.CommunityProfile.objects.create(user=new_community,about=bio,profile_imag=image)
        new_community_profile.save()
        return redirect('community')
    
    community_users=models.CommunityUser.objects.all()

    return render(request,'community.html',{'community_users':community_users})



# def communityProfile(request,pk):
#     # user=pk
#     # curr_user=models.CommunityUser.objects.filter(username=user).first()
#     # curr_user_prof=models.CommunityProfile.objects.get(user=curr_user).first()
#     # posts=models.CommunityPost.objects.filter(community_user=user)
#     user=pk
#     user_obj=models.CommunityUser.objects.get(username=pk)
#     user_prof=models.CommunityProfile.objects.get(user=user_obj)
#     posts=models.Post.objects.filter(user=user_prof)
#     context={
#         'profile_details':user_prof,
#         'posts':posts
#     }
#     return render(request,'communityProfile.html',context)


def update(request):
    user_prof=models.Profile.objects.get(user=request.user)
    username=request.user.username
    if request.method=="POST":
        if request.FILES.get('image')==None:
            image=user_prof.profimag
            bio=request.POST['bio']
            name=request.POST['name']
            
            user_prof.profimag=image
            user_prof.bio=bio
            user_prof.name=name
            user_prof.save()
            return redirect('profile/'+username)
        else:
            image=request.FILES.get('image')
            bio=request.POST['bio']
            name=request.POST['name']
            
            user_prof.profimag=image
            user_prof.bio=bio
            user_prof.name=name
            user_prof.save()
            return redirect('profile/'+username)
        
def Like(request):
    username=request.user.username
    post_id=request.GET.get('post_id')
    post=models.Post.objects.get(id=post_id)
    like=models.LikePost.objects.filter(post_id=post_id,username=username).first()

    if like==None:
        new_like=models.LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.likes=post.likes+1
        post.save()
        return redirect('home')
    else:
        like.delete()
        post.likes=post.likes-1
        post.save()
        return redirect('home')

def follow(request):
    if request.method=="POST":
        follower=request.POST['follower']
        user=request.POST['user']
        if models.FollowerCount.objects.filter(follower=follower,user=user).first():
            delete_follower=models.FollowerCount.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect('profile/'+user)
        else:
            new_follower=models.FollowerCount.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect('profile/'+user)
        

def ebooks(request):
    return render(request,'ebooks.html')


def bookmarks(request):

    user_following=models.FollowerCount.objects.filter(follower=request.user.username)
    all_user=User.objects.all()
    user_following_all=[]
    for user in user_following:
        user_list=User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestion = [x for x in (all_user) if (x not in (user_following_all))]
    print(new_suggestion)
    current_user=User.objects.filter(username=request.user.username)
    final_list=[x for x in (new_suggestion) if (x not in (current_user))]
    random.shuffle(final_list)
    print(final_list)
    username_profile=[]
    username_profile_list=[]
    for users in final_list:
        username_profile.append(users.id)
    for ids in username_profile:
        profile_lists=models.Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)
        
    suggestions_username_profile_list = list(chain(*username_profile_list))
    if request.method=="POST":
        post_user=request.POST['post_user']
        curr_user=request.user.username
        curr_post_id=request.POST['post_id']
        save_post=models.Post.objects.get(id=curr_post_id)
        # caption=save_post.caption
        # image=save_post.image
        # likes=save_post.likes
        
        if models.SavePost.objects.filter(curr_user=curr_user,post=save_post).first():
            delete_save_post=models.SavePost.objects.get(curr_user=curr_user,post=save_post)
            delete_save_post.delete()
            return redirect('bookmarks')
        else:
            save_post_new=models.SavePost.objects.create(curr_user=curr_user,post_user=post_user,post=save_post)
            save_post_new.save()
            return redirect('bookmarks')
    save_pos=models.SavePost.objects.filter(curr_user=request.user.username)

    return render(request,'bookmarks.html',{'suggestions':suggestions_username_profile_list,'save_post':save_pos})


def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = models.Profile.objects.get(user=user_object)
    posts=models.Post.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = models.Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list,'posts':posts})


def communityProfile(request, pk):
    try:
        user=pk
        user_obj = models.CommunityUser.objects.get(username=user)
        user_prof = models.CommunityProfile.objects.get(user=user_obj)
        posts = models.CommunityPost.objects.filter(community_user=user)
        follower=request.user.username
        if models.CommunityFollow.objects.filter(follower=follower,user=user).exists():
            can_post=True
            button='Leave'
        else:
            button='Join'
            can_post=False

        user_followers=len(models.CommunityFollow.objects.filter(user=user))
        prof=models.Profile.objects.get(user=request.user)
        # user_following=len(models.CommunityFollow.objects.filter(follower=pk))
        if request.method=="POST":
            image=request.FILES.get('image')
            caption=request.POST['caption']
            new_post=models.CommunityPost.objects.create(community_user=user,image=image,caption=caption,curr_user=prof)
            new_post.save()
            
        context = {
            'profile_details': user_prof,
            'posts': posts,
            'user_followers':user_followers,
            'button':button,
            'can_post':can_post,
            'prof':prof
        }

        return render(request, 'communityProfile.html', context)
    
    except models.CommunityUser.DoesNotExist:
        return redirect('community')

    except models.CommunityProfile.DoesNotExist:
        return redirect('community')


def community_like(request):
    username=request.user.username
    post_id=request.GET.get('post_id')
    post=models.CommunityPost.objects.get(id=post_id)
    curr_user=post.community_user
    like=models.CommunityLike.objects.filter(community_post_id=post_id,username=username).first()

    if like==None:
        new_like=models.CommunityLike.objects.create(community_post_id=post_id,username=username)
        new_like.save()
        post.likes=post.likes+1
        post.save()
        return redirect('communityProfile/'+curr_user)
    else:
        like.delete()
        post.likes=post.likes-1
        post.save()
        return redirect('communityProfile/'+curr_user)
    
    
def community_join(request):
    if request.method=="POST":
        follower=request.POST['follower']
        user=request.POST['user']
        if models.CommunityFollow.objects.filter(follower=follower,user=user).first():
            delete_follower=models.CommunityFollow.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect('communityProfile/'+user)
        else:
            new_follower=models.CommunityFollow.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect('communityProfile/'+user)


def save(request):
    if request.method=="POST":
        post_user=request.POST['post_user']
        curr_user=request.user.username
        curr_post_id=request.GET.get('post_id')
        save_post=models.Post.objects.get(id=curr_post_id)
        # caption=save_post.caption
        # image=save_post.image
        # likes=save_post.likes
        
        if models.SavePost.objects.filter(curr_user=curr_user,post=save_post).first():
            delete_save_post=models.SavePost.objects.get(curr_user=curr_user,post=save_post)
            delete_save_post.delete()
            return redirect('home')
        else:
            save_post_new=models.SavePost.objects.create(curr_user=curr_user,post_user=post_user,post=save_post)
            save_post_new.save()
            return redirect('home')

def deletepost(request):

    if request.method=="POST":
        post_id=request.GET.get('post_id')
        post_user=request.POST['post_user']
        print("yrs")
        delete_post=models.Post.objects.get(id=post_id,user=post_user)
        delete_post.delete()
        return redirect('profile/'+ post_user)
    
def mail(request): 
    if request.method=="POST":
        emails=request.POST.get('user-email')
        subject = 'Veda Soul'
        message = 'Welcome to Veda Soul'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [emails]
        print(recipient_list)
        send_mail(subject, message, from_email, recipient_list,fail_silently=False)
        return redirect('home')
    
# def forgotemail(request):
#     if request.method=="POST":
#         emails=request.POST.get('user-email')
#         subject = 'Veda Soul'
#         text='''you are receiving this email because you requested a password reset for your user account at 127.0.0.1:8000. Please go to the following page and choose a new password:
#         Your username, in case you have forgotten:
#         Thanks for using our site!
#         The 127.0.0.1:8000 team'''
#         message = text
#         from_email = settings.EMAIL_HOST_USER
#         recipient_list = [emails]
#         print(recipient_list)
#         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#         return redirect('password_reset_done')
    
# def PasswordReset(request):
#     return render(request,'password_reset_form.html')
    
def streamlit_view(request):
    # Run Streamlit app as a subprocess
    subprocess.run(["streamlit", "run", "base/streamlit_app/chatbot_app.py"])

    # You can customize this response or redirect to another page after Streamlit is run.
    return HttpResponse("Streamlit chatbot has been executed.")