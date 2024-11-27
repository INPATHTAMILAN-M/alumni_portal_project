from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets,status
from .models import PostCategory
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import date
from django.db.models import Q


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
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        # Extract data from request

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
        post.featured_image = request.data.get('featured_image',post.featured_image),
        post.save()

        return Response({
            "message": "Post updated successfully"
        }, status=status.HTTP_200_OK)
 
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
        
        # Admin sees all published posts
        published_posts = Post.objects.filter(published=True)
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
            post = Post.objects.get(id=post_id)  # Get the post object
        except Post.DoesNotExist:
            return Response({"message": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        # Add post and user to the serializer's data
        data = request.data.copy()
        data["post"] = post.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(comment_by=request.user)
        return Response({"message": "Comments posted"}, status=status.HTTP_201_CREATED)

class PostCommentDelete(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def delete(self, request, comment_id):
        try:
            # Get the comment by ID
            comment = PostComment.objects.get(id=comment_id)

            if comment.comment_by != request.user and not (
            request.user.groups.filter(name='Administrator').exists() or 
            request.user.groups.filter(name='Alumni_Manager').exists() ):
                return Response({"message": "You do not have permission to delete this comment."}, status=status.HTTP_403_FORBIDDEN)
        
            # Perform the deletion
            comment.delete()

            return Response({"message": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except PostComment.DoesNotExist:
            # If the comment doesn't exist
            return Response({"message": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
        
# manage post likes
class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='(?P<post_id>\d+)')
    def like_post(self, request, post_id):
        user = request.user
        
        # Ensure that the post exists
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"message": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the user has already liked the post
        existing_like = PostLike.objects.filter(post=post, liked_by=user).first()
        
        if existing_like:
            # If a like exists, remove it (dislike)
            existing_like.delete()
            return Response({"message": "Post disliked"}, status=status.HTTP_200_OK)
        else:
            # If no like exists, create a new like
            PostLike.objects.create(post=post, liked_by=user)
            return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)

# manage birthday wishes
# list 10 members
class UpcomingBirthdayListAPIView(APIView):
    def get(self, request):
        # Get the current date
        today = timezone.now().date()

        # Get the current year to check for upcoming birthdays in the future
        current_year = today.year

        # Query for members with birthdays in the upcoming weeks or months
        members = Member.objects.filter(
            dob__month__gte=today.month,
            dob__year=current_year
        ).order_by('dob')[:10]

        # Filter out members whose birthdays are before today in the current month
        upcoming_birthdays = []
        for member in members:
            # Only include members whose birthday hasn't passed yet
            if member.dob.day >= today.day or member.dob.month > today.month:
                upcoming_birthdays.append(member)

        # Serialize the members data
        serializer = MemberBirthdaySerializer(upcoming_birthdays, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

# list all members
class UpcomingBirthdayAll(APIView):
    def get(self, request):
        # Get the current date
        today = timezone.now().date()

        # Get the current year to check for upcoming birthdays in the future
        current_year = today.year

        # Query for members with birthdays in the upcoming weeks or months
        members = Member.objects.filter(
            dob__month__gte=today.month,
            dob__year=current_year
        ).order_by('dob')

        # Filter out members whose birthdays are before today in the current month
        upcoming_birthdays = []
        for member in members:
            # Only include members whose birthday hasn't passed yet
            if member.dob.day >= today.day or member.dob.month > today.month:
                upcoming_birthdays.append(member)

        # Serialize the members data
        serializer = MemberBirthdaySerializer(upcoming_birthdays, many=True,  context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

# send wishes via email
class SendBirthdayWishes(APIView):
    def post(self, request, member_id):
        try:
            # Fetch member by member_id
            member = Member.objects.get(id=member_id)
            
            # Check if today is the member's birthday
            if member.dob and member.dob.month == date.today().month and member.dob.day == date.today().day:
                
                # Send birthday email
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
        # Extract data from request
        post_category = request.data.get('post_category', None)
        title = request.data.get('title', None)
        published = request.data.get('published', None)  # Optional filter for published status
        
        # Default filter for published posts
        filters = Q(published=True)  # Default to published=True

        # Additional filtering based on user-provided criteria
        if post_category not in [None, ""]:
            filters &= Q(post_category__id=post_category)

        if title not in [None, ""]:
            filters &= Q(title__icontains=title)

        # If 'published' is specified, update the filter to include or exclude published posts
        if published is not None:
            filters &= Q(published=published)

        # Apply the filters to the Post queryset with prefetch_related to optimize DB queries
        queryset = Post.objects.prefetch_related(
            'post_category'
        ).filter(filters)

        # Serialize the filtered data
        serializer = PostSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
# manage albums
class AlbumView(APIView):

    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    

    def post(self, request):
        # Extract data from the request
        data = request.data
        album_name = data.get('album_name')
        description = data.get('description')
        album_location = data.get('album_location')
        album_date = data.get('album_date')
        public_view = data.get('public_view', True)

        # Validate required fields
        if not album_name or not album_date:
            return Response(
                {"detail": "album_name and album_date are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create the album
        album = Album.objects.create(
            album_name=album_name,
            description=description,
            album_location=album_location,
            album_date=album_date,
            public_view=public_view,
            created_by=request.user,
        )

        # Respond with the album ID and a success message
        return Response(
            {"id": album.id, "detail": "Album created successfully."},
            status=status.HTTP_201_CREATED,
        )

    def put(self, request, album_id):
        # Retrieve the album
        try:
            album = Album.objects.get(id=album_id, created_by=request.user)
        except Album.DoesNotExist:
            return Response(
                {"message": "Album not found or you do not have permission to add photos."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Retrieve files from the request
        files = request.FILES.getlist('photos')

        if not files:
            return Response(
                {"message": "No files were provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save each photo to the album
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
            # Retrieve a specific album by ID
            try:
                album = Album.objects.get(id=album_id)
                serialized_album = AlbumSerializer(album, context={'request': request}).data
                serialized_album['created_on'] = album.created_on
                serialized_album['created_by'] = album.created_by.username  # Assuming `User` has a `username` field
                return Response(serialized_album, status=status.HTTP_200_OK)
            except Album.DoesNotExist:
                return Response({"detail": "Album not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Retrieve all albums
            albums = Album.objects.all()
            serialized_albums = AlbumSerializer(albums, many=True, context={'request': request}).data
            for album in serialized_albums:
                album_instance = Album.objects.get(id=album['id'])
                album['created_on'] = album_instance.created_on
                album['created_by'] = album_instance.created_by.username
            return Response(serialized_albums, status=status.HTTP_200_OK)
        

    def patch(self, request, album_id):
        try:
            # Fetch the album instance
            album = Album.objects.get(id=album_id)
            
            # Update album fields
            serializer = AlbumSerializer(album, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                # Check if photos are included in the request
                if 'photos' in request.FILES:
                    photos = request.FILES.getlist('photos')  # Allow multiple photos
                    for photo in photos:
                        AlbumPhotos.objects.create(album=album, photo=photo)

                return Response(
                    {
                        "detail": "Album updated successfully."
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Album.DoesNotExist:
            return Response({"detail": "Album not found."}, status=status.HTTP_404_NOT_FOUND)