from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('profile/',Profile_Post_View.as_view(),name='profile'),
    path('newsfeed/',Newsfeed_View.as_view(),name='newsfeed'),
    path('likes/',LikePostView.as_view(),name='likes'),
    path('comments/',CommentView.as_view(),name='comments'),
    path('reply/',Reply_View.as_view(),name='reply'),
]
