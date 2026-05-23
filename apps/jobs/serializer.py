from rest_framework import serializers
from .models import Jobs,Application
from django.contrib.auth.models import User
from apps.users.models import Skill
from apps.users.serializer import skillserializer
class userminierializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class Jobsserializer(serializers.ModelSerializer):
    skill_required = skillserializer(many=True,read_only =True)
    recruiter = userminierializer(read_only=True) 
    class Meta:
        model = Jobs
        fields = '__all__'

class Applicationserializer(serializers.ModelSerializer):
    job = Jobsserializer(read_only=True)
    applicant = userminierializer(read_only=True)
    job_id = serializers.PrimaryKeyRelatedField(
        source='job',
        write_only=True,
        queryset=Jobs.objects.all()
    )
    
    class Meta:
        model = Application
        fields = '__all__'