from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import models
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
    return render(request,'home.html',{'posts':posts,'user_profile':user_profile})

def profile(request,pk):
    user=pk
    user_obj=User.objects.get(username=pk)
    user_prof=models.Profile.objects.get(user=user_obj)
    posts=models.Post.objects.filter(user_profile=user_prof)
    
    context={
        'user_obj':user_obj,
        'user_prof':user_prof,
        'posts':posts
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
        
