from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets,status

from account.models import ActivityPoints, UserActivity
from .models import PostCategory
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import date
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

class PostCategoryViewSet(viewsets.ModelViewSet):
    queryset = PostCategory.objects.all()
    serializer_class = PostCategorySerializer

    #permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        return Response({"message": "Delete operation is not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create_post_category(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            "message": "Category created successfully.",
        }
        return response

    def update_post_category(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {
            "message": "Category updated successfully.",
        }
        return response
    

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    parser_classes = (MultiPartParser, FormParser)

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(posted_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

        if self.request.user.groups.filter(name='Administrator').exists() or self.request.user.groups.filter(name='Alumni_Manager').exists():

            serializer.save(posted_by=self.request.user, published=True)
        else:
            serializer.save(posted_by=self.request.user, published=False)

# create post
        
class CreatePost(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request):

        post_category_id = request.data.get('post_category')
        published = request.data.get('published', False)
        
        post_category = get_object_or_404(PostCategory, id=post_category_id)
        
        if request.user.groups.filter(name='Administrator').exists() or request.user.groups.filter(name='Alumni_Manager').exists():
            published = True  

        post = Post.objects.create(
            title=request.data.get('title'),
            blog=request.data.get('blog'),
            post_category=post_category,
            content=request.data.get('content'),
            published=published,
            visible_to_public=request.data.get('visible_to_public'),
            featured_image = request.data.get('featured_image'), 
            posted_by=request.user,
        )
        try:
            activity = ActivityPoints.objects.get(name="Business Directory")
        except ActivityPoints.DoesNotExist:
            return Response("Activity not found.")
        UserActivity.objects.create(
            user=request.user,
            activity=activity,
            details=f"{post.title} Posted"
        )
        return Response({
            "message": "Post created successfully",
        }, status=status.HTTP_201_CREATED)

# update post
        
class UpdatePost(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request,post_id):
        
        if not post_id:
            return Response({"message": "Post ID is required to update."}, status=status.HTTP_400_BAD_REQUEST)
        
        post = get_object_or_404(Post, id=post_id)
        
        if post.posted_by != request.user:
            return Response({"message": "You are not authorized to update this post."}, status=status.HTTP_403_FORBIDDEN)
        
        post_category_id = request.data.get('post_category', post.post_category.id)
        post_category = get_object_or_404(PostCategory, id=post_category_id)
        
        post.title = request.data.get('title', post.title)  
        post.blog = request.data.get('blog', post.blog)
        post.post_category_id = post_category
        post.content = request.data.get('content', post.content)
        post.published = request.data.get('published', post.published)  
        post.visible_to_public = request.data.get('visible_to_public', post.visible_to_public)
        post.featured_image = request.data.get('featured_image',post.featured_image)
        post.save()

        return Response({
            "message": "Post updated successfully"
        }, status=status.HTTP_200_OK)
 
 #  get single post
class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# manage pending posts
class PostPendingViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    parser_classes = (MultiPartParser, FormParser)

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if self.request.user.groups.filter(name='Administrator').exists() or self.request.user.groups.filter(name='Alumni_Manager').exists():  
            return Post.objects.filter(published=False)
        return Post.objects.filter(published=False, posted_by=user)

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def published_posts(self, request):
        
        published_posts = Post.objects.filter(published=True).order_by('-id')
        serializer = self.get_serializer(published_posts, many=True)
        return Response(serializer.data)

    @action(detail = False, methods = ['put'],url_path = '(?P<post_id>\d+)')
    def publish_post(self, request,post_id, *args, **kwargs):
        
        user = request.user
        if not self.request.user.groups.filter(name='Administrator').exists() or not self.request.user.groups.filter(name='Alumni_Manager').exists():
            return Response(
                {"message": "Only admins can update posts."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"message": "Post not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        post.published = True
        post.save()
        return Response(
            {"message": "published successfully"},
            status=status.HTTP_200_OK
        )
        
# manage post Comments
class PostCommentViewSet(viewsets.ModelViewSet):
    queryset = PostComment.objects.all()
    serializer_class = PostComment_Serializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(comment_by=self.request.user)

    @action(detail = False, methods = ['post'],url_path = '(?P<post_id>\d+)')
    def create_postcomments(self, request, post_id):

        try:
            post = Post.objects.get(id=post_id) 
        except Post.DoesNotExist:
            return Response({"message": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data["post"] = post.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(comment_by=request.user)
        return Response({"message": "Comments posted"}, status=status.HTTP_201_CREATED)

class PostCommentDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):
        try:
            comment = PostComment.objects.get(id=comment_id)

            if comment.comment_by != request.user and not (
                request.user.groups.filter(name__in=['Administrator', 'Alumni_Manager']).exists()
            ):
                return Response(
                    {"message": "You do not have permission to delete this comment."},
                    status=status.HTTP_403_FORBIDDEN
                )

            comment.delete()
            return Response(
                {"message": "Comment deleted successfully."},
                status=status.HTTP_200_OK
            )

        except PostComment.DoesNotExist:
            return Response(
                {"message": "Comment not found."},
                status=status.HTTP_404_NOT_FOUND
            )
# manage post likes
class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='(?P<post_id>\d+)')
    def like_post(self, request, post_id):
        user = request.user
        
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"message": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        existing_like = PostLike.objects.filter(post=post, liked_by=user).first()
        
        if existing_like:
            existing_like.delete()
            return Response({"message": "Post disliked"}, status=status.HTTP_200_OK)
        else:
            PostLike.objects.create(post=post, liked_by=user)
            return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)

# manage birthday wishes
# list 10 members
class UpcomingBirthdayListAPIView(APIView):
    def get(self, request):
        # Get the current date
        today = timezone.now().date()

        current_year = today.year

        members = Member.objects.filter(
            dob__month__gte=today.month,
            dob__year=current_year,
            user__isnull=False
        ).order_by('dob')[:10]

        upcoming_birthdays = []
        for member in members:
            if member.dob.day >= today.day or member.dob.month > today.month:
                upcoming_birthdays.append(member)

        serializer = MemberBirthdaySerializer(upcoming_birthdays, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

# list all members
class UpcomingBirthdayAll(APIView):
    def get(self, request):
        today = timezone.now().date()

        current_year = today.year

        members = Member.objects.filter(
            dob__month__gte=today.month,
            dob__year=current_year,
            user__isnull=False
        ).order_by('dob')

        upcoming_birthdays = []
        for member in members:
            if member.dob.day >= today.day or member.dob.month > today.month:
                upcoming_birthdays.append(member)

        serializer = MemberBirthdaySerializer(upcoming_birthdays, many=True,  context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

# send wishes via email
class SendBirthdayWishes(APIView):
    def post(self, request, member_id):
        try:
            member = Member.objects.get(id=member_id)
            
            if member.dob and member.dob.month == date.today().month and member.dob.day == date.today().day:
                
                subject = 'Happy Birthday!'
                message = f"Dear {member.salutation} {member.user.first_name} {member.user.last_name},\n\nWe wish you a very Happy Birthday! 🎉\n\nBest regards,\n {request.user.email}"
                from_email = settings.EMAIL_HOST_USER
                to_email = [member.email]
                
                send_mail(subject, message, from_email, to_email)
                
                return Response({"message": "Birthday wishes sent successfully!"}, status=200)
            else:
                return Response({"message": "Today is not the member's birthday."}, status=200)
        
        except Member.DoesNotExist:
            return Response({"error": "Member not found!"}, status=404)
        
# filter posts
 
class PostFilterView(APIView):
    def post(self, request, *args, **kwargs):
        post_category = request.data.get('post_category', None)
        title = request.data.get('title', None)
        published = request.data.get('published', None)  
        
        filters = Q(published=True)  

        if post_category not in [None, ""]:
            filters &= Q(post_category__id=post_category)

        if title not in [None, ""]:
            filters &= Q(title__icontains=title)

        if published is not None:
            filters &= Q(published=published)

        queryset = Post.objects.prefetch_related(
            'post_category'
        ).filter(filters)

        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = PostSerializer(paginated_queryset, many=True, context={'request': request})

        return paginator.get_paginated_response(serializer.data)
    
    
# manage albums
class AlbumView(APIView):

    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    

    def post(self, request):
        data = request.data
        album_name = data.get('album_name')
        description = data.get('description')
        album_location = data.get('album_location')
        album_date = data.get('album_date')
        public_view = data.get('public_view', True)

        if not album_name or not album_date:
            return Response(
                {"message": "album_name and album_date are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        album = Album.objects.create(
            album_name=album_name,
            description=description,
            album_location=album_location,
            album_date=album_date,
            public_view=public_view,
            created_by=request.user,
        )
        try:
            activity = ActivityPoints.objects.get(name="Business Directory")
        except ActivityPoints.DoesNotExist:
            return Response("Activity not found.")
        UserActivity.objects.create(
            user=request.user,
            activity=activity,
            details=f"{album.album_name} Posted"
        )
        return Response(
            {"id": album.id, "message": "Album created successfully."},
            status=status.HTTP_201_CREATED,
        )


    


    def put(self, request, album_id):
        try:
            album = Album.objects.get(id=album_id, created_by=request.user)
        except Album.DoesNotExist:
            return Response(
                {"message": "Album not found or you do not have permission to add photos."},
                status=status.HTTP_404_NOT_FOUND,
            )

        files = request.FILES.getlist('photos')

        if not files:
            return Response(
                {"message": "No files were provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        photo_objects = []
        for file in files:
            photo = AlbumPhotos(album=album, photo=file)
            photo_objects.append(photo)
        AlbumPhotos.objects.bulk_create(photo_objects)

        return Response(
            {"message": "Files uploaded successfully."},
            status=status.HTTP_201_CREATED,
        )
    

    def get(self, request, album_id=None):
        if album_id:
            try:
                album = Album.objects.get(id=album_id)
                serialized_album = AlbumSerializer(album, context={'request': request}).data
                serialized_album['created_on'] = album.created_on
                serialized_album['created_by'] = album.created_by.username 
                return Response(serialized_album, status=status.HTTP_200_OK)
            except Album.DoesNotExist:
                return Response({"message": "Album not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            albums = Album.objects.all()
            serialized_albums = AlbumSerializer(albums, many=True, context={'request': request}).data
            for album in serialized_albums:
                album_instance = Album.objects.get(id=album['id'])
                album['created_on'] = album_instance.created_on
                album['created_by'] = album_instance.created_by.username
            return Response(serialized_albums, status=status.HTTP_200_OK)
        

    def patch(self, request, album_id):
        try:
            album = Album.objects.get(id=album_id)
            
            serializer = AlbumSerializer(album, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                if 'photos' in request.FILES:
                    photos = request.FILES.getlist('photos') 
                    for photo in photos:
                        AlbumPhotos.objects.create(album=album, photo=photo)

                return Response(
                    {
                        "message": "Album updated successfully."
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Album.DoesNotExist:
            return Response({"message": "Album not found."}, status=status.HTTP_404_NOT_FOUND)


        
    def delete(self, request, photo_id):
        try:
            photo = AlbumPhotos.objects.get(id=photo_id)

            is_creator = photo.album.created_by == request.user
            is_alumni_manager = request.user.groups.filter(name='Alumni_Manager').exists()
            is_adminstrator = request.user.groups.filter(name='Administrator').exists()

            if is_creator or is_alumni_manager or is_adminstrator:
                photo.delete()
                return Response({"message": "Photo deleted successfully."}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "You do not have permission to delete this photo."},
                    status=status.HTTP_403_FORBIDDEN
                )
        except AlbumPhotos.DoesNotExist:
            return Response({"message": "Photo not found."}, status=status.HTTP_404_NOT_FOUND)
        
    
    def delete(self, request, album_id):
        try:
            album = Album.objects.get(id=album_id)

            is_creator = album.created_by == request.user
            is_alumni_manager = request.user.groups.filter(name='Alumni_Manager').exists()
            is_adminstrator = request.user.groups.filter(name='Administrator').exists()

            if is_creator or is_alumni_manager or is_adminstrator:
                album.delete()
                return Response({"message": "Album deleted successfully."}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "You do not have permission to delete this album."},
                    status=status.HTTP_403_FORBIDDEN
                )
        except Album.DoesNotExist:
            return Response({"message": "Album not found."}, status=status.HTTP_404_NOT_FOUND)
        
class AlbumDetailView(APIView):

    def get(self, request, album_id):
        album = get_object_or_404(Album, id=album_id)

        album_data = AlbumSerializer(album).data

        approved_photos = AlbumPhotos.objects.filter(album=album, approved=True).order_by('-id')
        photo_urls = [request.build_absolute_uri(photo.photo.url) for photo in approved_photos]

        album_data['photos'] = [
            {
                "id": photo.id,
                "photo": request.build_absolute_uri(photo.photo.url),
                "uploaded_on": photo.uploaded_on,
            }
            for photo in approved_photos
        ]

        return Response(album_data, status=status.HTTP_200_OK)
    
    def get(self, request):
        albums = Album.objects.all()
        response_data = []

        for album in albums:
            serialized_album = AlbumSerializer(album).data

            approved_photos = AlbumPhotos.objects.filter(album=album, approved=True).order_by('-id')
            serialized_album['photos'] = [
                {
                    "id": photo.id,
                    "photo": request.build_absolute_uri(photo.photo.url),
                    "uploaded_on": photo.uploaded_on,
                }
                for photo in approved_photos
            ]

            response_data.append(serialized_album)

        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request, photo_id):
        try:
            photo = AlbumPhotos.objects.get(id=photo_id)
        except AlbumPhotos.DoesNotExist:
            return Response({"message": "Photo not found."}, status=status.HTTP_404_NOT_FOUND)

        if (not request.user.groups.filter(name='Alumni_Manager').exists() and not request.user.groups.filter(name='Adminstrator').exists()):
            return Response({"message": "You do not have permission to approve this photo."}, status=status.HTTP_403_FORBIDDEN)

        photo.approved = True
        photo.save()

        return Response({"message": "Photo approved successfully."}, status=status.HTTP_200_OK)
    
class AlbumsWithUnapprovedPhotosView(APIView):
    def get(self, request):
        albums = Album.objects.all()
        response_data = []

        for album in albums:
            serialized_album = AlbumSerializer(album).data
            
            unapproved_photos = AlbumPhotos.objects.filter(album=album, approved=False)
            serialized_photos = [
                {
                    "id": photo.id,
                    "photo": photo.photo.url,  
                    "uploaded_on": photo.uploaded_on,
                    "approved": photo.approved
                }
                for photo in unapproved_photos
            ]
            
            serialized_album["photos"] = serialized_photos
            
            response_data.append(serialized_album)

        return Response(response_data, status=status.HTTP_200_OK)

class MemoryView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        memory_data = {
            'year': request.data.get('year'),
            'month': request.data.get('month'),
            'approved': request.user.groups.filter(name='Alumni_Manager').exists() or request.user.groups.filter(name='Administrator').exists()
        }
        
        try:
            user = User.objects.get(id=request.user.id) 
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        memory_data['created_by'] = user 
        
        memory = Memories.objects.create(**memory_data)

        tags = request.data.getlist('tags')  
        if tags:
            for tag in tags:
                MemoryTags.objects.create(memory=memory, tag=tag)

        photos = request.FILES.getlist('photos') 
        if photos:
            for photo in photos:
                MemoryPhotos.objects.create(memory=memory, photo=photo)
                
        try:
            activity = ActivityPoints.objects.get(name="Business Directory")
        except ActivityPoints.DoesNotExist:
            return Response("Activity not found.")
        UserActivity.objects.create(
            user=request.user,
            activity=activity,
            details=f"Memories created on {memory.created_on}"
        )
        return Response(
            {"message": "Memory created successfully."},
            status=status.HTTP_201_CREATED
        )
    
    def get(self, request, memory_id=None):
        if memory_id:
            try:
                memory = Memories.objects.get(id=memory_id)
                memory_data = MemorySerializer(memory).data
                memory_data['created_by'] = memory.created_by.username
                memory_data['tags'] = [
                    tag.tag for tag in MemoryTags.objects.filter(memory=memory)
                ]
                memory_data['photos'] = [
                    request.build_absolute_uri(photo.photo.url) 
                    for photo in MemoryPhotos.objects.filter(memory=memory)
                ]
                return Response(memory_data, status=status.HTTP_200_OK)
            except Memories.DoesNotExist:
                return Response({"message": "Memory not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            memories = Memories.objects.all()
            all_memories_data = []
            for memory in memories:
                memory_data = MemorySerializer(memory).data
                memory_data['created_by'] = memory.created_by.username
                memory_data['tags'] = [
                    tag.tag for tag in MemoryTags.objects.filter(memory=memory)
                ]
                memory_data['photos'] = [
                    request.build_absolute_uri(photo.photo.url) 
                    for photo in MemoryPhotos.objects.filter(memory=memory)
                ]
                all_memories_data.append(memory_data)
            return Response(all_memories_data, status=status.HTTP_200_OK)
        

    def patch(self, request, memory_id):
        if not (request.user.groups.filter(name__in=['Alumni_Manager', 'Administrator']).exists()):
            return Response(
                {"message": "You do not have permission to approve memories."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            memory = Memories.objects.get(id=memory_id, approved=False)
        except Memories.DoesNotExist:
            return Response(
                {"message": "Memory not found or already approved."},
                status=status.HTTP_404_NOT_FOUND
            )

        memory.approved = True
        memory.save()

        return Response(
            {"message": "Memories approved successfully."},
            status=status.HTTP_200_OK
        )
    
    def delete(self, request, photo_id):
        try:
            photo = MemoryPhotos.objects.get(id=photo_id)
        except MemoryPhotos.DoesNotExist:
            return Response(
                {"message": "Photo not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not (photo.memory.created_by == request.user or request.user.groups.filter(name='Alumni_Manager').exists() or request.user.groups.filter(name='Administrator').exists()):
            return Response( {"message": "You do not have permission to delete this photo."},status=status.HTTP_403_FORBIDDEN)

        photo.delete()
        return Response(
            {"message": "Photo deleted successfully."},
            status=status.HTTP_200_OK
        )
    
    def delete(self, request, tag_id):
        try:
            tag = MemoryTags.objects.get(id=tag_id)
        except MemoryTags.DoesNotExist:
            return Response(
                {"message": "Tag not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not (tag.memory.created_by == request.user or request.user.groups.filter(name='Alumni_Manager').exists() or request.user.groups.filter(name='Administrator').exists()):
            return Response( {"message": "You do not have permission to delete this photo."},status=status.HTTP_403_FORBIDDEN)

        tag.delete()
        return Response(
            {"message": "Tag deleted successfully."},
            status=status.HTTP_200_OK
        )
    
    def delete(self, request, memory_id):
        try:
            memory = Memories.objects.get(id=memory_id)
        except Memories.DoesNotExist:
            return Response(
                {"message": "Memory not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not (memory.created_by == request.user or request.user.groups.filter(name='Alumni_Manager').exists() or request.user.groups.filter(name='Administrator').exists()):
            return Response( {"message": "You do not have permission to delete this photo."},status=status.HTTP_403_FORBIDDEN)

        memory.delete()
        return Response(
            {"message": "Memory deleted successfully."},
            status=status.HTTP_200_OK
        )


class ApprovedMemoriesView(APIView):
    
    def get(self, request):
        approved_memories = Memories.objects.filter(approved=True).order_by('-id')
        serialized_memories = MemorySerializer(approved_memories, many=True)
        return Response(serialized_memories.data, status=status.HTTP_200_OK)

class PendingMemoriesView(APIView):
   
    def get(self, request):
        pending_memories = Memories.objects.filter(approved=False)
        serialized_memories = MemorySerializer(pending_memories, many=True)
        return Response(serialized_memories.data, status=status.HTTP_200_OK)