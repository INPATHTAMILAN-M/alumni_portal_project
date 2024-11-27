from rest_framework import serializers

from account.models import Member
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
    member_id = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = PostLike
        fields = ['liked_by', 'member_id', 'profile_photo']

    def get_member_id(self, obj):
        try:
            return obj.liked_by.member.id
        except Member.DoesNotExist:
            return None

    def get_profile_photo(self, obj):
        try:
            member = obj.liked_by.member
            if member.profile_picture:
                return self.context['request'].build_absolute_uri(member.profile_picture.url)
            return None
        except Member.DoesNotExist:
            return None


class PostCommentSerializer(serializers.ModelSerializer):
    comment_by = serializers.CharField(source='comment_by.username')
    member_id = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()
    is_comment = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = ['id','comment', 'comment_by', 'comment_on', 'is_comment', 'member_id', 'profile_photo']

    def get_is_comment(self, obj):
        user = self.context['request'].user
        return obj.comment_by == user 

    def get_member_id(self, obj):
        try:
            return obj.comment_by.member.id
        except Member.DoesNotExist:
            return None

    def get_profile_photo(self, obj):
        try:
            member = obj.comment_by.member
            if member.profile_picture:
                # Generate the absolute URL
                return self.context['request'].build_absolute_uri(member.profile_picture.url)
            return None
        except Member.DoesNotExist:
            return None

    
class PostSerializer(serializers.ModelSerializer):
    post_likes_count = serializers.SerializerMethodField()
    post_comments_count = serializers.SerializerMethodField()
    post_comments = PostCommentSerializer(many=True, read_only=True)
    post_likes = PostLikeSerializer(many=True, read_only=True)
    posted_by = serializers.SerializerMethodField()
    post_liked = serializers.SerializerMethodField()
    post_category = serializers.CharField(source='post_category.name', read_only=True)
    member_id = serializers.IntegerField(source='posted_by.member.id', read_only=True)
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'blog', 'post_category', 'content', 'published', 'visible_to_public', 'featured_image', 
                  'posted_on', 'posted_by', 'post_likes_count', 'post_comments_count', 'post_comments', 'post_likes', 
                  'post_liked', 'member_id', 'profile_photo']

    def get_post_likes_count(self, obj):
        return obj.post_likes.count() if obj.post_likes else 0

    def get_post_comments_count(self, obj):
        return obj.post_comments.count() if obj.post_comments else 0

    def get_post_liked(self, obj):
        user = self.context['request'].user
        return obj.post_likes.filter(liked_by=user).exists()

    def get_posted_by(self, obj):
        return obj.posted_by.username

    def get_member_id(self, obj):
        try:
            return obj.posted_by.member.id
        except Member.DoesNotExist:
            return None

    def get_profile_photo(self, obj):
        try:
            member = obj.posted_by.member
            if member.profile_picture:
                return self.context['request'].build_absolute_uri(member.profile_picture.url)
            return None
        except Member.DoesNotExist:
            return None

class MemberBirthdaySerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField()
    fullname = serializers.CharField(source='user.get_full_name', read_only=True)
    batch = serializers.CharField(source='batch.title', read_only=True)
    course = serializers.CharField(source='course.title', read_only=True)
    member_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Member
        fields = ['profile_picture', 'fullname', 'batch', 'course', 'member_id','dob']

