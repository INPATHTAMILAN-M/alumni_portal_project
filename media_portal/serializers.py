from rest_framework import serializers
from .models import *
from django.core.exceptions import ValidationError


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = '__all__'


class PostSerializerview(serializers.ModelSerializer):
    posted_by = serializers.SerializerMethodField()
    post_category = serializers.PrimaryKeyRelatedField(queryset=PostCategory.objects.all())

    class Meta:
        model = Post
        fields = ['id','title', 'blog', 'post_category', 'content', 'published', 
                  'visible_to_public', 'featured_image', 'posted_on', 'posted_by']
        
    def get_posted_by(self, obj):
        return obj.posted_by.username
    
    def get_post_category(self, obj):
        return obj.post_category.name

class PostComment_Serializer(serializers.ModelSerializer):
    comment_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = PostComment
        fields = ['id', 'post', 'comment_by', 'comment']
        
class PostLike_Serializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['id', 'post', 'liked_by']
        
class PostLikeSerializer(serializers.ModelSerializer):
    liked_by = serializers.CharField(source='liked_by.username')
    class Meta:
        model = PostLike
        fields = ['liked_by']

class PostCommentSerializer(serializers.ModelSerializer):
    comment_by = serializers.CharField(source='comment_by.username')
    is_comment = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = ['comment', 'comment_by', 'comment_on','is_comment']
    
    def get_is_comment(self, obj):
        user = self.context['request'].user  
        return obj.comment_by == user 
        
class PostSerializer(serializers.ModelSerializer):
    post_likes_count = serializers.SerializerMethodField()
    post_comments_count = serializers.SerializerMethodField()
    post_comments = PostCommentSerializer(many=True, read_only=True)
    post_likes = PostLikeSerializer(many=True, read_only=True)
    posted_by = serializers.SerializerMethodField()
    post_liked = serializers.SerializerMethodField()
    post_category = serializers.CharField(source='post_category.name', read_only=True) 
     
    class Meta:
        model = Post
        fields = ['id','title', 'blog', 'post_category', 'content', 'published', 'visible_to_public', 'featured_image', 
                  'posted_on', 'posted_by', 'post_likes_count', 'post_comments_count', 'post_comments', 'post_likes', 'post_liked']

    def get_post_likes_count(self, obj):
        return obj.post_likes.count() if obj.post_likes else 0

    def get_post_comments_count(self, obj):
        return obj.post_comments.count() if obj.post_comments else 0
    
    def get_post_liked(self, obj):
        user = self.context['request'].user  # Access the request from the serializer context
        return obj.post_likes.filter(liked_by=user).exists()
    
    def get_posted_by(self, obj):
        return obj.posted_by.username
    
