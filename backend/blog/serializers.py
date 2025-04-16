from rest_framework import serializers
from .models import Post, Comment
from users.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'content','image','slug','author', 'created_at', 'updated_at']
        read_only_fields = ['author']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']
        read_only_fields = ['author','created_at']