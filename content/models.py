from django.db import models
from user.models import *

# Create your models here.
class Post(models.Model):
    caption = models.CharField(max_length=250)
    photo = models.URLField()
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    text = models.CharField(max_length=500)
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')   
    created_at = models.DateTimeField(auto_now_add=True) 

class Reply(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)

class Like(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')    

    class Meta:
       unique_together = ('user', 'post')

class Save(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
