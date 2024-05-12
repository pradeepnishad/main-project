
from django.urls import path
from . import views

from django.contrib.auth import views as auth_views
urlpatterns = [
  
   path('',views.user_login, name='login'),
   path('signup/',views.signup, name='signup'),
   # path('home/',views.home,name="home"),
   path('feed/',views.feed,name="feed"),
   path('profileview/',views.profileview,name='profileview'),
   path('profile/<username>',views.profile,name='profile'),
   path('message/',views.message, name='message'), 
   path('notification/', views.notification, name='notification'),
   path('search/',views.search,name="search"),
   path('discover/', views.discover,name='discover'),
   path('settings/',views.settings,name='settings'),
   path('logout/', views.logout_view, name='logout'),
   path('profileview/editprofile/', views.editprofile, name='editprofile'),
   path('post', views.post, name='post'),
   path('like/',views.like,name="like"),
   path('follow/<user_id>/', views.follow_user, name='follow_user'),
   path('unfollow/<user_id>/', views.unfollow_user, name='unfollow_user'),
   # path('<int:pk>/detail/', views.post_detail, name='post_detail'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'baseapp/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'baseapp/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'baseapp/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name = 'baseapp/password_reset_complete.html'), name='password_reset_complete'),
]