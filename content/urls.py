from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('profile/',Profile_Post_View.as_view(),name='profile'),
    path('newsfeed/',Newsfeed_View.as_view(),name='newsfeed'),
    path('likes/<int:post_id>/',LikePostView.as_view(),name='likes'),
    path('comments/',CommentView.as_view(),name='comments'),
    path('comments/<int:id>/', CommentUpdateDelete.as_view(), name='comment-update-delete'),
    path('reply/',Reply_View.as_view(),name='reply'),
    path('create_post/',Create_Post.as_view(),name='reply'),
    path('save/', SaveView.as_view(), name='save-post'),
    path('unsave/<int:post_id>/', UnsaveView.as_view(), name='unsave-post'),
]
