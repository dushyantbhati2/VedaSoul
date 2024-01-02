from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
# Create your models here.
User=get_user_model()


class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,blank=True)
    id_user=models.IntegerField()
    location=models.CharField(max_length=200,blank=True)
    bio=models.TextField(blank=True)
    profimag=models.ImageField(upload_to="prof_images",default="avatar.png")
    
    def __str__(self):
        return self.user.username


class Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    user_profile=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    user=models.CharField(max_length=100,blank=True)
    image=models.ImageField(upload_to="posts",blank=True)
    caption=models.CharField(max_length=100)
    location=models.CharField(max_length=200)
    upload_time=models.DateTimeField(default=datetime.now)
    likes=models.IntegerField(default=0)
    def __str__(self):
        return self.user
    
class LikePost(models.Model):
    post_id=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    
    def __str__(self):
        return self.username
    
class FollowerCount(models.Model):
    follower=models.CharField(max_length=100)
    user=models.CharField(max_length=100)
    
    def __str__(self):
        return self.user