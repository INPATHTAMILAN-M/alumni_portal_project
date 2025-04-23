import csv
import datetime
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.crypto import get_random_string
from rest_framework import status
from django.contrib.auth.models import User, Group
from alumni_portal.settings import FRONTEND_URL
from .serializers import *
import pandas as pd
from django.contrib.auth.models import User
from .models import *
import random
import string
from django.core.mail import send_mail
from .permissions import *
from django.db.models import Q
from rest_framework import status
from django.db.models import Sum


class Login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            member = None
            try:
                member = Member.objects.get(email=username)
            except Member.DoesNotExist:
                member = None  # Keep it None if member does not exist

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            if member is not None:
                profile_picture_check = bool(member.profile_picture)

                # Module 2: Check if Skills and Education are populated
                skills_check = Member_Skills.objects.filter(member=member).exists() and all(
                    skill.member is not None for skill in Member_Skills.objects.filter(member=member)
                )

                education_check = Member_Education.objects.filter(member=member).exists() and all(
                    edu.member for edu in Member_Education.objects.filter(member=member)
                )
                
                # If both Skills and Education are valid, set module2_check to True
                module2_check = skills_check and education_check

                # Module 3: Check if Experience is valid (not null)
                experience_check = Member_Experience.objects.filter(member=member).exists() and all(
                    exp.member is not None  for exp in Member_Experience.objects.filter(member=member)
                )

                # Module 4: Check if Alumni is valid (not null)
                alumni_check = Alumni.objects.filter(member=member).exists() and all(
                    alum.member for alum in Alumni.objects.filter(member=member)
                )

                milestone_check = Member_Milestone.objects.filter(member=member).exists() and all(
                    milestone.member is not None  for milestone in Member_Milestone.objects.filter(member=member)
                )
                # Creating a dictionary for module checks
                modules = {
                    'module1': profile_picture_check,
                    'module2': module2_check,
                    'module3': experience_check,
                    'module4': alumni_check,
                    'milestone': milestone_check, 
                }

            else:
                # Member does not exist, return tokens and user info without module checks
                modules = {}

            group_names = user.groups.values_list('name', flat=True)
            group_dict = {group_name: True for group_name in group_names}

            return Response({
                'refresh': refresh_token,
                'access': access_token,
                'username': username,
                'user_id': user.id,
                'member_id': member.id if member else None,
                'modules': modules,
                'groups': group_dict
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# class Login(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)
#         member = None

#         try:
#             member = Member.objects.get(email=username)
#         except Member.DoesNotExist:
#             member = None  # Keep it None if member does not exist

#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             access_token = str(refresh.access_token)
#             refresh_token = str(refresh)
#             group_names = user.groups.values_list('name', flat=True)

#             # Create a dictionary with group names as keys and True as values
#             group_dict = {group_name: True for group_name in group_names}

#             return Response({
#                 'refresh': refresh_token,
#                 'access': access_token,
#                 'username': username,
#                 'user_id': user.id,
#                 'member_id': member.id if member else None,
#                 'groups': group_dict  # Updated to use the group dictionary
#             }, status=status.HTTP_200_OK)

#         return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ForgetPassword(APIView):
    def post(self, request):
        email = request.data.get('email')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        new_password = get_random_string(length=8)
        user.set_password(new_password)
        user.save()

        send_mail(
            'Your Password has reset',
            f'Your new password is: {new_password}. Make your password with more secure',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response({'message': 'Password reset token has been sent to your email'})


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('oldPassword')
        new_password = request.data.get('newPassword')

        if not user.check_password(old_password):
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return Response({
            'message': 'Password has been successfully changed',
            'refresh': refresh_token,
            'access': access_token,
        })

class CreateUser(APIView):
    # permission_classes = [IsAuthenticated, IsAlumniManagerOrAdministrator]

    def post(self, request):
        username = request.data.get('email')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            return Response({"error": "User with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create_user(username=username, password=password)

        return Response({"success": "User created successfully.", "user_id": user.id}, status=status.HTTP_201_CREATED)

# Assign Role
class Users(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]
    def get(self, request):
        users = User.objects.all().order_by('-id')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class Groups(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]
    def get(self, request):
        groups = Group.objects.all().order_by('-id')
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

class Assign_Group(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def post(self, request):
        user_id = request.data.get('id')
        group_ids = request.data.get('group_ids')  # Expecting a list of group IDs

        if not group_ids:
            return Response({'error': 'group_ids is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # If group_ids is a single value, convert it to a list
        # if isinstance(group_ids, int):
        #     group_ids = [group_ids]
        # elif not isinstance(group_ids, list):
        #     return Response({'error': 'group_ids must be a list or an integer.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Get all groups currently assigned to the user
        current_groups = set(user.groups.values_list('id', flat=True))
        new_groups = set(group_ids)

        # Determine groups to remove
        groups_to_remove = current_groups - new_groups
        # Determine groups to add
        groups_to_add = new_groups - current_groups

        # Remove user from groups no longer assigned
        for group_id in groups_to_remove:
            try:
                group = Group.objects.get(id=group_id)
                group.user_set.remove(user)
            except Group.DoesNotExist:
                continue  # If the group doesn't exist, skip

        # Add user to new groups
        for group_id in groups_to_add:
            try:
                group = Group.objects.get(id=group_id)
                group.user_set.add(user)
            except Group.DoesNotExist:
                continue  

        response_message = {
            'message': 'User groups updated successfully.',

        }

        return Response(response_message, status=status.HTTP_200_OK)
    
# Deactivate user

class DeactivateUser(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.is_active = request.data.get('is_active')
            user.save()
            return Response({"message": "User account deactivated successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)


# active data for dropdown
class ActiveDepartment(APIView):
    def get(self, request):
        departments = Department.objects.filter(is_active=True).order_by('-id')
        data = [
            {
                "department_id": department.id,
                "short_name": department.short_name,
                "full_name": department.full_name,
                "is_active": department.is_active
            }
            for department in departments
        ]
        return Response(data, status=status.HTTP_200_OK)

class ActiveCourse(APIView):
    def get(self, request):
        courses = Course.objects.filter(is_active=True).order_by('-id')
        data = [
            {
                "course_id": course.id,
                "title": course.title,
                "graduate": course.graduate,
                "department": course.department.full_name,
                "is_active": course.is_active
            }
            for course in courses
        ]
        return Response(data, status=status.HTTP_200_OK)


# Manage Salutation
class CreateSalutation(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]
    def post(self, request):
        salutation = Salutation(
            salutation= request.data['salutation'],
            description= request.data['description'],
        )
        salutation.save()

        return Response({"message": "Salutation created successfully"}, status=status.HTTP_201_CREATED)

class RetrieveSalutation(APIView):
    def get(self, request):
        salutations = Salutation.objects.all().order_by('-id')
        data = [
            {
                "salutation_id": salutation.id,
                "salutation_name": salutation.salutation,
                "description": salutation.description,
            }
            for salutation in salutations
        ]
        return Response(data, status=status.HTTP_200_OK)

class UpdateSalutation(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]
    def get(self, request, salutation_id):
        try:
            salutation = Salutation.objects.get(id=salutation_id)
            data = {
                "salutation": salutation.salutation,
                "description": salutation.description,
            }
            return Response(data, status=status.HTTP_200_OK)
        except Salutation.DoesNotExist:
            return Response({"message": "Salutation not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, salutation_id):
        try:
            salutation = Salutation.objects.filter(id=salutation_id)
        except Salutation.DoesNotExist:
            return Response({"message": "Salutation not found"}, status=status.HTTP_404_NOT_FOUND)
        salutation.update(
        salutation = request.data["salutation"],
        description = request.data["description"],
        )

        return Response({"message": "Salutation updated successfully"}, status=status.HTTP_200_OK)


# manage Batch
class CreateBatch(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def post(self, request):
        batch = Batch(
            title=request.data['title'],
            start_year=request.data['start_year'],
            end_year=request.data['end_year']
        )
        batch.save()
        return Response({"message": "Batch created successfully"}, status=status.HTTP_201_CREATED)

class RetrieveBatch(APIView):
    def get(self, request):
        batches = Batch.objects.all().order_by('-id')
        data = [
            {
                "batch_id": batch.id,
                "title": batch.title,
                "start_year": batch.start_year,
                "end_year": batch.end_year
            }
            for batch in batches
        ]
        return Response(data, status=status.HTTP_200_OK)

class UpdateBatch(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def get(self, request, batch_id):
        try:
            batch = Batch.objects.get(id=batch_id)
            data = {
                "title": batch.title,
                "start_year": batch.start_year,
                "end_year": batch.end_year
            }
            return Response(data, status=status.HTTP_200_OK)
        except Batch.DoesNotExist:
            return Response({"message": "Batch not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, batch_id):
        try:
            batch = Batch.objects.get(id=batch_id)
        except Batch.DoesNotExist:
            return Response({"message": "Batch not found"}, status=status.HTTP_404_NOT_FOUND)
        batch.title = request.data["title"]
        batch.start_year = request.data["start_year"]
        batch.end_year = request.data["end_year"]
        batch.save()

        return Response({"message": "Batch updated successfully"}, status=status.HTTP_200_OK)

# manage Department
class CreateDepartment(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def post(self, request):
        department = Department(
            short_name=request.data['short_name'],
            full_name=request.data['full_name'],
            is_active=request.data.get('is_active', True)
        )
        department.save()
        return Response({"message": "Department created successfully"}, status=status.HTTP_201_CREATED)

class RetrieveDepartment(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def get(self, request):
        departments = Department.objects.all().order_by('-id')
        data = [
            {
                "department_id": department.id,
                "short_name": department.short_name,
                "full_name": department.full_name,
                "is_active": department.is_active
            }
            for department in departments
        ]
        return Response(data, status=status.HTTP_200_OK)

class UpdateDepartment(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def get(self, request, department_id):
        try:
            department = Department.objects.get(id=department_id)
            data = {
                "short_name": department.short_name,
                "full_name": department.full_name,
                "is_active": department.is_active
            }
            return Response(data, status=status.HTTP_200_OK)
        except Department.DoesNotExist:
            return Response({"message": "Department not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, department_id):
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            return Response({"message": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        department.short_name = request.data["short_name"]
        department.full_name = request.data["full_name"]
        department.is_active = request.data.get("is_active", department.is_active)
        department.save()

        return Response({"message": "Department updated successfully"}, status=status.HTTP_200_OK)

class InactiveDepartment(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]
    def put(self, request, department_id):
        
        if department_id is None:
            return Response({"message": "Department ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            department = Department.objects.get(id=department_id)
            department.is_active = request.data.get('is_active')

            department.save()
            return Response({"message": "Department status has been updated successfully"}, status=status.HTTP_200_OK)
        except Department.DoesNotExist:
            return Response({"message": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        

# manage course
class CreateCourse(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def post(self, request):
        course = Course(
            title=request.data['title'],
            graduate=request.data['graduate'],
            department_id=request.data['department_id'],  # assuming department_id is passed
            is_active=request.data.get('is_active', True)
        )
        course.save()
        return Response({"message": "Course created successfully"}, status=status.HTTP_201_CREATED)

class RetrieveCourse(APIView):
    def get(self, request):
        courses = Course.objects.all().order_by('-id')
        data = [
            {
                "course_id": course.id,
                "title": course.title,
                "graduate": course.graduate,
                "department": course.department.full_name,
                "department_id": course.department.id,
                "is_active": course.is_active
            }
            for course in courses
        ]
        return Response(data, status=status.HTTP_200_OK)

class UpdateCourse(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    # def get(self, request, course_id):
    #     try:
    #         course = Course.objects.get(id=course_id)
    #         data = {
    #             "title": course.title,
    #             "graduate": course.graduate,
    #             "department_id": course.department.id,
    #             "is_active": course.is_active
    #         }
    #         return Response(data, status=status.HTTP_200_OK)
    #     except Course.DoesNotExist:
    #         return Response({"message": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"message": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        course.title = request.data["title"]
        course.graduate = request.data["graduate"]
        course.department_id = request.data["department_id"]
        course.is_active = request.data.get("is_active", course.is_active)
        course.save()

        return Response({"message": "Course updated successfully"}, status=status.HTTP_200_OK)

class InactiveCourse(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]
    def put(self, request, course_id):
        
        if course_id is None:
            return Response({"message": "Course ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            course = Course.objects.get(id=course_id)
            course.is_active = request.data.get('is_active')

            course.save()
            return Response({"message": "Course status has been updated successfully"}, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({"message": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        

# manage Institution Views
class CreateInstitution(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def post(self, request):
        institution = Institution(
            title=request.data['title'],
            description=request.data.get('description', '')
        )
        institution.save()
        return Response({"message": "Institution created successfully"}, status=status.HTTP_201_CREATED)

class RetrieveInstitution(APIView):
    def get(self, request):
        institutions = Institution.objects.all().order_by('-id')
        data = [{"id": inst.id, "title": inst.title, "description": inst.description} for inst in institutions]
        return Response(data, status=status.HTTP_200_OK)

class UpdateInstitution(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def get(self, request, institution_id):
        try:
            institution = Institution.objects.get(id=institution_id)
            data = {
                "title": institution.title,
                "description": institution.description
            }
            return Response(data, status=status.HTTP_200_OK)
        except Institution.DoesNotExist:
            return Response({"message": "Institution not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, institution_id):
        try:
            institution = Institution.objects.get(id=institution_id)
        except Institution.DoesNotExist:
            return Response({"message": "Institution not found"}, status=status.HTTP_404_NOT_FOUND)

        institution.title = request.data.get("title", institution.title)
        institution.description = request.data.get("description", institution.description)
        institution.save()

        return Response({"message": "Institution updated successfully"}, status=status.HTTP_200_OK)

# manage social media

class CreateSocialMedia(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def post(self, request):
        social_media = Social_Media(
            title=request.data['title'],
            icon=request.FILES['icon'],  # Assuming you're uploading a file
            url=request.data['url'],
            is_active=request.data.get('is_active', True)
        )
        social_media.save()
        return Response({"message": "Social Media entry created successfully"}, status=status.HTTP_201_CREATED)

class RetrieveSocialMedia(APIView):
    def get(self, request):
        social_media_entries = Social_Media.objects.all().order_by('-id')
        data = [
            {
                "id": sm.id,
                "title": sm.title,
                "icon": request.build_absolute_uri(sm.icon.url) if sm.icon else None,
                "url": sm.url,
                "is_active": sm.is_active
            }
            for sm in social_media_entries
        ]
        return Response(data, status=status.HTTP_200_OK)


class UpdateSocialMedia(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def get(self, request, social_media_id):
        try:
            social_media = Social_Media.objects.get(id=social_media_id)
            data = {
                "title": social_media.title,
                "icon": request.build_absolute_uri(social_media.icon.url) if social_media.icon else None,
                "url": social_media.url,
                "is_active": social_media.is_active
            }
            return Response(data, status=status.HTTP_200_OK)
        except Social_Media.DoesNotExist:
            return Response({"message": "Social Media entry not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request, social_media_id):
        try:
            social_media = Social_Media.objects.get(id=social_media_id)
        except Social_Media.DoesNotExist:
            return Response({"message": "Social Media entry not found"}, status=status.HTTP_404_NOT_FOUND)

        social_media.title = request.data.get("title", social_media.title)
        if 'icon' in request.FILES:
            social_media.icon = request.FILES['icon']
        social_media.url = request.data.get("url", social_media.url)
        social_media.is_active = request.data.get("is_active", social_media.is_active)
        social_media.save()

        return Response({"message": "Social Media entry updated successfully"}, status=status.HTTP_200_OK)

class InactiveSocialMedia(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def put(self, request, social_media_id):
        if social_media_id is None:
            return Response({"message": "Social Media ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            social_media = Social_Media.objects.get(id=social_media_id)
            social_media.is_active = request.data.get('is_active', not social_media.is_active)
            social_media.save()
            return Response({"message": "Social Media status has been updated successfully"}, status=status.HTTP_200_OK)
        except Social_Media.DoesNotExist:
            return Response({"message": "Social Media entry not found"}, status=status.HTTP_404_NOT_FOUND)
        
# manage role
class CreateRole(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def post(self, request):
        role = Role(role=request.data['role'], description=request.data.get('description', ''))
        role.save()
        return Response({"message": "Role created successfully"}, status=status.HTTP_201_CREATED)

class RetrieveRoles(APIView):
    def get(self, request):
        roles = Role.objects.all().order_by('-id')
        data = [{"id": role.id, "role": role.role, "description": role.description} for role in roles]
        return Response(data, status=status.HTTP_200_OK)

class UpdateRole(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def get(self, request, role_id):
        try:
            role = Role.objects.get(id=role_id)
            data = {
                "role": role.role,
                "description": role.description
            }
            return Response(data, status=status.HTTP_200_OK)
        except Role.DoesNotExist:
            return Response({"message": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, role_id):
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response({"message": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

        role.role = request.data.get("role", role.role)
        role.description = request.data.get("description", role.description)
        role.save()

        return Response({"message": "Role updated successfully"}, status=status.HTTP_200_OK)

# manage Industry Views
class CreateIndustry(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def post(self, request):
        industry = Industry(
            title=request.data['title'],
            description=request.data['description'],
            website=request.data['website']
        )
        industry.save()
        return Response({"message": "Industry created successfully"}, status=status.HTTP_201_CREATED)

class RetrieveIndustry(APIView):
    def get(self, request):
        industries = Industry.objects.all().order_by('-id')
        data = [{"id": ind.id, "title": ind.title, "description": ind.description, "website": ind.website} for ind in industries]
        return Response(data, status=status.HTTP_200_OK)

class UpdateIndustry(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def get(self, request, industry_id):
        try:
            industry = Industry.objects.get(id=industry_id)
            data = {
                "title": industry.title,
                "description": industry.description,
                "website": industry.website
            }
            return Response(data, status=status.HTTP_200_OK)
        except Industry.DoesNotExist:
            return Response({"message": "Industry not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, industry_id):
        try:
            industry = Industry.objects.get(id=industry_id)
        except Industry.DoesNotExist:
            return Response({"message": "Industry not found"}, status=status.HTTP_404_NOT_FOUND)

        industry.title = request.data.get("title", industry.title)
        industry.description = request.data.get("description", industry.description)
        industry.website = request.data.get("website", industry.website)
        industry.save()

        return Response({"message": "Industry updated successfully"}, status=status.HTTP_200_OK)

# manage Location Views
class CreateLocation(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def post(self, request):
        location = Location(location=request.data['location'])
        location.save()
        return Response({"message": "Location created successfully"}, status=status.HTTP_201_CREATED)

class RetrieveLocation(APIView):
    def get(self, request):
        locations = Location.objects.all()
        data = [{"id": loc.id, "location": loc.location} for loc in locations]
        return Response(data, status=status.HTTP_200_OK)

class UpdateLocation(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def get(self, request, location_id):
        try:
            location = Location.objects.get(id=location_id)
            data = {
                "location": location.location
            }
            return Response(data, status=status.HTTP_200_OK)
        except Location.DoesNotExist:
            return Response({"message": "Location not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, location_id):
        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return Response({"message": "Location not found"}, status=status.HTTP_404_NOT_FOUND)

        location.location = request.data.get("location", location.location)
        location.save()

        return Response({"message": "Location updated successfully"}, status=status.HTTP_200_OK)


# manage Country 
class CreateCountry(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def post(self, request):
        country = Country(
            country_name=request.data['country_name'],
            country_code=request.data.get('country_code', '')
        )
        country.save()
        return Response({"message": "Country created successfully"}, status=status.HTTP_201_CREATED)

class RetrieveCountry(APIView):
    def get(self, request):
        countries = Country.objects.all()
        data = [{"id": country.id, "country_name": country.country_name, "country_code": country.country_code} for country in countries]
        return Response(data, status=status.HTTP_200_OK)

class UpdateCountry(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def get(self, request, country_id):
        try:
            country = Country.objects.get(id=country_id)
            data = {
                "country_name": country.country_name,
                "country_code": country.country_code
            }
            return Response(data, status=status.HTTP_200_OK)
        except Country.DoesNotExist:
            return Response({"message": "Country not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, country_id):
        try:
            country = Country.objects.get(id=country_id)
        except Country.DoesNotExist:
            return Response({"message": "Country not found"}, status=status.HTTP_404_NOT_FOUND)

        country.country_name = request.data.get("country_name", country.country_name)
        country.country_code = request.data.get("country_code", country.country_code)
        country.save()

        return Response({"message": "Country updated successfully"}, status=status.HTTP_200_OK)


# register process

# alumni can register
class RegisterUsers(APIView):
    
    def post(self, request):
        email = request.data.get('email')
        
        # Check if email exists in Member model
        try:
            member = Member.objects.get(email=email)
        except Member.DoesNotExist:
            return Response({'error': 'Email not found in our records'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if member is approved
        if not member.is_approve:
            return Response({'error': 'Still you are not approved by admin. If approved, you will receive an email.'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        # Check user group
        if member.user is not None:
            if member.user.groups.filter(name='Faculty').exists():
                return Response({'error': 'Faculties have only the option to login'}, status=status.HTTP_403_FORBIDDEN)
            elif member.user.groups.filter(name='Alumni').exists():
                return Response({'error': 'You have already registered'}, status=status.HTTP_400_BAD_REQUEST)

        
        # Generate OTP
        otp = random.randint(100000, 999999)

        # Send OTP to email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            'noreply@yourdomain.com',
            [email],
            fail_silently=False,
        )
        
        # Store OTP in session (or any secure storage)
        # request.session['otp'] = otp
        # request.session['member_id'] = member.id

        return Response({
            'otp':otp,
            'message': 'OTP sent to email',
            'member_id': member.id
                         
            }, status=status.HTTP_200_OK)


class CreateOwnMember(APIView):
    
    def post(self, request):
        # Manually extract data from request
        try:
            salutation_id = request.data.get('salutation')
            gender = request.data.get('gender')
            profile_picture = request.data.get('profile_picture')
            batch_id = request.data.get('batch')
            course_id = request.data.get('course')
            mobile_no = request.data.get('mobile_no')
            email = request.data.get('email')
            file = request.data.get('file')
            register_no = request.data.get('register_no')

            # Manually validate fields
            if not email:
                return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if register_no already exists
            member = None
            if register_no:
                try:
                    member = Member.objects.get(register_no=register_no)
                except Member.DoesNotExist:
                    member = None
            
            # If member with the same register_no exists and the conditions are met, update the data
            if member:
                if member.email == email and not member.is_approve:
                    return Response({"error": "Still you are not approved by admin. If approved, you will receive an email."}, status=status.HTTP_400_BAD_REQUEST)
                elif member.user is None and member.is_approve:
                    
                    if salutation_id:
                        salutation = Salutation.objects.get(id=salutation_id)
                        member.salutation = salutation
                    if gender:
                        member.gender = gender
                    if profile_picture:
                        member.profile_picture = profile_picture
                    if batch_id:
                        batch = Batch.objects.get(id=batch_id)
                        member.batch = batch
                    if course_id:
                        course = Course.objects.get(id=course_id)
                        member.course = course
                    if mobile_no:
                        member.mobile_no = mobile_no
                    if email:
                        member.email = email
                    if file:
                        member.file = file
                    member.is_approve=True
                    member.save()  # Save the updated member
                    return Response({'message': 'Admin Approved you, Now you can registerd with email'}, status=status.HTTP_200_OK)
                else:
                    # If member is already approved or user is not null, return an error message
                    return Response({"error": "Entered data already exists. Please check the entered register number."}, status=status.HTTP_400_BAD_REQUEST)

            else:
                # If no existing member, create a new one
                salutation = Salutation.objects.get(id=salutation_id)
                batch = Batch.objects.get(id=batch_id) if batch_id else None
                course = Course.objects.get(id=course_id) if course_id else None
                
                # Create a new Member instance
                member = Member.objects.create(
                    salutation=salutation,
                    gender=gender,
                    profile_picture=profile_picture,
                    batch=batch,
                    course=course,
                    mobile_no=mobile_no,
                    email=email,
                    file=file,
                    register_no=register_no,
                    is_approve=False  # New member, so not approved yet
                )

                return Response({'message': 'You are waiting for approval. After receiving approval, you will get an email.'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
class PendingMembers(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        # Extract data from the JSON body
        members = Member.objects.filter(is_approve=False)
        data = []
        
        for member in members:
            data.append({
                'member_id': member.id,
                'register_no': member.register_no,
                'profile_picture': request.build_absolute_uri(member.profile_picture.url) if member.profile_picture else None,
                'email': member.email,
                'mobile_no': member.mobile_no,
                'batch': member.batch.title if member.batch else None,
                'course': member.course.title if member.course else None,
                'file': request.build_absolute_uri(member.file.url) if member.file else None,
                
            })
        
        return Response(data, status=status.HTTP_200_OK)

class ApproveMember(APIView):
    permission_classes = [IsAuthenticated]  # Uncomment if authentication is required

    def post(self, request, member_id):
        try:
            # Get the member by ID
            member = Member.objects.get(id=member_id)

            # Update the approval status of the member
            member.is_approve = True
            member.save()
            register_url= FRONTEND_URL.rstrip("/") + "/registration"
            # Send the approval email
            email_subject = 'Your Membership has been Approved'
            email_message = (
                f"Dear {member.email},\n\n"
                f"Your membership has been approved by the admin. You can now register by following the link below:\n"
                f"{register_url}\n\n"
                f"Best regards,\n[Your Karpagam Collage of Pharmacy]"
            )

            # Send email to the member
            send_mail(
                subject=email_subject,
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[member.email],
                fail_silently=False,  # Set to True if you don't want to raise exceptions on failure
            )

            return Response({'message': 'Member approved and email sent successfully'}, status=status.HTTP_200_OK)

        except Member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
    

# alumni set password
class CreatingUser(APIView):
    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')
        member_id = request.data.get('member_id')
        # Fetch the member object
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a user with the email as the username
        try:
            user = User.objects.create_user(
                username=member.email,
                first_name=first_name,
                last_name=last_name,
                email=member.email,
                password=password
            )
        except IntegrityError:
            return Response({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        alumni_group = Group.objects.get(name='Alumni')
        user.groups.add(alumni_group)
        # Link the user to the member
        member.user = user
        member.save()

        return Response({'member_id':member.id,'message': 'User account created and linked to member successfully'}, status=status.HTTP_201_CREATED)
        
# alumni can edit member details
class ShowMemberData(APIView):
    
    def get(self, request, member_id):
        # member_id = request.data.get('member_id')
        
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        member_data = {
            'salutation': member.salutation.id if member.salutation else None,
            'first_name': member.user.first_name if member.user else None,
            'last_name': member.user.last_name if member.user else None,
            'email': member.email if member.email else None,
            'gender': member.gender if member.gender else None,
            'dob': member.dob if member.dob else None,
            'blood_group': member.blood_group if member.blood_group else None,
            'mobile_no': member.mobile_no if member.mobile_no else None,
            'batch': member.batch.id if member.batch else None,
            'course': member.course.id if member.course else None,
            'about_me': member.about_me if member.about_me else None,
            'register_no': member.register_no if member.register_no else None,
        }
        
        return Response({'member_data': member_data}, status=status.HTTP_200_OK)
    def post(self, request,member_id):
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update member fields with the new data
        member.salutation_id = request.data.get('salutation') or member.salutation_id
        member.gender = request.data.get('gender') or member.gender
        member.dob = request.data.get('dob') or member.dob
        member.blood_group = request.data.get('blood_group') or member.blood_group
        member.batch_id = request.data.get('batch') or member.batch_id
        member.course_id = request.data.get('course') or member.course_id
        member.about_me = request.data.get('about_me') or member.about_me
        member.mobile_no = request.data.get('mobile_no') or member.mobile_no
        member.email = request.data.get('email') or member.email
        member.register_no = request.data.get('register_no') or member.register_no
        if member.user:
            member.user.first_name = request.data.get('first_name') or member.user.first_name
            member.user.last_name = request.data.get('last_name') or member.user.last_name
            member.user.email = member.email
            member.user.save()
        else:
            return Response({'error': 'User not found for this member'}, status=status.HTTP_404_NOT_FOUND)

        # Save the updated member
        member.save()

        return Response({'message': 'Member Updated successfully'}, status=status.HTTP_200_OK)


# Bulk import 

class BulkRegisterUsers(APIView):
    # permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]
    
    def post(self, request):
        group_name = request.data.get('group_name')
        if not group_name:
            return Response({'error': 'Member Type is Required'}, status=status.HTTP_400_BAD_REQUEST)

        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        excel_file = request.FILES['file']
        if not (excel_file.name.endswith('.xlsx') or excel_file.name.endswith('.xls')):
            return Response({'error': 'File is not Excel type'}, status=status.HTTP_400_BAD_REQUEST)

        # Read the Excel file
        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        created_users = []
        errors = []
        seen_emails = set()  # Set to track seen emails

        for index, row in df.iterrows():
            email = row.get('email')
            first_name = row.get('name') 
            if not email:
                errors.append({'error': 'Email is required', 'row': index + 1})
                continue

            # Check for duplicate emails
            if email in seen_emails or Member.objects.filter(email=email).exists():
                errors.append({'email': email, 'error': 'Duplicate email found', 'row': index + 1})
                continue  # Skip this row if the email is a duplicate
            seen_emails.add(email)

            # Check for required fields
            salutation = row.get('salutation')
            gender = row.get('gender')
            if not salutation:
                errors.append({'email': email, 'error': 'Salutation is required', 'row': index + 1})
                continue
            if not gender:
                errors.append({'email': email, 'error': 'Gender is required', 'row': index + 1})
                continue

            try:
                # Fetch the Salutation instance by name
                salutation_instance = Salutation.objects.get(salutation=salutation)

                # Gender validation (optional check depending on what you expect)
                if gender not in dict(Member.GENDER_CHOICES):
                    errors.append({'email': email, 'error': f'Invalid gender value: {gender}', 'row': index + 1})
                    continue

                # Optional fields (can be left blank or null)
                dob = row.get('dob', None)
                if isinstance(dob, float) and pd.isna(dob):
                    dob = None  # Convert NaN to None
                blood_group = row.get('blood_group', None)
                profile_picture = row.get('profile_picture', None)

                # Handle NaN (empty) profile_picture fields
                if isinstance(profile_picture, float) and pd.isna(profile_picture):
                    profile_picture = None  # Convert NaN to None

                mobile_no = row.get('mobile_no', None)

                # Handle department field (check if it's NaN)
                department_name = row.get('department', None)
                if isinstance(department_name, float) and pd.isna(department_name):
                    department_name = None  # Convert NaN to None

                # Check if `group_name` is 'Faculty' or 'Alumni' and handle fields accordingly
                if group_name == 'Faculty':
                    if department_name:
                        # Fetch department if exists
                        department = Department.objects.filter(short_name=department_name).first()
                        if not department:
                            errors.append({'email': email, 'error': f'Department "{department_name}" not found', 'row': index + 1})
                            continue
                    else:
                        department = None  # Allow department to be None

                    # Generate a random password for Faculty
                    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

                    # Create User with email as username
                    user = User.objects.create_user(
                        username=email,
                        password=password,
                        email=email,
                        first_name=first_name or ''
                    )

                    # Add the user to the Faculty group
                    faculty_group = Group.objects.get(name='Faculty')
                    user.groups.add(faculty_group)

                    # Create Member for Faculty
                    member = Member.objects.create(
                        user=user,
                        salutation=salutation_instance,
                        gender=gender,
                        dob=dob,
                        blood_group=blood_group,
                        mobile_no=mobile_no,
                        email=email,
                        department=department,
                        profile_picture=profile_picture,
                        is_approve=True,
                    )

                    # Send email with login credentials to Faculty
                    login_url = FRONTEND_URL.rstrip("/") + "/login"
                    email_subject = 'Your Faculty Account Details'

                    email_message = f'''
                    Dear {salutation} {email},

                    Welcome! Your faculty account has been successfully created. Below are your login credentials:

                    - **Username**: {user.username}
                    - **Password**: {password}

                    You can use these credentials to log in to the portal via the following link:

                    {login_url}

                    If you face any issues or need further assistance, please don't hesitate to reach out to us.

                    Best regards,
                    [Your Karpagam Collage of Pharmacy]
                    '''

                    send_mail(
                        subject=email_subject,
                        message=email_message,
                        from_email='your_email@example.com',
                        recipient_list=[user.email],
                    )

                    # Add created user to success list
                    created_users.append({'email': email, 'username': user.username})

                else:  # Alumni logic (group_name != 'Faculty')
                    # Batch and Course are required for Alumni
                    batch_name = row.get('batch')
                    course_name = row.get('course')
                    register_no = row.get('register_no')
                    
                    if not batch_name or not course_name:
                        errors.append({'email': email, 'error': 'Batch and Course are required for Alumni', 'row': index + 1})
                        continue
                    
                    batch = Batch.objects.filter(title=batch_name).first()
                    course = Course.objects.filter(title=course_name).first()

                    # Check if register_no is provided and if it already exists in the database
                    if register_no:
                        if Member.objects.filter(register_no=register_no).exists():
                            errors.append({'email': email, 'error': f'Duplicate register number: {register_no}', 'row': index + 1})
                            continue
                    else:
                        errors.append({'email': email, 'error': 'Register number is required for Alumni', 'row': index + 1})
                        continue
                    # Create Member for Alumni
                    member = Member.objects.create(
                        salutation=salutation_instance,
                        gender=gender,
                        dob=dob,
                        blood_group=blood_group,
                        mobile_no=mobile_no,
                        email=email,
                        batch=batch,
                        course=course,
                        register_no=register_no,
                        profile_picture=profile_picture,
                        is_approve=True,
                    )

                    # Send email with account details to Alumni
                    register_url = FRONTEND_URL.rstrip("/") + "/registration"
                    email_subject = 'Your Alumni Account Has Been Created'

                    email_message = f'''
                    Dear {salutation} {email},

                    We are pleased to inform you that your alumni account has been successfully created.

                    You are now part of our alumni network, and we look forward to staying connected with you!

                    You can register to the portal via the following link:

                    {register_url}

                    Best regards,
                    [Your Karpagam Collage of Pharmacy]
                    '''

                    send_mail(
                        subject=email_subject,
                        message=email_message,
                        from_email='your_email@example.com',
                        recipient_list=[email],
                    )

                    # Add created user to success list
                    created_users.append({'email': email, 'batch': batch_name, 'course': course_name})

            except (Salutation.DoesNotExist, Department.DoesNotExist, Batch.DoesNotExist, Course.DoesNotExist) as e:
                errors.append({'email': email, 'error': str(e), 'row': index + 1})
            except Exception as e:
                errors.append({'email': email, 'error': str(e), 'row': index + 1})

        if errors:
            response_data = {
                # 'message': 'Bulk user registration processed.',
                'created_users': created_users,  # List of successfully created users
                'errors': errors  # List of errors encountered
            }
            return Response(response_data, status=status.HTTP_207_MULTI_STATUS)
        else:
            if group_name == 'Faculty':
                return Response({
                    'message': 'All Faculties were created and mail sent successfully.',
                    # 'created_users': created_users  # List of successfully created users
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'message': 'All Alumnies were created and mail sent successfully.',
                    # 'created_users': created_users  # List of successfully created users
                }, status=status.HTTP_201_CREATED)


# Single register by manager

class SingleRegisterUser(APIView):
    def post(self, request):
        group_name = request.data.get('group_name')
        if not group_name:
            return Response({'error': 'Member Type is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Extract fields
        salutation_id = request.data.get('salutation_id')
        gender = request.data.get('gender')
        dob = request.data.get('dob', None)
        blood_group = request.data.get('blood_group', None)
        mobile_no = request.data.get('mobile_no', None)
        email = request.data.get('email')
        department_id = request.data.get('department_id', None)
        course_id = request.data.get('course_id', None)
        batch_id = request.data.get('batch_id', None)
        profile_picture = request.data.get('profile_picture', None)
        first_name= request.data.get('name', None),
        register_no = request.data.get('register_no')
        # Validate required fields
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        if Member.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Fetch the Salutation instance by ID
            salutation = None
            if salutation_id:
                try:
                    salutation = Salutation.objects.get(id=salutation_id)
                except Salutation.DoesNotExist:
                    return Response({'error': 'Salutation not found'}, status=status.HTTP_400_BAD_REQUEST)

            # Handle other fields and fetch related objects with proper error handling
            department = None
            if department_id:
                try:
                    department = Department.objects.get(id=department_id)
                except Department.DoesNotExist:
                    return Response({'error': 'Department not found'}, status=status.HTTP_400_BAD_REQUEST)

            course = None
            if course_id:
                try:
                    course = Course.objects.get(id=course_id)
                except Course.DoesNotExist:
                    return Response({'error': 'Course not found'}, status=status.HTTP_400_BAD_REQUEST)

            batch = None
            if batch_id:
                try:
                    batch = Batch.objects.get(id=batch_id)
                except Batch.DoesNotExist:
                    return Response({'error': 'Batch not found'}, status=status.HTTP_400_BAD_REQUEST)

            # Proceed with creating the Faculty or Alumni Member
            if group_name == 'Faculty':
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

                try:
                    user = User.objects.create_user(username=email, password=password, first_name=first_name,email=email)
                    faculty_group = Group.objects.get(name='Faculty')
                    user.groups.add(faculty_group)

                    member = Member.objects.create(
                        user=user,
                        salutation=salutation,
                        gender=gender,
                        dob=dob,
                        blood_group=blood_group,
                        mobile_no=mobile_no,
                        email=email,
                        department=department,
                        profile_picture=profile_picture,
                        is_approve=True,
                    )

                    # Send email with credentials
                    login_url= FRONTEND_URL.rstrip("/") + "/login"
                    email_subject = 'Your Faculty Account Details'
                    email_message = f'''
                    Dear {salutation} {email},

                    Welcome! Your faculty account has been successfully created. Below are your login credentials:

                    - **Username**: {user.username}
                    - **Password**: {password}

                    You can log in via the following link:

                    {login_url}
                    Best regards,
                    [Your Karpagam Collage of Pharmacy]
                    '''
                    send_mail(subject=email_subject, message=email_message, from_email='your_email@example.com', recipient_list=[user.email])
                    return Response({'message': 'Faculty user created and email sent with credentials.'}, status=status.HTTP_201_CREATED)

                except Exception as e:
                    return Response({'error': f"Error creating user: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

            else:  # Handle alumni registration
                member = Member.objects.create(
                    salutation=salutation,
                    gender=gender,
                    dob=dob,
                    blood_group=blood_group,
                    mobile_no=mobile_no,
                    email=email,
                    course=course,
                    batch=batch,
                    register_no=register_no,
                    profile_picture=profile_picture,
                    is_approve=True,
                )
                register_url= FRONTEND_URL.rstrip("/") + "/registration"
                email_subject = 'Your Alumni Account Has Been Created'
                email_message = f'''
                Dear {salutation} {email},

                We are pleased to inform you that your alumni account has been successfully created.

                You can register via the following link:

                {register_url}
                Best regards,
                [Your Karpagam Collage of Pharmacy]
                '''
                send_mail(subject=email_subject, message=email_message, from_email='your_email@example.com', recipient_list=[email])
                return Response({'message': 'Alumni member created and email sent.'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f"Unexpected error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)



# manage skills

class CreateSkill(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def post(self, request):
        skill = Skill(
            skill=request.data['skill'],
            description=request.data.get('description', '')  # Use get for optional fields
        )
        skill.save()
        return Response({"message": "Skill created successfully"}, status=status.HTTP_201_CREATED)

class RetrieveSkill(APIView):
    def get(self, request):
        skills = Skill.objects.all().order_by('-id')
        data = [
            {
                "skill_id": skill.id,
                "skill": skill.skill,
                "description": skill.description
            }
            for skill in skills
        ]
        return Response(data, status=status.HTTP_200_OK)

class UpdateSkill(APIView):
    permission_classes = [IsAuthenticated,IsAlumniManagerOrAdministrator]

    def get(self, request, skill_id):
        try:
            skill = Skill.objects.get(id=skill_id)
            data = {
                "skill": skill.skill,
                "description": skill.description
            }
            return Response(data, status=status.HTTP_200_OK)
        except Skill.DoesNotExist:
            return Response({"message": "Skill not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, skill_id):
        try:
            skill = Skill.objects.get(id=skill_id)
        except Skill.DoesNotExist:
            return Response({"message": "Skill not found"}, status=status.HTTP_404_NOT_FOUND)

        skill.skill = request.data["skill"]
        skill.description = request.data.get("description", skill.description)  # Update if provided
        skill.save()

        return Response({"message": "Skill updated successfully"}, status=status.HTTP_200_OK)

# profile picture
class ProfilePicture(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request,member_id):
        member = Member.objects.get(id=member_id)
        data = {
            "profile_picture": request.build_absolute_uri(member.profile_picture.url) if member.profile_picture else None

        }

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request,member_id):
        member = Member.objects.get(id=member_id)
        profile_picture = request.FILES.get('profile_picture')

        if not profile_picture:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the profile picture
        member.profile_picture = profile_picture
        member.save()
        activity = ActivityPoints.objects.get(name="Profile Picture")
        UserActivity.objects.create(
            user=request.user,
            activity=activity,
            details="Profile picture Added"
        )
        return Response({'message': 'Profile picture updated successfully'}, status=status.HTTP_200_OK)

    def delete(self, request,member_id):
        member = Member.objects.get(id=member_id)

        if member.profile_picture:
            member.profile_picture.delete(save=False)  # Delete the file from storage
            member.profile_picture = None
            member.save()
            return Response({'message': 'Profile picture deleted successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No profile picture to delete'}, status=status.HTTP_404_NOT_FOUND)

# basic profile
class MemberData(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,member_id):
        # member_id = request.data.get('member_id')
        
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        member_data = {
            'salutation': member.salutation.id,
            'first_name': member.user.first_name,
            'last_name': member.user.last_name,
            'email': member.email,
            'gender': member.gender,
            'dob': member.dob,
            'blood_group': member.blood_group,
            'mobile_no': member.mobile_no,
            'batch': member.batch.id,
            'course': member.course.id,
            'about_me': member.about_me,
        }
        
        return Response({'member_data': member_data}, status=status.HTTP_200_OK)
    def post(self, request,member_id):
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update member fields with the new data
        user= User.objects.get(email=member.email)
        
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        member.salutation_id = request.data.get('salutation')
        member.email = request.data.get('email')
        user.email = member.email
        member.gender = request.data.get('gender')
        member.dob = request.data.get('dob')
        member.blood_group = request.data.get('blood_group')
        member.batch_id = request.data.get('batch')
        member.course_id = request.data.get('course')
        member.about_me = request.data.get('about_me')
        member.mobile_no = request.data.get('mobile_no')

        user.save()
        # Save the updated member
        member.save()
        try:
            activity = ActivityPoints.objects.get(name="Basic Details")
        except ActivityPoints.DoesNotExist:
            return Response("Activity not found.")
        UserActivity.objects.create(
            user=request.user,
            activity=activity,
            details="Basic Details Added"
        )
        return Response({'message': 'Member Updated successfully'}, status=status.HTTP_200_OK)

# manage member skills
class CreateMemberSkill(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            member = Member.objects.get(id=request.data['member_id'])
            skill = Skill.objects.get(id=request.data['skill_id'])
            
            if Member_Skills.objects.filter(member=member, skill=skill).exists():
                return Response({"message": "Member already has this skill"}, status=status.HTTP_400_BAD_REQUEST)
            
            member_skill = Member_Skills(member=member, skill=skill)
            member_skill.save()
            try:
                activity = ActivityPoints.objects.get(name="Skill")
            except ActivityPoints.DoesNotExist:
                return Response("Activity not found.")
            UserActivity.objects.create(
                user=request.user,
                activity=activity,
                details=f"{skill.name} Added"
            )
            return Response({"message": "Member skill created successfully"}, status=status.HTTP_201_CREATED)
        except (Member.DoesNotExist, Skill.DoesNotExist):
            return Response({"message": "Member or Skill not found"}, status=status.HTTP_404_NOT_FOUND)

class RetrieveMemberSkills(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,member_id):
        member_skills = Member_Skills.objects.filter(member_id=member_id)
        data = [
            {
                "skill_id": member_skill.skill.id,
                "member_skill_id": member_skill.id,
                "skill_name":member_skill.skill.skill
            }
            for member_skill in member_skills
        ]
        return Response(data, status=status.HTTP_200_OK)

class UpdateMemberSkill(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, member_skill_id):
        try:
            member_skill = Member_Skills.objects.get(id=member_skill_id)
            member = Member.objects.get(id=request.data['member_id'])
            skill = Skill.objects.get(id=request.data['skill_id'])

            member_skill.member = member
            member_skill.skill = skill
            member_skill.save()

            return Response({"message": "Member skill updated successfully"}, status=status.HTTP_200_OK)
        except Member_Skills.DoesNotExist:
            return Response({"message": "Member skill not found"}, status=status.HTTP_404_NOT_FOUND)
        except (Member.DoesNotExist, Skill.DoesNotExist):
            return Response({"message": "Member or Skill not found"}, status=status.HTTP_404_NOT_FOUND)

class DeleteMemberSkill(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, member_skill_id):
        try:
            member_skill = Member_Skills.objects.get(id=member_skill_id)
            member_skill.delete()
            return Response({"message": "Member skill deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Member_Skills.DoesNotExist:
            return Response({"message": "Member skill not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
# manage member education
class CreateMemberEducation(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MemberEducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            member_education = serializer
            degree = member_education.validated_data.get('degree')
            institute = member_education.validated_data.get('institute')
            try:
                activity = ActivityPoints.objects.get(name="Education")
            except ActivityPoints.DoesNotExist:
                return Response("Activity not found.")
            UserActivity.objects.create(
                user=request.user,
                activity=activity,
                details=f"{degree} and {institute.title} Added"
            )
            return Response({"message": "Member education created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrieveMemberEducation(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, member_id):
        education_records = Member_Education.objects.filter(member_id=member_id)
        data = []

        for record in education_records:
            data.append({
                'id': record.id,
                'institute': record.institute.title,  # Assuming institute has a 'name' field
                'degree': record.degree,
                'start_year': record.start_year,
                'end_year': record.end_year,
                'is_currently_pursuing': record.is_currently_pursuing,
                'location': record.location.location if record.location else None  # Assuming location has a 'name' field
            })

        return Response(data, status=status.HTTP_200_OK)

class UpdateMemberEducation(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, education_id):
        try:
            education_record = Member_Education.objects.get(id=education_id)
            serializer = MemberEducationSerializer(education_record)  # No many=True since it's a single instance
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Member_Education.DoesNotExist:
            return Response({"message": "Member education not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request, education_id):
        try:
            education = Member_Education.objects.get(id=education_id)
            serializer = MemberEducationSerializer(instance=education, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Member education updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Member_Education.DoesNotExist:
            return Response({"message": "Member education not found"}, status=status.HTTP_404_NOT_FOUND)

class DeleteMemberEducation(APIView):
    # permission_classes = [IsAuthenticated]

    def delete(self, request, education_id):
        try:
            education = Member_Education.objects.get(id=education_id)
            education.delete()
            return Response({"message": "Member education deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Member_Education.DoesNotExist:
            return Response({"message": "Member education not found"}, status=status.HTTP_404_NOT_FOUND)

# manage member experience
class CreateMemberExperience(APIView):
    permission_classes = [IsAuthenticated]  # Uncomment if you want authentication

    def post(self, request):
        serializer = MemberExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            member_experience = serializer
            industry = member_experience.validated_data.get('degree')
            role = member_experience.validated_data.get('institute')
            try:
                activity = ActivityPoints.objects.get(name="Experience")
            except ActivityPoints.DoesNotExist:
                return Response("Activity not found.")
            UserActivity.objects.create(
                user=request.user,
                activity=activity,
                details=f"{industry.title} and {role.role} Added"
            )
            return Response({"message": "Member experience created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveMemberExperience(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, member_id):
        experience_records = Member_Experience.objects.filter(member_id=member_id)

        # Convert the queryset to a list of dictionaries
        experience_list = [
            {
                'id': exp.id,
                'industry': exp.industry.title,  
                'role': exp.role.role if exp.role else None,  
                'start_date': exp.start_date,
                'end_date': exp.end_date,
                'is_currently_working': exp.is_currently_working,
                'location': exp.location.location  
            }
            for exp in experience_records
        ]

        return Response(experience_list, status=status.HTTP_200_OK)

class UpdateMemberExperience(APIView):
    permission_classes = [IsAuthenticated]  # Uncomment if you want authentication
    def get(self, request, experience_id):
        try:
            experience_record = Member_Experience.objects.get(id=experience_id)
            serializer = MemberExperienceSerializer(experience_record)  # Remove many=True
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Member_Experience.DoesNotExist:
            return Response({"message": "Member experience not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request, experience_id):
        try:
            experience = Member_Experience.objects.get(id=experience_id)
            serializer = MemberExperienceSerializer(instance=experience, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Member experience updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Member_Experience.DoesNotExist:
            return Response({"message": "Member experience not found"}, status=status.HTTP_404_NOT_FOUND)


class DeleteMemberExperience(APIView):
    permission_classes = [IsAuthenticated]  
    def delete(self, request, experience_id):
        try:
            experience = Member_Experience.objects.get(id=experience_id)
            experience.delete()
            return Response({"message": "Member experience deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Member_Experience.DoesNotExist:
            return Response({"message": "Member experience not found"}, status=status.HTTP_404_NOT_FOUND)

# member milestone


# contact details for alumni
class CreateAlumni(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AlumniSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Alumni contacts created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrieveAlumni(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, member_id):
        try:
            alumni_record = Alumni.objects.get(member_id=member_id)  # Use get() here
            serializer = AlumniSerializer(alumni_record)  # No need for many=True since it's a single object
            member = Member.objects.get(id=member_id)
            if member is not None:
                profile_picture_check = bool(member.profile_picture)

                # Module 2: Check if Skills and Education are populated
                skills_check = Member_Skills.objects.filter(member=member).exists() and all(
                    skill.member is not None for skill in Member_Skills.objects.filter(member=member)
                )

                education_check = Member_Education.objects.filter(member=member).exists() and all(
                    edu.member for edu in Member_Education.objects.filter(member=member)
                )
                
                # If both Skills and Education are valid, set module2_check to True
                module2_check = skills_check and education_check

                # Module 3: Check if Experience is valid (not null)
                experience_check = Member_Experience.objects.filter(member=member).exists() and all(
                    exp.member is not None  for exp in Member_Experience.objects.filter(member=member)
                )

                # Module 4: Check if Alumni is valid (not null)
                alumni_check = Alumni.objects.filter(member=member).exists() and all(
                    alum.member for alum in Alumni.objects.filter(member=member)
                )

                # Creating a dictionary for module checks
                modules = {
                    'module1': profile_picture_check,  # True if profile photo exists
                    'module2': module2_check,        # True if skills and education are valid
                    'module3': experience_check,     # True if experience is valid
                    'module4': alumni_check,         # True if alumni information is valid
                }

            else:
                # Member does not exist, return tokens and user info without module checks
                modules = {}
            return Response({'modules': modules, 'data': serializer.data}, status=status.HTTP_200_OK)
        except Alumni.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Alumni.MultipleObjectsReturned:
            return Response({"detail": "Multiple records found."}, status=status.HTTP_400_BAD_REQUEST)

class UpdateAlumni(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, member_id):
        try:
            alumni = Alumni.objects.get(member_id=member_id)
            serializer = AlumniSerializer(instance=alumni, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Alumni updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Alumni.DoesNotExist:
            return Response({"message": "Alumni record not found"}, status=status.HTTP_404_NOT_FOUND)
        


# profile status


class ProfileCompletionStatus(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, member_id):
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)

        # Profile Picture
        profile_picture_complete = bool(member.profile_picture)  # 10%
        
        # Basic Profile Completion (5 fields)
        basic_fields = [
            member.salutation,
            member.gender,
            member.dob,
            member.email,
            member.mobile_no,
        ]
        basic_complete = all(basic_fields)  # Complete if all fields are filled
        
        # Skills Completion
        skills_complete = Member_Skills.objects.filter(member=member).exists()  # 10%

        # Education Completion
        education_complete = Member_Education.objects.filter(member=member).exists()  # 10%

        # Experience Completion
        experience_complete = Member_Experience.objects.filter(member=member).exists()  # 10%

        # Alumni Completion
        alumni_complete = False
        if Alumni.objects.filter(member=member).exists():
            alumni = Alumni.objects.get(member=member)
            alumni_complete = all([alumni.address, alumni.postal_code])  # Both fields required for 10%

        milestone = Member_Milestone.objects.filter(member=member).exists()
        # Calculate overall completion status
        completion_percentage = 0

        # Add up completion based on the criteria
        completion_percentage += 10 if profile_picture_complete else 0  # Profile Picture
        completion_percentage += 10 if basic_complete else 0  # Basic Profile
        completion_percentage += 10 if skills_complete else 0  # Skills
        completion_percentage += 10 if education_complete else 0  # Education
        completion_percentage += 10 if experience_complete else 0  # Experience
        completion_percentage += 10 if alumni_complete else 0  # Alumni
        completion_percentage += 10 if milestone else 0  # Milestone

        # Normalize to a total of 100%
        completion_percentage = min(completion_percentage, 100)

        # Determine status
        status = "Incomplete"
        if completion_percentage == 100:
            status = "Complete"
        elif completion_percentage >= 50:
            status = "Partially Complete"

        return Response({
            'completion_percentage': completion_percentage,
            'status': status
        })

# list all members
class MemberListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        members = Member.objects.all().order_by('-id')
        response_data = []
        for member in members:
            alumni_data = None
            if member.alumni.exists():
                alumni = member.alumni.first()
                alumni_data = {
                    'website': alumni.website,
                    'linked_in': alumni.linked_in,
                    'twitter_handle': alumni.twitter_handle,
                }
            full_name = f"{member.user.first_name} {member.user.last_name}" if member.user else None
            member_data = {
                'id': member.id,
                'name': full_name,
                'email': member.email,
                'batch': member.batch.title if member.batch else None,
                'course': member.course.title if member.course else None,
                'profile_picture': request.build_absolute_uri(member.profile_picture.url) if member.profile_picture else None,
                'alumni': alumni_data,
            }
            response_data.append(member_data)

        return Response(response_data, status=status.HTTP_200_OK)
    
# get latest member
class LatestMembers(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        members = Member.objects.all().order_by('-id')[:10]
        response_data = []
        for member in members:
            alumni_data = None
            if member.alumni.exists():
                alumni = member.alumni.first()
                alumni_data = {
                    'website': alumni.website,
                    'linked_in': alumni.linked_in,
                    'twitter_handle': alumni.twitter_handle,
                }
            full_name = f"{member.user.first_name} {member.user.last_name}" if member.user else None
            member_data = {
                'id': member.id,
                'name': full_name,
                'email': member.email,
                'batch': member.batch.title if member.batch else None,
                'course': member.course.title if member.course else None,
                'profile_picture': request.build_absolute_uri(member.profile_picture.url) if member.profile_picture else None,
                'alumni': alumni_data,
            }
            response_data.append(member_data)

        return Response(response_data, status=status.HTTP_200_OK)
        



# main filter
class MemberFilterView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Extract data from request
        batch = request.data.get('batch', None)
        role = request.data.get('role', None)
        course = request.data.get('course', None)
        department = request.data.get('department', None)
        industry = request.data.get('industry', None)
        skill = request.data.get('skill', None)
        institution = request.data.get('institution', None)
        location = request.data.get('location', None)
        first_name = request.data.get('first_name', None)
        email = request.data.get('email', None)
        dob = request.data.get('dob', None)
        registered = request.data.get('registered', None)  # New filter for registration status
        member_type = request.data.get('member_type', None)  # New member_type filter
        # Create a dictionary for the filter arguments using Q objects
        filters = Q()  # Start with an empty Q object

        # Filter based on registration status
        if registered not in [None, ""]:
            if registered:  # If registered is true, filter for members with a user
                filters &= Q(user__isnull=False)
            else:  # If registered is false, filter for members without a user
                filters &= Q(user__isnull=True)

        # Filter by member_type (check user's group)
        if member_type not in [None, ""]:
            filters &= Q(user__groups__name=member_type)  # Assuming member_type matches a group name

        # Filters based on batch, role, course, department, etc.
        if batch not in [None, ""]:
            filters &= Q(batch__id=batch)
        if role not in [None, ""]:
            filters &= Q(experience__role__id=role)
        if course not in [None, ""]:
            filters &= Q(course__id=course)
        
        if industry not in [None, ""]:
            filters &= Q(experience__industry__id=industry)
        if skill not in [None, ""]:
            filters &= Q(skills__skill__id=skill)
        if institution not in [None, ""]:
            filters &= Q(education__institute__id=institution)
        if location not in [None, ""]:
            filters &= Q(experience__location__id=location) | Q(education__location__id=location)

        # Additional filters for personal details
        if first_name:
            filters &= Q(user__first_name__icontains=first_name)
        if email:
            filters &= Q(email__icontains=email)
        if dob not in [None, ""]:
            # Validate the date format for dob
            try:
                # dob = datetime.strptime(dob, "%Y-%m-%d").date()  # Ensure dob is in 'YYYY-MM-DD' format
                filters &= Q(dob=dob)
            except ValueError:
                return Response({"error": "Invalid date format for DOB. Use 'YYYY-MM-DD'."}, status=status.HTTP_400_BAD_REQUEST)
        
        if member_type == 'Faculty' and department not in [None, ""]:
            filters &= Q(department__id=department)
        elif department not in [None, ""]:  # If not faculty, filter by department associated with the course
            filters &= Q(course__department__id=department)
        # Apply the filters to the Member queryset with prefetch_related to optimize DB queries
        queryset = Member.objects.prefetch_related(
            'skills', 'education', 'experience', 'alumni', 
            'experience__industry', 'experience__role'
        ).filter(filters)

        # Serialize the filtered data
        response_data = []
        for member in queryset:
            # Fetch alumni data if it exists
            alumni_data = None
            if member.alumni.exists():
                alumni = member.alumni.first()
                alumni_data = {
                    'website': alumni.website,
                    'linked_in': alumni.linked_in,
                    'twitter_handle': alumni.twitter_handle,
                    'address': alumni.address,
                    'location': alumni.location.location if alumni.location else None,
                    'postal_code': alumni.postal_code,
                }

            # Construct member data
            full_name = f"{member.user.first_name} {member.user.last_name}" if member.user else None
            member_data = {
                'id': member.id,
                'name': full_name,
                'email': member.email,
                'batch': member.batch.title if member.batch else None,
                'course': member.course.title if member.course else None,
                'profile_picture': request.build_absolute_uri(member.profile_picture.url) if member.profile_picture else None,
                'alumni': alumni_data,
            }

            response_data.append(member_data)

        return Response(response_data, status=status.HTTP_200_OK)

# detail in member
class MemberDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, member_id):
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
        full_name = f"{member.user.first_name} {member.user.last_name}" if member.user else None
        # Manually construct the response data
        member_data = {
            'name': full_name,
            'register_no': member.register_no,
            'email': member.email or None,
            'gender': member.gender or None,
            'dob': member.dob or None,
            'blood_group': member.blood_group or None,
            'mobile_no': member.mobile_no or None,
            'profile_picture': request.build_absolute_uri(member.profile_picture.url) if member.profile_picture else None,
            'about_me': member.about_me or None,
            'salutation': member.salutation.salutation if member.salutation else None,
            'batch': member.batch.title if member.batch else None,
            'course': member.course.title if member.course else None,
            'skills': [skill.skill.skill for skill in member.skills.all()] if member.skills.exists() else None,
            'education': [
                {
                    'institute': edu.institute.title if edu.institute else None,
                    'degree': edu.degree or None,
                    'start_year': edu.start_year or None,
                    'end_year': edu.end_year or None,
                    'is_currently_pursuing': edu.is_currently_pursuing or None,
                    'location': edu.location.location if edu.location else None
                }
                for edu in member.education.all()
            ] or None,
            'experiences': [
                {
                    'industry': exp.industry.title if exp.industry else None,
                    'role': exp.role.role if exp.role else None,
                    'start_date': exp.start_date or None,
                    'end_date': exp.end_date or None,
                    'is_currently_working': exp.is_currently_working or None,
                    'location': exp.location.location if exp.location else None
                }
                for exp in member.experience.all()
            ] or None,
            'alumni': (
                {
                    'website': member.alumni.first().website if member.alumni.exists() else None,
                    'linked_in': member.alumni.first().linked_in if member.alumni.exists() else None,
                    'twitter_handle': member.alumni.first().twitter_handle if member.alumni.exists() else None,
                    'address': member.alumni.first().address if member.alumni.exists() else None,
                    'postal_code': member.alumni.first().postal_code if member.alumni.exists() else None,
                    'registered_on': member.alumni.first().registered_on if member.alumni.exists() else None,
                    'location': member.alumni.first().location.location if member.alumni.exists() and member.alumni.first().location else None
                }
                if member.alumni.exists() else None
            )
        }

        return Response(member_data, status=status.HTTP_200_OK)

class TotalPointsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user_activities = UserActivity.objects.filter(user=request.user)
        total_points = user_activities.aggregate(total_points=Sum('activity__points'))['total_points']
        
        if total_points is None:
            total_points = 0
            
        activity_details = [
            {
                'activity_name': user_activity.activity.name,
                'points': user_activity.activity.points,
                'details': user_activity.details,
                'date_time': user_activity.date_time
            }
            for user_activity in user_activities
        ]
        
        return Response({
            "total_points": total_points,
            "activity_details": activity_details
        })