from django.db import models
from django.contrib.auth.models import User
from apps.users.models import Skill
# Create your models here.
class Tag(models.Model):
    name = models.CharField(unique=True)

    def __str__(self):
        return self.name
class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='posts')
    likes  = models.ManyToManyField(User, related_name='liked_posts')
    title = models.CharField()
    content = models.TextField() 
    tags = models.ManyToManyField(Tag,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') 
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')  
    likes = models.ManyToManyField(User, related_name='liked_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)