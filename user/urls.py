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
    path('follow/<int:id>/', FollowUserView.as_view(),name='follow'),
    path('unfollow/<int:id>/', UnfollowUserView.as_view(),name='unfollow'),
    path('searchUser/', SearchUserView.as_view(),name='searchUser'),
    path('profile/', UserProfile.as_view(),name='profile'),
    path('suggest-follow/', SuggestFollowView.as_view(),name='profile'),
    path('followers/', FollowerList.as_view(),name='followers'),
    path('following/', FollowingList.as_view(),name='following'),
    path('public_profile/<int:id>/', PublicUserProfileView.as_view(),name='public_profile'),
]
