from django.db import models
from django.contrib.auth.models import User
from apps.users.models import Skill
# Create your models here.
class Jobs(models.Model):
    recruiter =  models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=100)
    skill_required = models.ManyToManyField(Skill)
    location = models.CharField()
    is_remote = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    job =  models.ForeignKey(Jobs,on_delete=models.CASCADE)
    applicant = models.ForeignKey(User,on_delete=models.CASCADE)
    cover_letter = models.TextField(max_length=200,blank=True)
    resume = models.FileField(upload_to='resumes/',blank=True)
    status =  models.CharField(choices=[('Pending','Pending'),('Accepted','Accepted'),('Rejected','Rejected')],default='Pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
     return self.job.title

