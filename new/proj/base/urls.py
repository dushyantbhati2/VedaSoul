from django.contrib import admin
from django.conf import settings
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 


urlpatterns = [
   
    path('',views.index,name='index'),
    path('login',views.log_in,name='login'),
    path('register',views.register,name='register'),
    path('home',views.home,name='home'),
    path('post',views.post,name='post'),
    path('logout',views.logout,name='logout'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('community',views.community,name='community'),
    path('communityProfile',views.communityProfile,name='communityProfile'),
    path('update',views.update,name='update'),
    path('password_reset', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]