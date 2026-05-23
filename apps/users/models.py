

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Skill(models.Model):
    name  = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name
class Userprofile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(choices=[('Developer','Developer'),('Recruiter','Recruiter'),('Admin','Admin')])
    bio = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill,blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    avatar = models.ImageField(upload_to='avatars/',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
