from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,ListAPIView
from .serializer import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,CreateAPIView
from django.shortcuts import get_object_or_404
from rest_framework import status

# Create your views here.
class Profile_Post_View(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(user=user)
        return queryset
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)        

class Newsfeed_View(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user

        following_user = Follow.objects.filter(
            followers = user
        ).values_list('following',flat=True)

        queryset = Post.objects.filter(user__in = list(following_user)+[user.id]).order_by('-created_at')
        return queryset
    
class Create_Post(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 
    
class UpdateDeletePost(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user = self.request.user)

class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,post_id):
        like,create = Like.objects.get_or_create(user=request.user,post_id=post_id)
        if not create:
            like.delete()
            return Response({'details':'Unliked'})
        return Response({'message':'Liked'},status=status.HTTP_201_CREATED)
    
class CommentView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        post = get_object_or_404(Post,id=post_id)
        queryset = Comment.objects.filter(post=post)
        return queryset

    def perform_create(self, serializer):
        post_id = self.request.data.get('post_id')
        post = get_object_or_404(Post,id=post_id)

        serializer.save(
            user = self.request.user,
            post = post
        )


class Reply_View(ListCreateAPIView):
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        comment_id = self.request.query_params.get('comment_id')
        comment = get_object_or_404(Comment,id=comment_id)
        queryset = Reply.objects.filter(comment=comment)
        return queryset

    def perform_create(self, serializer):
        comment_id = self.request.data.get('comment_id')
        comment = get_object_or_404(Comment,id=comment_id)

        serializer.save(
            user = self.request.user,
            comment = comment
        )
    
