from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets,status
from .models import PostCategory
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
# Create your views here.


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
            serializer.save(posted_by=self.request.user)

    def create_post(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            "message": "Post created successfully.",
        }
        return response

    def update_post(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {
            "message": "Post updated successfully.",
        }
        return response


#admin can able to see the false post
class PostPendingViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    parser_classes = (MultiPartParser, FormParser)

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  
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

    def publish_post(self, request, *args, **kwargs):
        
        user = request.user
        if not user.is_staff:
            return Response(
                {"message": "Only admins can update posts."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            post = self.get_object()
        except Post.DoesNotExist:
            return Response(
                {"message": "Post not found or already published."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        post.published = True
        post.save()
        return Response(
            {"message": "published successfully"},
            status=status.HTTP_200_OK
        )

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

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.comment_by or self.request.user.groups.filter(name='Administrator').exists() or self.request.user.groups.filter(name='Alumni_Manager').exists():
            self.perform_destroy(instance)
            return Response({"message": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "You do not have permission to delete this comment."}, status=status.HTTP_403_FORBIDDEN)


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