from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
# from .views import AlbumDetailView

router = DefaultRouter()
router.register(r'postcategory',PostCategoryViewSet)
# manage post
router.register(r'posts', PostViewSet,basename='post')
# manage pending post
router.register(r'postpending',PostPendingViewSet,basename='postpending')
# manage post comments
router.register(r'postcomments', PostCommentViewSet, basename='postcomment'),
# manage post likes
router.register(r'post-likes', PostLikeViewSet)


urlpatterns = [

path('',include(router.urls)),
# manage post
path('create_post/', CreatePost.as_view(), name='create_post'),
path('update_post/<int:post_id>/', UpdatePost.as_view(), name='update_post'),
path('post_detail/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
# path('user_posts/<int:user_id>/', UserPostsView.as_view(), name='user_posts'),


# delete post comment
path('delete_post_comment/<int:comment_id>/', PostCommentDelete.as_view(), name='delete_post_comment'),

# # manage birthday wishes
path('upcoming_birthdays/', UpcomingBirthdayListAPIView.as_view(), name='upcoming_birthdays'),
path('all_upcoming_birthdays/', UpcomingBirthdayAll.as_view(), name='all_upcoming_birthdays'),
path('send_birthday_wishes/<int:member_id>/', SendBirthdayWishes.as_view(), name='send_birthday_wishes'),

# filter post
path('filter_posts/', PostFilterView.as_view(), name='filter_posts'),

# manage albums
path("createalbum/", AlbumView.as_view(), name="createalbum"),
path("uploadalbum/<int:album_id>/", AlbumView.as_view(), name="uploadalbum"),
path('albums/', AlbumView.as_view(), name='album_list'),  
path('photos/<int:album_id>/', AlbumPhotosView.as_view(), name='photos'),
path('albums/<int:album_id>/', AlbumView.as_view(), name='album_detail'),
path('updatealbum/<int:album_id>/', AlbumView.as_view(), name='update_album'),
path('delete/photos/<int:photo_id>/', AlbumView.as_view(), name='delete_photo'),
path('delete/albums/<int:album_id>/', AlbumView.as_view(), name='delete_album'),
path('album/approved/<int:album_id>/', AlbumDetailView.as_view(), name='approved_album_detail'),
path('approvedalbums/', AlbumDetailView.as_view(), name='approved_albums'),
path('album/photos/<int:photo_id>/approve/', AlbumDetailView.as_view(), name='approve_album_photo'),
path('albums/unapprovedphotos/', AlbumsWithUnapprovedPhotosView.as_view(), name='albums_unapproved_photos'),
path('sorting_albums/', SortingAlbums.as_view(), name='sorting_albums'),

# manage memories
path('creatememories/', MemoryView.as_view(), name='create_memories'),
path('memories/<int:memory_id>/', MemoryView.as_view(), name='detail_memories'),
path('updatememories/<int:memory_id>/', MemoryView.as_view(), name='update_memories'),
path('memories/', MemoryView.as_view(), name='retrieve_memories'),
path('memories/approved/', ApprovedMemoriesView.as_view(), name='approved-memories'),
path('memories/pending/', PendingMemoriesView.as_view(), name='pending-memories'),
path('memories/approving/<int:memory_id>/', ApproveMemory.as_view(), name='approve_process'),
path('memories/deletephotos/<int:photo_id>/', MemoryView.as_view(), name='delete_memory_photo'),
path('memories/deletetags/<int:tag_id>/', MemoryView.as_view(), name='delete_memory_tag'),
path('deletememories/<int:memory_id>/', MemoryView.as_view(), name='delete_memory'),
path('sorting_memories/', SortingMemories.as_view(), name='sorting_memories'),
]