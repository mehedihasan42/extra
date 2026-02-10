from rest_framework import serializers
from user.models import *
from .models import *

class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    total_likes = serializers.IntegerField(source='likes.count', read_only=True)
    total_comments = serializers.IntegerField(source='comments.count', read_only=True)
    class Meta:
        model = Post
        fields = ['id','caption','photo','user','total_likes','total_comments']
        read_only_fields = ['id','user']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ['user']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'   
        read_only_fields = ['user']   

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'

class SaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Save
        fields = '__all__'
        