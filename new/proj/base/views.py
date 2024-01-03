from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import models
from itertools import chain
import random
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
        # name=request.POST['name']
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
                new_prof=models.Profile.objects.create(user=user_model,id_user=user_model.id)
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
    user_following=len(models.FollowerCount.objects.filter(follower=pk))
    length=len(posts)

    context={
        'user_obj':user_obj,
        'user_prof':user_prof,
        'posts':posts,
        'button':button,
        'user_following':user_following,
        'user_followers':user_followers,
        'length':length
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
    return render(request,'community.html')



def communityProfile(request):
    return render(request,'communityProfile.html')


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
