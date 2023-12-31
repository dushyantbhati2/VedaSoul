from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
                return redirect('home')
    return render(request,'register.html')


@login_required(login_url='login')
def home(request):
    return render(request,'home.html')