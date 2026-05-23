from rest_framework import serializers
from .models import Tag, Comment, Post
from django.contrib.auth.models import User
class userminierializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class tagserializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class commentserializer(serializers.ModelSerializer):
    author = userminierializer( read_only=True)
    likes = userminierializer(many=True, read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'


class postserializer(serializers.ModelSerializer):
    tags = tagserializer(many=True, read_only=True)
    comments = commentserializer(many=True, read_only=True)
    author = userminierializer( read_only=True)
    likes = userminierializer(many=True, read_only=True)
    tags_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        source='tags',
        write_only=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Post
        fields = '__all__'