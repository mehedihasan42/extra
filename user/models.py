from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Users(AbstractUser):
    phone = models.CharField(max_length=12)
    present_address = models.CharField(max_length=150)
    hometown = models.CharField(max_length=150)

    def __str__(self):
        return self.username
        
class Profile(models.Model):
    profile = models.URLField()
    bio = models.CharField(max_length=150)    
    user = models.OneToOneField(Users,on_delete=models.CASCADE)    
   
class Follow(models.Model):
    follower = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='following')
    following = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='follower')
    created_at = models.DateTimeField(auto_now_add=True)   

    class Meta:
        unique_together = ['follower','following']
        
    def __str__(self):
        return f"{self.follower} follows {self.following}"    
    