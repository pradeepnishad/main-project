from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(blank =True, max_length = 30)
    bio = models.TextField(blank=True, max_length = 100)
    dob = models.DateField(blank=True, null=True)
    coverImg = models.FileField(upload_to='cover/', default='cover.png',null=True , blank=True)
    profileImg = models.FileField(upload_to='profileImg/', default='profile.jpeg')

    # Add more fields as needed

    def __str__(self):
        return f'{self.user.username} profile'