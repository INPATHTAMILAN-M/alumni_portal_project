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
    post_category = serializers.SerializerMethodField()
    member_id = serializers.SerializerMethodField()
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
        except (Member.DoesNotExist, AttributeError):
            return None

    def get_profile_photo(self, obj):
        try:
            member = obj.posted_by.member
            if member.profile_picture:
                return self.context['request'].build_absolute_uri(member.profile_picture.url)
            return None
        except (Member.DoesNotExist, AttributeError):
            return None

    def get_post_category(self, obj):
        try:
            if obj.post_category:
                return {
                    "id": obj.post_category.id,  # Return the ID of the post category
                    "name": obj.post_category.name  # Return the name of the post category
                }
        except AttributeError:
            return None  # Return None if post_category is not present
        return None


class MemberBirthdaySerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    fullname = serializers.CharField(source='user.get_full_name', read_only=True)
    batch = serializers.CharField(source='batch.end_year', read_only=True)
    course = serializers.CharField(source='course.department.short_name', read_only=True)
    member_id = serializers.IntegerField(source='id', read_only=True)
    faculty = serializers.BooleanField(read_only=True)
    department = serializers.CharField(read_only=True)

    class Meta:
        model = Member
        fields = ['profile_picture', 'fullname', 'email', 'batch', 'course', 'member_id', 'dob', 'faculty', 'department']

    def get_profile_picture(self, obj):
        """
        Method to get the absolute URL for the profile picture.
        """
        if obj.profile_picture:
            return self.context['request'].build_absolute_uri(obj.profile_picture.url)
        return None

    def to_representation(self, instance):
        """
        Customizing the representation based on the user's group.
        """
        representation = super().to_representation(instance)
        
        user_groups = instance.user.groups.values_list('name', flat=True)
        
        if 'Faculty' in user_groups:
            # For faculty, show the department directly from the Member model
            representation['faculty'] = True
            representation['department'] = instance.department.short_name if instance.department else 'N/A'
        elif 'Alumni' in user_groups:
            # For alumni, show the department from the course
            representation['faculty'] = False
            representation['department'] = instance.course.department.short_name if instance.course and instance.course.department else 'N/A'
        
        return representation

    
class AlbumPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumPhotos
        fields = ['id', 'photo', 'uploaded_on', 'approved']

class AlbumSerializer(serializers.ModelSerializer):
    photos = AlbumPhotoSerializer(many=True, read_only=True, source='albumphotos_set')

    class Meta:
        model = Album
        fields = ['id', 'album_name', 'description', 'album_location', 'album_date', 
                  'public_view', 'created_on', 'created_by', 'photos']
        
class MemoryTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryTags
        fields = ['id', 'tag']

class MemoryPhotosSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = MemoryPhotos
        fields = ['id', 'photo']

    def get_photo(self, obj):
        """
        Method to get the absolute URL for the photo.
        """
        if obj.photo:
            return self.context['request'].build_absolute_uri(obj.photo.url)
        return None

class MemorySerializer(serializers.ModelSerializer):
    tags = MemoryTagsSerializer(many=True, read_only=True, source='memorytags')  # Use related_name for source
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Memories
        fields = ['id', 'year', 'month', 'approved', 'tags', 'photos']
        read_only_fields = ['approved']
        
    
    def get_photos(self, obj):
        """
        Method to get the absolute URL for the photos.
        """
        photos = obj.memoryphoto.all()
        return MemoryPhotosSerializer(photos, many=True, context=self.context).data

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        photos_data = validated_data.pop('photos', [])
        memory = Memories.objects.create(**validated_data)

        # Save tags
        for tag_data in tags_data:
            MemoryTags.objects.create(memory=memory, **tag_data)

        # Save photos
        for photo_data in photos_data:
            MemoryPhotos.objects.create(memory=memory, **photo_data)

        return memory
    
class MemoryUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Memories
        fields = ['id', 'year', 'month', 'approved']
        read_only_fields = ['approved']
        