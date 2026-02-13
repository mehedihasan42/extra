from rest_framework import serializers
from user.models import *
from .models import *

class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    total_likes = serializers.IntegerField(source='likes.count', read_only=True)
    total_comments = serializers.IntegerField(source='comments.count', read_only=True)
    is_saved = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id','caption','photo','user','total_likes','total_comments','is_saved']
        read_only_fields = ['id','user']
        
    def get_is_saved(self, obj):
        user = self.context['request'].user
        return Save.objects.filter(user=user, post=obj).exists()    

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ['user']

class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'text','user_username', 'created_at']
        read_only_fields = ['id','created_at']   

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'

class SaveSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(),
        source="post",
        write_only=True
    )
    class Meta:
        model = Save
        fields = ['id', 'post', 'post_id']
        