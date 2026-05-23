from django.contrib import admin
from .models import Skill, Userprofile
# Register your models here.
admin.site.register(Userprofile)
admin.site.register(Skill)