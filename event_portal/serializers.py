from rest_framework import serializers
from .models import *

class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question', 'help_text', 'options', 'is_faq', 'is_recommended']

    def validate_question(self, value):
        """
        Ensure the question is unique to avoid duplication.
        """
        if Question.objects.filter(question=value).exists():
            raise serializers.ValidationError("A question with this text already exists.")
        return value
    
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question', 'help_text', 'options', 'is_faq','is_recommended']
        
class EventQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()  

    class Meta:
        model = EventQuestion
        fields = ['question']
        
class EventSerializer(serializers.ModelSerializer):
    event_wallpaper = serializers.ImageField(required=False)
    event_question = EventQuestionSerializer(many=True, read_only=True)  

    class Meta:
        model = Event
        fields = ['id','title', 'category', 'start_date', 'start_time', 'venue', 'address', 'link', 'is_public',
                  'need_registration', 'registration_close_date', 'description', 'event_wallpaper', 'instructions',
                  'posted_by', 'event_question']

class EventUpdateSerializer(serializers.ModelSerializer):
    event_wallpaper = serializers.ImageField(required=False)
    event_question = EventQuestionSerializer(many=True, read_only=True)  

    class Meta:
        model = Event
        fields = ['id','title', 'category', 'start_date', 'start_time', 'venue', 'address', 'link', 'is_public',
                  'need_registration', 'registration_close_date', 'description', 'event_wallpaper', 'instructions',
                  'posted_by', 'event_question']
    # def get_event_wallpaper(self, obj):
    #     request = self.context.get('request')
    #     if obj.event_wallpaper:
    #         return request.build_absolute_uri(obj.event_wallpaper.url)
    #     return None  

class EventRetrieveSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', read_only=True)
    category_id = serializers.CharField(source='category.id', read_only=True)
    posted_by = serializers.CharField(source='posted_by.get_full_name', read_only=True)
    event_wallpaper = serializers.SerializerMethodField()
    event_question = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = [
            'id','title','category_id', 'category', 'start_date', 'start_time', 'venue', 'address', 'link', 'is_public',
            'need_registration', 'registration_close_date', 'description', 'event_wallpaper', 'instructions',
            'posted_by', 'event_question','is_active', 'is_owner', 'is_admin'
        ]

    def get_is_owner(self, obj):
        """
        Check if the user making the request is the owner of the album.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            if obj.posted_by == user:
                return True
            if user.groups.filter(name__in=['Administrator', 'Alumni_Manager']).exists():
                return True
        return False
    
    def get_is_admin(self, obj):

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            if user.groups.filter(name__in=['Administrator', 'Alumni_Manager']).exists():
                return True
        return False
    
    def get_event_wallpaper(self, obj):
        request = self.context.get('request')
        if obj.event_wallpaper:
            return request.build_absolute_uri(obj.event_wallpaper.url)
        return None

    def get_event_question(self, obj):
        """
        Custom method to serialize related EventQuestion and Question data.
        """
        event_questions = EventQuestion.objects.filter(event=obj)
        event_question_data = []

        for event_question in event_questions:
            
            question = event_question.question
            question_data = {
                
                'id': question.id,
                'question': question.question,
                'options': question.options,
                'help_text': question.help_text,
                'is_faq': question.is_faq
            }
            event_question_data.append(question_data)

        return event_question_data

class EventActiveRetrieveSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', read_only=True)
    posted_by = serializers.CharField(source='posted_by.get_full_name', read_only=True)
    event_wallpaper = serializers.SerializerMethodField()
    event_question = serializers.SerializerMethodField()
    is_registered = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = [
            'id','title', 'category', 'start_date', 'start_time', 'venue', 'address', 'link', 'is_public',
            'need_registration', 'registration_close_date', 'description', 'event_wallpaper', 'instructions',
            'posted_by', 'event_question','is_active', 'is_registered','is_owner','is_admin'
        ]

    def get_is_owner(self, obj):
        """
        Check if the user making the request is the owner of the album.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            if obj.posted_by == user:
                return True
            if user.groups.filter(name__in=['Administrator', 'Alumni_Manager']).exists():
                return True
        return False
    
    def get_is_admin(self, obj):

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            if user.groups.filter(name__in=['Administrator', 'Alumni_Manager']).exists():
                return True
        return False
    
    def get_is_registered(self, obj):
        """
        Check if the user is registered for the event.
        """
        request = self.context.get('request')
        user = request.user
        return EventRegistration.objects.filter(event=obj, user=user).exists()
    
    def get_event_wallpaper(self, obj):
        request = self.context.get('request')
        if obj.event_wallpaper:
            return request.build_absolute_uri(obj.event_wallpaper.url)
        return None

    def get_event_question(self, obj):
        """
        Custom method to serialize related EventQuestion and Question data.
        """
        event_questions = EventQuestion.objects.filter(event=obj)
        event_question_data = []

        for event_question in event_questions:
            question = event_question.question
            options_list = question.options.split(',') if question.options else []
            options_data = [{"option": option.strip()} for option in options_list]

            question_data = {
                'id': question.id,
                'question': question.question,
                'options': options_data,
                'help_text': question.help_text,
                'is_faq': question.is_faq
            }
            event_question_data.append(question_data)

        return event_question_data

class EventExportQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()  # Nesting the QuestionSerializer

    class Meta:
        model = EventQuestion
        fields = ['id', 'event', 'question']

class EventRegistrationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Assuming 'user' is a ForeignKey to the User model
    event = serializers.StringRelatedField()  # You can also use EventSerializer if you need more fields

    class Meta:
        model = EventRegistration
        fields = ['id', 'event', 'user', 'applied_on']

class RegistrationResponseSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()  # Nesting the QuestionSerializer
    # registered_event = EventRegistrationSerializer()  # Nesting the EventRegistrationSerializer

    class Meta:
        model = RegistrationResponse
        fields = ['id', 'question', 'response']

class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ['id', 'title']
            
class EventExportSerializer(serializers.ModelSerializer):
    category = EventCategorySerializer()  # Nested EventCategorySerializer
    event_questions = EventExportQuestionSerializer(many=True, source='eventquestion_set')  # Correct reverse relation
    registrations = EventRegistrationSerializer(many=True, source='eventregistration_set')  # Correct reverse relation

    # SerializerMethodField to get registration responses manually
    registration_responses = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'category', 'start_date', 'start_time', 'venue', 'address', 'link',
            'is_public', 'need_registration', 'registration_close_date', 'description',
            'event_wallpaper', 'instructions', 'posted_on', 'posted_by', 'is_active',
            'event_questions', 'registrations', 'registration_responses'
        ]

    def get_registration_responses(self, obj):
        # Get all registration responses related to this event
        responses = []
        for registration in obj.eventregistration_set.all():
            # For each event registration, get the related registration responses
            responses.extend(registration.registrationresponse_set.all())
        return RegistrationResponseSerializer(responses, many=True).data