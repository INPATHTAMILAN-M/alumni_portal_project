from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import *
from job_portal.models import *
from event_portal.models import *
from media_portal.models import *

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username','is_active','groups']  # Add any other fields you need

    def get_groups(self, obj):
        return [{"id": group.id, "name": group.name} for group in obj.groups.all()]


class MemberListSerializer(serializers.ModelSerializer):
    # salutation = serializers.StringRelatedField()
    # batch = serializers.StringRelatedField()
    # course = serializers.StringRelatedField()
    # department = serializers.StringRelatedField()
    # user = serializers.StringRelatedField()
    
    class Meta:
        model = Member
        fields = [
            'id', 'salutation', 'gender', 'dob', 'blood_group', 'profile_picture',
            'batch', 'course', 'department', 'about_me', 'user', 'mobile_no',
            'email', 'file', 'register_no', 'is_approve'
        ]
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class MemberEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member_Education
        fields = ['id', 'member', 'institute', 'degree', 'start_year', 'end_year', 'is_currently_pursuing', 'location']

class MemberExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member_Experience
        fields = ['id', 'member', 'industry', 'role', 'start_date', 'end_date', 'is_currently_working', 'location']
        

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['name']  # Adjust this to match your model fields


class AlumniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumni
        fields = ['id', 'member', 'website', 'linked_in', 'twitter_handle', 'address', 'location', 'postal_code', 'registered_on']



# Serializer for Post
class PostLikeSerializer(serializers.ModelSerializer):
    liked_by = serializers.CharField(source='liked_by.username')
    class Meta:
        model = PostLike
        fields = ['liked_by']

class PostCommentSerializer(serializers.ModelSerializer):
    comment_by = serializers.CharField(source='comment_by.username')

    class Meta:
        model = PostComment
        fields = ['comment', 'comment_by']

class PostSerializer(serializers.ModelSerializer):
    post_likes_count = serializers.SerializerMethodField()
    post_comments_count = serializers.SerializerMethodField()
    post_comments = PostCommentSerializer(many=True, read_only=True)
    post_likes = PostLikeSerializer(many=True, read_only=True)
    created_by_username = serializers.CharField(source='posted_by.username')
    type = serializers.SerializerMethodField()
     
    class Meta:
        model = Post
        fields = ['title', 'blog', 'post_category', 'content', 'published', 'visible_to_public', 'featured_image', 
                  'posted_on', 'created_by_username', 'post_likes_count', 'post_comments_count', 'post_comments', 'post_likes','type']

    def get_post_likes_count(self, obj):
        return obj.post_likes.count() if obj.post_likes else 0

    def get_post_comments_count(self, obj):
        return obj.post_comments.count() if obj.post_comments else 0
    
    def get_type(self, obj):
        return 'Post'

# Serializer for Album
class AlbumPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumPhotos
        fields = ['photo']

class AlbumCommentSerializer(serializers.ModelSerializer):
    comment_by = serializers.CharField(source='comment_by.username')

    class Meta:
        model = AlbumComment
        fields = ['comment', 'comment_by']

class AlbumLikeSerializer(serializers.ModelSerializer):
    liked_by = serializers.CharField(source='liked_by.username')
    class Meta:
        model = AlbumLike
        fields = ['liked_by']

class AlbumSerializer(serializers.ModelSerializer):
    album_photos = AlbumPhotoSerializer(many=True, read_only=True)
    album_comments = AlbumCommentSerializer(many=True, read_only=True)
    album_likes = AlbumLikeSerializer(many=True, read_only=True)
    album_comments_count = serializers.SerializerMethodField()
    album_likes_count = serializers.SerializerMethodField()
    created_by_username = serializers.CharField(source='created_by.username')
    type = serializers.SerializerMethodField()
    
    class Meta:
        model = Album
        fields = ['album_name', 'description', 'album_location', 'album_date', 'public_view', 'created_on', 'created_by_username',
                  'album_photos', 'album_comments', 'album_comments_count', 'album_likes', 'album_likes_count','type']


    def get_album_comments_count(self, obj):
        return obj.album_comments.count() if obj.album_comments else 0

    def get_album_likes_count(self, obj):
        return obj.album_likes.count() if obj.album_likes else 0
    def get_type(self, obj):
        return 'Album'

