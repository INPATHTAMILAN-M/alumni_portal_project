from django.db import models
from django.contrib.auth.models import User,Group
from django.utils import timezone
import datetime

class Salutation(models.Model):
    salutation = models.CharField(max_length=10, null=False)
    description = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return self.salutation

class Social_Media(models.Model):
    title = models.CharField(max_length=55, null=False)
    icon = models.ImageField(upload_to='icons/')
    url = models.URLField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Batch(models.Model):
    title = models.CharField(max_length=55, null=False)
    start_year = models.IntegerField(null=False)
    end_year = models.IntegerField(null=False)

    def __str__(self):
        return self.title

class Department(models.Model):
    short_name = models.CharField(max_length=55, null=False)
    full_name = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name

class Course(models.Model):

    GRADUATE_CHOICES = [
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
    ]

    title = models.CharField(max_length=255, null=False)
    graduate = models.CharField(max_length=55, choices=GRADUATE_CHOICES, null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Institution(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

class Industry(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    website = models.URLField(max_length=255)

    def __str__(self):
        return self.title

class Location(models.Model):
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.location

class Skill(models.Model):
    skill = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.skill

class Role(models.Model):
    role = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.role

class Industry_Type(models.Model):
    type_name = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.type_name

class Country(models.Model):
    country_name = models.CharField(max_length=50, null=False)
    country_code = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.country_name

class Member(models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A_POSITIVE', 'A+'),
        ('A_NEGATIVE', 'A-'),
        ('B_POSITIVE', 'B+'),
        ('B_NEGATIVE', 'B-'),
        ('AB_POSITIVE', 'AB+'),
        ('AB_NEGATIVE', 'AB-'),
        ('O_POSITIVE', 'O+'),
        ('O_NEGATIVE', 'O-'),
    ]
    
    salutation = models.ForeignKey(Salutation, on_delete=models.CASCADE, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=11, choices=BLOOD_GROUP_CHOICES,null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE,null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    mobile_no = models.CharField(max_length=25,null=True, blank=True)
    email = models.EmailField(null=False)
    file = models.FileField(upload_to='proofs/',null=True, blank=True)
    register_no = models.CharField(max_length=25, null=True, blank=True)
    is_approve = models.BooleanField(default=False)
    otp_verified = models.BooleanField(default=False)
    
    def __str__(self):
        # If user is not null and has groups
        if self.user:
            group_names = ', '.join([group.name for group in self.user.groups.all()])
            return f'{self.email} | {self.batch} | {self.course} | {group_names}'
        else:
            return f'{self.email} | {self.batch} | {self.course}'

class OTP(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_expired(self):
        return timezone.now() > self.created_at + datetime.timedelta(minutes=5)

class Member_Skills(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.member} - {self.skill}'

class Member_Education(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='education')
    institute = models.ForeignKey(Institution, on_delete=models.CASCADE)
    degree = models.CharField(max_length=255)
    start_year = models.IntegerField()
    end_year = models.IntegerField(null=True, blank=True)
    is_currently_pursuing = models.BooleanField(default=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.member} - {self.degree}'

class Member_Experience(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='experience', null=False)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, null=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_currently_working = models.BooleanField(default=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.member} - {self.industry}'

class Member_Milestone(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    year = models.IntegerField()

    def __str__(self):
        return f'{self.member} - {self.title}'
    
class Alumni(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='alumni')
    website = models.URLField(blank=True)
    linked_in = models.URLField(blank=True)
    twitter_handle = models.CharField(max_length=225, blank=True)
    address = models.TextField(blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    registered_on = models.DateField(null=True,blank=True)

    def __str__(self):
        return f'{self.member} - Alumni'

class ActivityPoints(models.Model):
    name = models.CharField(max_length=255)
    points = models.IntegerField() 
    details = models.TextField(null=True,blank=True)

    def __str__(self):
        return f'{self.name} - {self.points}'

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(ActivityPoints, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    details = models.TextField()

    def __str__(self):
        return f'{self.user.username} - {self.activity.name} - {self.activity.points}'
