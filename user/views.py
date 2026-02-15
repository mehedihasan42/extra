from django.shortcuts import render
from .serializer import *
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView,ListAPIView,RetrieveUpdateAPIView,CreateAPIView,RetrieveAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Subquery
from django.db.models import Q
from django.shortcuts import get_object_or_404

# Create your views here.
class SignUpView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [] 

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Signup successful',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [] 

    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'details':'email and password is required'})
        
        try:
            user_obj = Users.objects.get(email=email)
        except Users.DoesNotExist: 
            return Response({'details':'Invalid email or password'})  
        
        user = authenticate(username=user_obj.username,password=password)


        if not user:
            return Response({'details':'User not found'})

        refresh = RefreshToken.for_user(user)

        return Response({'message':'Signup successfull',
                             'access':str(refresh.access_token),
                             'refresh':str(refresh),
                             "user": {
                             "id": user.id,
                             "username": user.username,
                             "email": user.email,
                             }
                             },status=status.HTTP_201_CREATED)
    
class FollowerList(ListAPIView):    
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Users.objects.filter(following__following=self.request.user)
    
class FollowingList(ListAPIView):    
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Users.objects.filter(follower__follower=self.request.user)  
    
class SuggestFollowView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        current_user = self.request.user

        followed_users = Follow.objects.filter(
            follower=current_user
        ).values_list('following_id', flat=True)

        queryset = Users.objects.exclude(
            Q(id__in=list(followed_users) + [current_user.id]) |
            Q(is_superuser=True)
        ).order_by('-id')[:6]   

        return queryset     
    
class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self,request,id):
        user_to_follow = Users.objects.get(id=id)
        follower = request.user

        if follower == user_to_follow:
            return Response({'error':'You can"t follow your self'},status=status.HTTP_400_BAD_REQUEST)
        
        Follow.objects.get_or_create(follower=follower,following=user_to_follow)
        return Response({'message':'Followed successfull'})

class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self,request,id):
        Follow.objects.filter(follower=request.user,following__id=id).delete()
        return Response({'details':'Unfollowed Successfull'})     
   
    
# class ProfileView():  

class SearchUserView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        search = self.request.query_params.get('search')
        following_ids = Follow.objects.filter(follower=self.request.user).values_list('following_id', flat=True)
        queryset = Users.objects.exclude(
            Q(id__in=Subquery(following_ids)) | 
            Q(id=self.request.user.id) |
            Q(is_superuser=True)
        )

        if search:
            queryset = queryset.filter(
                Q(username__icontains = search)   
            ).exclude(id=self.request.user.id)

        return queryset  


class UserProfile(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        profile,create = Profile.objects.get_or_create(user=self.request.user)  
        return profile
    

class PublicUserProfileView(RetrieveAPIView):
    serializer_class = PublicProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        user_id = self.kwargs.get("id")
        return get_object_or_404(Profile, user__id=user_id)    