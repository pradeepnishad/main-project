
from django.urls import path
from . import views
urlpatterns = [
  
   path('',views.user_login, name='login'),
   path('signup/',views.signup, name='signup'),
   # path('home/',views.home,name="home"),
   path('feed/',views.feed,name="feed"),
   path('profileview/',views.profileview,name='profileview'),
   path('message/',views.message, name='message'), 
   path('notification/', views.notification, name='notification'),
   path('search/',views.search,name="search"),
   path('discover/', views.discover,name='discover'),
   path('settings/',views.settings,name='settings'),
   path('logout/', views.logout_view, name='logout'),
   path('profileview/editprofile/', views.editprofile, name='editprofile'),
]