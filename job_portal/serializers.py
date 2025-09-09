from rest_framework import serializers
from .models import *
from account.models import Industry, Role, Skill
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

# Industry Serializer
class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['id', 'title']

# Role Serializer
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'role']

# Skill Serializer
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'skill']

# JobPost Serializer with nested serializers
class JobPostSerializer(serializers.ModelSerializer):
    posted_by = UserSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    industry = IndustrySerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    
    class Meta:
        model = JobPost
        fields = [
            'id',
            'posted_by',
            'job_title',
            'industry',
            'experience_level_from',
            'experience_level_to',
            'location',
            'contact_email',
            'contact_link',
            'role',
            'skills',
            'salary_package',
            'dead_line',
            'job_description',
            'file',
            'post_type',
            'is_active',
            'picture',
        ]

    def to_representation(self, instance):
        # Call the parent class to get the original representation
        representation = super().to_representation(instance)

        # Replace 'file' with its absolute URL if it exists
        if instance.file:
            request = self.context.get('request')
            representation['file'] = request.build_absolute_uri(instance.file.url)

        return representation

class JobPostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = [
            'job_title', 'industry', 'experience_level_from', 'experience_level_to',
            'location', 'contact_email', 'contact_link', 'role', 'salary_package',
            'dead_line', 'job_description', 'post_type', 'skills', 'file'
        ]

    def update(self, instance, validated_data):
        # Handle skills separately if needed
        skills_data = validated_data.pop('skills', None)
        
        # Update the instance fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if skills_data is not None:
            instance.skills.set(skills_data)

        instance.save()
        return instance
