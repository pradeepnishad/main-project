from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(blank =True, max_length = 30)
    phoneno = models.CharField(blank=True, max_length=10)
    bio = models.TextField(blank=True, max_length = 100)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(blank=True, null=True, max_length=10)
    coverImg = models.FileField(upload_to='cover/', default='cover.png',null=True , blank=True)
    profileImg = models.FileField(upload_to='profileImg/', default='profile.jpeg',null=True, blank=True)

    # Add more fields as needed

    def __str__(self):
        return f'{self.user.username} profile'
    

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload = models.FileField(upload_to='post/')
    title = models.CharField(max_length=20, null=True, blank=True)
    caption = models.CharField(max_length=1000,null=True,blank=True )
    created_at = models.DateTimeField(default= datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Post.'
    


class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Follow(models.Model):
  follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
  following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

  class Meta:
    unique_together = ('follower', 'following_user',)


class Comment(models.Model):
    comment_text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200, blank=True)  # For anonymous comments
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_text[:20]  # Truncate comment for display
