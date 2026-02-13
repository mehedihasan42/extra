from django.contrib import admin
from django.urls import path,include
from .views import *
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'signup', SignUpView)
# router.register(r'login', LoginView)

urlpatterns = [
    path('signup/', SignUpView.as_view(),name='signup'),
    path('login/', LoginView.as_view(),name='login'),
    path('follow/', FollowUserView.as_view(),name='follow'),
    path('unfollow/', UnfollowUserView.as_view(),name='unfollow'),
    path('searchUser/', SearchUserView.as_view(),name='searchUser'),
    path('profile/', UserProfile.as_view(),name='profile'),
]
