import datetime
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import *
from account.permissions import *
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist
import openpyxl
from django.http import HttpResponse
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser
import json

# manage category
class CreateEventCategory(APIView):
    # permission_classes = [IsAuthenticated, IsAlumniManagerOrAdministrator]

    def post(self, request):
        event_category = EventCategory(
            title=request.data['category'],
        )
        event_category.save()

        return Response({"message": "Event category created successfully"}, status=status.HTTP_201_CREATED)

class RetrieveEventCategory(APIView):
    def get(self, request):
        event_categories = EventCategory.objects.all().order_by('-id')
        data = [
            {
                "category_id": event_category.id,
                "title": event_category.title,
            }
            for event_category in event_categories
        ]
        return Response(data, status=status.HTTP_200_OK)

class UpdateEventCategory(APIView):
    def post(self, request, category_id):  # 'post' should be lowercase
        try:
            event_category = EventCategory.objects.get(id=category_id)
            event_category.title = request.data.get('category', event_category.title)
            event_category.save()
            return Response({"message": "Event category updated successfully"}, status=status.HTTP_200_OK)
        except EventCategory.DoesNotExist:
            return Response({"error": "Event category not found"}, status=status.HTTP_404_NOT_FOUND)

#---------------------------------------------------- manage Event

class CreateEvent(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        # Copy incoming request data
        event_data = request.data.copy()
        event_data['posted_by'] = request.user.id

        # Serialize the event data
        event_serializer = EventSerializer(data=event_data)

        if event_serializer.is_valid():
            # Save the event instance
            event = event_serializer.save()

            # Get event_questions and parse it as JSON
            event_questions = request.data.get('event_question', '[]')  # Default to empty list if not provided
            try:
                event_questions = json.loads(event_questions)
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON format in event_question."}, status=status.HTTP_400_BAD_REQUEST)

            # Process each question in event_questions
            for question_data in event_questions:
                question = None
                if 'question' in question_data:
                    try:
                        # Check if the question already exists
                        question = Question.objects.get(question=question_data['question'])
                    except ObjectDoesNotExist:
                        pass

                if not question:
                    # Create new question if not found
                    question = Question.objects.create(
                        question=question_data.get('question', ''),
                        help_text=question_data.get('help_text', ''),
                        options=question_data.get('option', ''),
                        is_faq=question_data.get('is_faq', False)
                    )

                # Create EventQuestion linking event and question
                EventQuestion.objects.create(event=event, question=question)

            return Response({
                "message": "Event created successfully",
            }, status=status.HTTP_201_CREATED)

        return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrieveEvent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Event.objects.all().order_by('-id')
        serializer = EventRetrieveSerializer(events, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class MyRetrieveEvent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Event.objects.filter(posted_by=request.user).order_by('-id')
        serializer = EventRetrieveSerializer(events, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UpdateEvent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,event_id):
        events = Event.objects.get(id=event_id)  # Fetch all events
        serializer = EventRetrieveSerializer(events, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id, posted_by=request.user)
        except Event.DoesNotExist:
            return Response({"error": "Event not found or you do not have permission to edit it."},
                            status=status.HTTP_404_NOT_FOUND)

        event_data = request.data.copy()
        event_data['posted_by'] = request.user.id  

        event_serializer = EventSerializer(event, data=event_data, partial=True)

        if event_serializer.is_valid():
            event_serializer.save()

            event_questions = request.data.get('event_question', [])

            EventQuestion.objects.filter(event=event).delete()

            EventQuestion.objects.filter(
                event=event, 
                question__is_recommended=False
            ).delete()

            for question_data in event_questions:
                question = None
                if 'question' in question_data:
                    try:
                        question = Question.objects.get(question=question_data['question'])
                    except ObjectDoesNotExist:
                        question = Question.objects.create(
                            question=question_data.get('question', ''),
                            help_text=question_data.get('help_text', ''),
                            options=question_data.get('options', ''),
                            is_faq=question_data.get('is_faq', False),
                            is_recommended=question_data.get('is_recommended', False)
                        )

                EventQuestion.objects.create(event=event, question=question)

            return Response({
                "message": "Event updated successfully",
            }, status=status.HTTP_200_OK)

        return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# deactivate event
class DeactivateEvent(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request, event_id):
        try:
            event = Event.objects.get(id=event_id)
            event.is_active = request.data.get('is_active')
            event.save()
            if event.is_active:
                return Response({"message": "Event activated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Event deactivated successfully"}, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({"message": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

# active Event

class ActiveEvent(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        events = Event.objects.filter(is_active=True).order_by('-id')
        serializer = EventActiveRetrieveSerializer(events, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# retrieve question
class RecommendedQuestions(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        questions = Question.objects.filter(is_recommended=True)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Event by category
class EventByCategory(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        category_id = request.data.get('category_id')
        
        today = timezone.now().date()  
        
        if category_id:
            events = Event.objects.filter(
                category_id=category_id,
                is_active=True,
                start_date__gte=today 
            ).order_by('-id')
        else:
            events = Event.objects.filter(
                is_active=True,
                start_date__gte=today  
            ).order_by('-id')
        
        serializer = EventRetrieveSerializer(events, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class PastEventByCategory(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        category_id = request.data.get('category_id')
        today = timezone.now().date()  
        if category_id:
            events = Event.objects.filter(
                category_id=category_id,
                is_active=True,
                start_date__lt=today 
            ).order_by('-id')
        else:
            events = Event.objects.filter(
                is_active=True,
                start_date__lt=today  
            ).order_by('-id')
        serializer = EventRetrieveSerializer(events, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

# manage question
# Create question
class QuestionCreateView(APIView):
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve question (single)
class QuestionRetrieveView(APIView):
    def get(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuestionSerializer(question)
        return Response(serializer.data)

# Retrieve question 
class QuestionListView(APIView):
    def get(self, request):
        questions = Question.objects.all().order_by('-id')
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

# Update question
class QuestionUpdateView(APIView):
    def put(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# delete question

class DeleteQuestion(APIView):
    def delete(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
            question.delete()
            return Response({"message": "Question deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)
        
# make recommended question

class MakeRecommendedQuestion(APIView):
    def post(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
            question.is_recommended = request.data.get('is_recommended')
            question.save()
            return Response({"message": "Question Updated successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)
        
# delete event questions

class EventQuestionDelete(APIView):
    
    def delete(self, request, event_question_id):
        try:
            event_question = EventQuestion.objects.get(id=event_question_id)
            event_question.delete()
            return Response({"message": "EventQuestion deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except EventQuestion.DoesNotExist:
            return Response({"error": "EventQuestion not found"}, status=status.HTTP_404_NOT_FOUND)
        
# register event
class RegisterEvent(APIView):
    permission_classes = [IsAuthenticated]  # Ensure that the user is authenticated
    
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        
        if EventRegistration.objects.filter(event=event, user=request.user).exists():
            return Response({"error": "You are already registered for this event."}, status=status.HTTP_400_BAD_REQUEST)

        event_registration = EventRegistration.objects.create(
            event=event,
            user=request.user
        )

        responses_data = request.data.get('responses', [])
        
        if responses_data:
            for response_data in responses_data:
                question_id = response_data.get('question_id')
                response = response_data.get('response')
                
                try:
                    question = Question.objects.get(id=question_id)
                except Question.DoesNotExist:
                    return Response({"error": "Question not found."}, status=status.HTTP_404_NOT_FOUND)

                RegistrationResponse.objects.create(
                    registered_event=event_registration,
                    question=question,
                    response=response
                )

        return Response({
            "message": "Successfully registered for the event."
        }, status=status.HTTP_201_CREATED)

class RetrieveRegisteredEvent(APIView):
    # permission_classes = [IsAuthenticated]
    
    def get(self, request, event_id):
        # Retrieve the specific event
        event = get_object_or_404(Event, id=event_id)
        
        # Fetch all registrations for the event
        registrations = EventRegistration.objects.filter(event=event)
        
        if not registrations.exists():
            return Response({"error": "No registrations found for this event."}, status=status.HTTP_404_NOT_FOUND)
        
        all_registered_users = []
        
        # For each registration, get the user and their responses
        for registration in registrations:
            user_data = {
                "member_id": registration.user.member.id if registration.user.member else None,  
                "email": registration.user.email,
                "registration_date": registration.applied_on,
                "responses": []
            }

            # Fetch all responses for this event registration
            responses = RegistrationResponse.objects.filter(registered_event=registration)
            for response in responses:
                user_data["responses"].append({
                    "question": response.question.question,
                    "response": response.response
                })
            
            all_registered_users.append(user_data)
        
        return Response({
            "event_id": event.id,
            "event_title": event.title,
            "registered_users": all_registered_users
        }, status=status.HTTP_200_OK)

# export event data
class ExportEvent(APIView):
    """
    API view to export event data including event details, questions, registrations, and responses.
    """
    
    def get(self, request, event_id):
        # Fetch the event object, or return a 404 error if it doesn't exist
        event = get_object_or_404(Event, id=event_id)

        # Create a new workbook and set the sheet name
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = f"Event {event.title}"

        # Define headers for event details and questions
        headers = [
            'Event Title', 'Category', 'Start Date', 'Start Time', 'Venue',
            'Address', 'Link', 'Is Public', 'Need Registration', 'Registration Close Date',
            'Description', 'Event Wallpaper', 'Instructions', 'Posted By',
            'Question', 'Options', 'Help Text', 'Is FAQ', 'Username', 'Applied On', 'Responses'
        ]
        sheet.append(headers)

        # Fetch all registrations for this event
        event_registrations = EventRegistration.objects.filter(event=event)
        
        for registration in event_registrations:
            # Fetch the responses for each registration
            responses = RegistrationResponse.objects.filter(registered_event=registration)

            # Collect the response data for each registration
            response_data = {response.question.question: response.response for response in responses}
            
            # Loop through the questions for the event
            event_questions = EventQuestion.objects.filter(event=event)
            
            for event_question in event_questions:
                question = event_question.question  # Access the Question object via EventQuestion
                options = question.options  # Access 'options' from the related Question model
                help_text = question.help_text
                is_faq = question.is_faq
                question_response = response_data.get(question.question, 'No Response')

                # Create a row with the event details and the question/response details
                row = [
                    event.title,  # Event Title
                    event.category.title,  # Category
                    event.start_date,  # Start Date
                    event.start_time,  # Start Time
                    event.venue,  # Venue
                    event.address,  # Address
                    event.link,  # Link
                    event.is_public,  # Is Public
                    event.need_registration,  # Need Registration
                    event.registration_close_date,  # Registration Close Date
                    event.description,  # Description
                    event.event_wallpaper.url if event.event_wallpaper else 'No Wallpaper',  # Event Wallpaper
                    event.instructions,  # Instructions
                    event.posted_by.get_full_name(),  # Posted By
                    question.question,  # Question
                    options,  # Options (from Question model)
                    help_text,  # Help Text (from Question model)
                    is_faq,  # Is FAQ (from Question model)
                    registration.user.username,  # Username
                    registration.applied_on,  # Applied On
                    f"{question.question}: {question_response}"  # Responses
                ]
                sheet.append(row)

        # Create an HTTP response with the Excel file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=event_{event.id}_data.xlsx'
        workbook.save(response)
        
        return response
