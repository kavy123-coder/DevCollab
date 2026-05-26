from .models import Skill,Userprofile
from rest_framework import serializers
from django.contrib.auth.models import User
class userminierializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        ref_name = 'UserMiniUsers'

class skillserializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class userprofileserializer(serializers.ModelSerializer):
    skills = skillserializer(many=True,read_only =True)
    user = userminierializer(read_only =True)
    Skills = serializers.PrimaryKeyRelatedField(
        many=True,
        source='skills',
        write_only=True,
        queryset=Skill.objects.all()
    )

    class Meta:
        model = Userprofile
        fields = '__all__'



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user