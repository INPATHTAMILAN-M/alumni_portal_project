from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'postcategory',PostCategoryViewSet)
router.register(r'posts', PostViewSet,basename='post')
router.register(r'postpending',PostPendingViewSet,basename='postpending')
router.register(r'postcomments', PostCommentViewSet, basename='postcomment'),
router.register(r'post-likes', PostLikeViewSet)


urlpatterns = [

path('',include(router.urls)),
path('create_post/', CreatePost.as_view(), name='create_post'),  # For creating a new post
path('update_post/<int:post_id>/', UpdatePost.as_view(), name='update_post'),

]