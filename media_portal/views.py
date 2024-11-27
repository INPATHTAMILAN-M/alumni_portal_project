from django.shortcuts import get_object_or_404, render
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
            serializer.save(posted_by=self.request.user, published=False)

    
#admin can able to see the false post
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
            visible_to_public=request.data.get('visible_to_public', False),
            posted_by=request.user,
        )

        return Response({
            "message": "Post created successfully",
        }, status=status.HTTP_201_CREATED)
        
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

        post.save()

        return Response({
            "message": "Post updated successfully"
        }, status=status.HTTP_200_OK)