# Serializer for Event
class EventCommentSerializer(serializers.ModelSerializer):
    comment_by = serializers.CharField(source='comment_by.username')

    class Meta:
        model = EventComment
        fields = ['comment', 'comment_by']

class EventLikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    class Meta:
        model = EventLike
        fields = ['user']

# serializers.py
class EventSerializer(serializers.ModelSerializer):
    event_comments = EventCommentSerializer(many=True, read_only=True)
    event_likes = EventLikeSerializer(many=True, read_only=True)
    event_comments_count = serializers.SerializerMethodField()
    event_likes_count = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.title')
    posted_by_username = serializers.CharField(source='posted_by.username')
    type = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['title', 'category_name', 'start_date', 'start_time', 'venue', 'address', 'link', 'is_public', 'need_registration',
                  'registration_close_date', 'description', 'event_wallpaper', 'instructions', 'posted_on', 'posted_by_username',
                  'is_active', 'event_comments', 'event_comments_count', 'event_likes', 'event_likes_count','type']

    def get_event_comments_count(self, obj):
        return obj.event_comments.count() if obj.event_comments else 0  # Return 0 if no comments

    def get_event_likes_count(self, obj):
        return obj.event_likes.count() if obj.event_likes else 0  # Return 0 if no likes

    def get_type(self, obj):
        return 'Event'


# Serializer for JobPost
class JobCommentSerializer(serializers.ModelSerializer):
    comment_by = serializers.CharField(source='comment_by.username')

    class Meta:
        model = JobComment
        fields = ['comment', 'comment_by']

class JobLikeSerializer(serializers.ModelSerializer):
    liked_by = serializers.CharField(source='liked_by.username')
    class Meta:
        model = JobLike
        fields = ['liked_by']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill  # Replace with the actual name of your Skill model
        fields = ['skill']

class JobPostSerializer(serializers.ModelSerializer):
    job_comments = JobCommentSerializer(many=True, read_only=True)
    job_likes = JobLikeSerializer(many=True, read_only=True)
    job_comments_count = serializers.SerializerMethodField()
    job_likes_count = serializers.SerializerMethodField()
    industry_name = serializers.CharField(source='industry.title')  # Assuming 'Industry' has a 'title' field
    role_name = serializers.CharField(source='role.role')  # Assuming 'Role' has a 'title' field
    posted_by_username = serializers.CharField(source='posted_by.username')
    skills = SkillSerializer(many=True)
    type = serializers.SerializerMethodField()
    
    class Meta:
        model = JobPost
        fields = ['job_title', 'industry_name', 'experience_level_from', 'experience_level_to', 'location', 'contact_email',
                  'contact_link', 'role_name', 'skills', 'salary_package', 'dead_line', 'job_description', 'file', 'post_type',
                  'posted_on', 'is_active', 'job_comments', 'job_comments_count', 'job_likes', 'job_likes_count','posted_by_username','type']

    def get_job_comments_count(self, obj):
        return obj.job_comments.count() if obj.job_comments else 0

    def get_job_likes_count(self, obj):
        return obj.job_likes.count() if obj.job_likes else 0
    
    def get_type(self, obj):
        return 'Job'

class MainSerializer(serializers.ModelSerializer):
    post = PostSerializer(many=True, read_only=True)
    album = AlbumSerializer(many=True, read_only=True)
    event = EventSerializer(many=True, read_only=True)
    job_post = JobPostSerializer(many=True, read_only=True)
    
    class Meta:
        fields = ['post', 'album', 'event', 'job_post']
        
# Member Milestone

class MemberMilestoneCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member_Milestone
        fields = ['id','member', 'title', 'description', 'year']

class MemberMilestoneListSerializer(serializers.ModelSerializer):
    member = MemberListSerializer()
    class Meta:
        model = Member_Milestone
        fields = ['id', 'member', 'title', 'description', 'year']

class MemberMilestoneUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Member_Milestone
        fields = ['id', 'member', 'title', 'description', 'year']

class MemberMilestoneRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member_Milestone
        fields = ['id','member',  'title', 'description', 'year']
    
    
    