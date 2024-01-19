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
    path('communityProfile/<str:pk>',views.communityProfile,name='communityProfile'),
    path('ebooks',views.ebooks,name='ebooks'),
    path('update',views.update,name='update'),
    path('like',views.Like,name='like'),
    path('follow',views.follow,name='follow'),
    path('search',views.search,name='search'),
    path('bookmarks',views.bookmarks,name='bookmarks'),
    path('deletepost',views.deletepost,name='deletepost'),
    path('community_like',views.community_like,name='community_like'),
    path('community_join',views.community_join,name='community_join'),
    path('save',views.save,name='save'),
    path('password_reset', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    # path('forgotemail',views.forgotemail,name='forgotemail'),
    path('send_mail',views.mail,name='send_mail'),
    path('streamlit/',views.streamlit_view, name='streamlit_view')

]