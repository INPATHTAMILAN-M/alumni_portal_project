import datetime
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from account.models import Member
from media_portal.models import Post, PostCategory
from account.permissions import *
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist
import openpyxl
from django.http import HttpResponse
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

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
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        paginated_categories = paginator.paginate_queryset(event_categories, request)
        data = [
            {
                "category_id": event_category.id,
                "title": event_category.title,
            }
            for event_category in paginated_categories
        ]
        return paginator.get_paginated_response(data)

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
                        options=question_data.get('options', ''),
                        is_faq=question_data.get('is_faq', False)
                    )

                # Create EventQuestion linking event and question
                EventQuestion.objects.create(event=event, question=question)
            Post.objects.create(
                title=event.title,
                event=event,
                published=True,
                visible_to_public=event.is_public,
                posted_by=event.posted_by,
                post_category=PostCategory.objects.get(name='Event'),  # Assuming you have a category named 'Memories'
            )
            return Response({
                "message": "Event created successfully",
            }, status=status.HTTP_201_CREATED)

        return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrieveEvent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Event.objects.all().order_by('-posted_on')
        paginator = PageNumberPagination()
        paginator.page_size = 12  # Set the number of items per page
        paginated_events = paginator.paginate_queryset(events, request)
        serializer = EventRetrieveSerializer(paginated_events, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

class MyRetrieveEvent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        event_category_id = request.query_params.get('event_category_id')
        is_active = request.query_params.get('is_active')
        is_upcoming = request.query_params.get('is_upcoming', 'false').lower() == 'true'
        is_completed = request.query_params.get('is_completed', 'false').lower() == 'true'
        today = timezone.now().date()

        events = Event.objects.filter(posted_by=request.user)

        if event_category_id:
            events = events.filter(category=event_category_id)
        if is_active is not None:
            events = events.filter(is_active=is_active.lower() == 'true')
        if is_upcoming:
            events = events.filter(start_date__gte=today)
        if is_completed:
            events = events.filter(start_date__lt=today)

        events = events.order_by('-posted_on')
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        paginated_events = paginator.paginate_queryset(events, request)
        serializer = EventRetrieveSerializer(paginated_events, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
    
class UpdateEvent(APIView):
    # permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request,event_id):
        events = Event.objects.get(id=event_id)  # Fetch all events
        serializer = EventRetrieveSerializer(events, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # def patch(self, request, event_id):
    #     try:
    #         event = Event.objects.get(id=event_id, posted_by=request.user)
    #     except Event.DoesNotExist:
    #         return Response({"error": "Event not found or permission denied."}, status=status.HTTP_404_NOT_FOUND)

    #     # Copy request data for serializer use
    #     event_data = request.data.copy()
    #     event_data['posted_by'] = request.user.id

    #     # Parse event_question from form-data (stringified JSON)
    #     try:
    #         event_questions_raw = request.data.get('event_question', '[]')
    #         event_questions = json.loads(event_questions_raw)
    #     except json.JSONDecodeError:
    #         return Response({"error": "Invalid format for event_question"}, status=status.HTTP_400_BAD_REQUEST)

    #     # Prepare serializer with partial update
    #     event_serializer = EventUpdateSerializer(event, data=event_data, partial=True)

    #     if event_serializer.is_valid():
    #         event_serializer.save()

    #         # Clean up old event-question links
    #         related_question_ids = list(EventQuestion.objects.filter(event=event).values_list('question_id', flat=True))
    #         EventQuestion.objects.filter(event=event).delete()
    #         Question.objects.filter(id__in=related_question_ids, is_recommended=False).delete()

    #         for question_data in event_questions:
    #             if not isinstance(question_data, dict):
    #                 return Response({"error": "Each question must be a dictionary with proper fields."}, status=status.HTTP_400_BAD_REQUEST)

    #             question = None
    #             question_text = question_data.get('question', '').strip()

    #             if question_text:
    #                 try:
    #                     question = Question.objects.get(question=question_text)
    #                 except ObjectDoesNotExist:
    #                     question = Question.objects.create(
    #                         question=question_text,
    #                         help_text=question_data.get('help_text', ''),
    #                         options=question_data.get('option', ''),
    #                         is_faq=question_data.get('is_faq', False),
    #                     )

    #             if question:
    #                 EventQuestion.objects.create(event=event, question=question)
    #             else:
    #                 return Response({"error": "A valid question is required."}, status=status.HTTP_400_BAD_REQUEST)

    #         return Response({"message": "Event updated successfully"}, status=status.HTTP_200_OK)

    #     return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        # Parse event_question from form-data (stringified JSON)
        try:
            event_questions_raw = request.data.get('event_question', '[]')
            event_questions = json.loads(event_questions_raw)
        except json.JSONDecodeError:
            return Response({"error": "Invalid format for event_question"}, status=status.HTTP_400_BAD_REQUEST)

        event_serializer = EventUpdateSerializer(event, data=request.data, partial=True)

        if event_serializer.is_valid():
            event_serializer.save(posted_by=request.user)  # Inject posted_by here if needed

            # Clean up old questions
            related_question_ids = list(EventQuestion.objects.filter(event=event).values_list('question_id', flat=True))
            EventQuestion.objects.filter(event=event).delete()
            Question.objects.filter(id__in=related_question_ids, is_recommended=False).delete()

            for question_data in event_questions:
                if not isinstance(question_data, dict):
                    return Response({"error": "Each question must be a dictionary."}, status=status.HTTP_400_BAD_REQUEST)

                question_text = question_data.get('question', '').strip()
                if not question_text:
                    continue

                question, _ = Question.objects.get_or_create(
                    question=question_text,
                    defaults={
                        'help_text': question_data.get('help_text', ''),
                        'options': question_data.get('option', ''),
                        'is_faq': question_data.get('is_faq', False)
                    }
                )
                EventQuestion.objects.create(event=event, question=question)

            return Response({"message": "Event updated successfully"}, status=status.HTTP_200_OK)

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
        events = Event.objects.filter(is_active=True).order_by('-posted_on')
        paginator = PageNumberPagination()
        paginator.page_size = 12  # Set the number of items per page
        paginated_events = paginator.paginate_queryset(events, request)
        serializer = EventActiveRetrieveSerializer(paginated_events, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

class DetailEvent(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,event_id):
            try:
                event = Event.objects.get(id=event_id)
                serializer = EventActiveRetrieveSerializer(event, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Event.DoesNotExist:
                return Response({"message": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
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
        category_id = request.query_params.get('category_id')
        today = timezone.now().date()
        is_past = request.query_params.get('is_past', 'false').lower() == 'true'

        if category_id:
            if is_past:
                events = Event.objects.filter(
                    category_id=category_id,
                    is_active=True,
                    start_date__lt=today
                ).order_by('-posted_on')
            else:
                events = Event.objects.filter(
                    category_id=category_id,
                    is_active=True,
                    start_date__gte=today
                ).order_by('-posted_on')
        else:
            if is_past:
                events = Event.objects.filter(
                    is_active=True,
                    start_date__lt=today
                ).order_by('-posted_on')
            else:
                events = Event.objects.filter(
                    is_active=True,
                    start_date__gte=today
                ).order_by('-posted_on')

        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        paginated_events = paginator.paginate_queryset(events, request)
        serializer = EventRetrieveSerializer(paginated_events, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

# manage question
# Create question
class QuestionCreateView(APIView):
    def post(self, request):
        serializer = QuestionCreateSerializer(data=request.data)
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
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        paginated_questions = paginator.paginate_queryset(questions, request)
        serializer = QuestionSerializer(paginated_questions, many=True)
        return paginator.get_paginated_response(serializer.data)

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
    # permission_classes = [IsAuthenticated]  # Ensure that the user is authenticated
    def get(self, request, event_id):
        # Get the event object
        event = get_object_or_404(Event, id=event_id)

        # Get all EventQuestion objects related to the event
        event_questions = EventQuestion.objects.filter(event=event)
        
          # Format the questions and their details
        questions_data = []
        for event_question in event_questions:
            question = event_question.question  # Access the Question object related to the EventQuestion
            
            # Split the options into a list (if options exist and are comma-separated)
            options_list = question.options.split(',') if question.options else []

            # Convert options into a list of dictionaries with 'name' as the key
            options_dict_list = [{"name": option.strip()} for option in options_list]
            
            question_data = {
                "id": question.id,
                "question": question.question,
                "help_text": question.help_text,
                "options": options_dict_list,  # Use the new structure
                "is_faq": question.is_faq
            }
            questions_data.append(question_data)

        return Response(questions_data, status=status.HTTP_200_OK)


    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)

        # Check if the user is already registered
        if EventRegistration.objects.filter(event=event, user=request.user).exists():
            return Response({"error": "You are already registered for this event."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the registration
        event_registration = EventRegistration.objects.create(
            event=event,
            user=request.user
        )
        # if request.data.get('responses') is None:
        #     return Response({"error": "Responses are required."}, status=status.HTTP_400_BAD_REQUEST)
        responses_data = request.data.get('responses', [])
        invalid_question_ids = []

        for response_data in responses_data:
            question_id = response_data.get('question_id')
            response_text = response_data.get('response')

            if not question_id :
                return Response({"error": "Question ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Ensure the question is linked to this event
            try:
                question = Question.objects.get(id=question_id)
                # question = event_question.question
            except Question.DoesNotExist:
                invalid_question_ids.append(question_id)
                continue

            RegistrationResponse.objects.create(
                registered_event=event_registration,
                question=question,
                response=response_text
            )

        if invalid_question_ids:
            return Response({
                "message": "Registered with some warnings.",
                "invalid_question_ids": invalid_question_ids
            }, status=status.HTTP_201_CREATED)

        return Response({
            "message": "Successfully registered for the event."
        }, status=status.HTTP_201_CREATED)

class RetrieveRegisteredEvent(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        registrations = EventRegistration.objects.filter(event=event)
        
        if not registrations.exists():
            return Response({"error": "No registrations found for this event."}, status=status.HTTP_404_NOT_FOUND)
        
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        paginated_registrations = paginator.paginate_queryset(registrations, request)
        
        all_registered_users = []
        
        for registration in paginated_registrations:
            user_data = {
                "member_id": registration.user.member.id if hasattr(registration.user, 'member') else None,
                "profile_picture": request.build_absolute_uri(registration.user.member.profile_picture.url) if hasattr(registration.user, 'member') and registration.user.member.profile_picture else None,
                "full_name": registration.user.get_full_name(),
                "email": registration.user.email,
                "registration_date": registration.applied_on,
                "responses": []
            }
            responses = RegistrationResponse.objects.filter(registered_event=registration)
            for response in responses:
                user_data["responses"].append({
                    "question": response.question.question,
                    "response": response.response
                })
            all_registered_users.append(user_data)
        
        return paginator.get_paginated_response({
            "event_id": event.id,
            "event_title": event.title,
            "registered_users": all_registered_users
        })


class EmailAttendees(APIView):
    # permission_classes = [IsAuthenticated]
    
    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        registrations = EventRegistration.objects.filter(event=event)
        
        all_registered_users = []
        
        for registration in registrations:
            user_data = {              
                "full_name": registration.user.get_full_name(),
                "email": registration.user.email,
            }
            
            all_registered_users.append(user_data)
        
        return Response({
            "event_id": event.id,
            "event_title": event.title,
            "venue": event.venue,
            "date": event.start_date,
            "time": event.start_time,
            "registered_users": all_registered_users
        }, status=status.HTTP_200_OK)
        
    # def post(self, request, event_id):
    #     event = get_object_or_404(Event, id=event_id)
    #     registrations = EventRegistration.objects.filter(event=event)
        
    #     if not registrations.exists():
    #         return Response({"error": "No registrations found for this event."}, status=status.HTTP_404_NOT_FOUND)

    #     subject = request.data.get('subject')
    #     name_check = request.data.get('name_checkbox', 'false').lower() == 'true'
    #     message = request.data.get('message')
    #     file = request.FILES.get('file', None)
        
        
    #     recipient_emails = [registration.user.email for registration in registrations]
        
    #     if not subject or not message:
    #         return Response({"error": "Subject and message are required."}, status=status.HTTP_400_BAD_REQUEST)
        

    #     email = EmailMessage(
    #         subject=subject, 
    #         body=message,     
    #         from_email=settings.DEFAULT_FROM_EMAIL,  
    #         to=recipient_emails,  
    #     )


    #     if file:
    #         email.attach(file.name, file.read(), file.content_type)

    #     try:
    #         email.send()
    #         return Response({"status": "Email sent successfully!"}, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({"status": "Failed to send email", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        registrations = EventRegistration.objects.filter(event=event)
        
        if not registrations.exists():
            return Response({"error": "No registrations found for this event."}, status=status.HTTP_404_NOT_FOUND)

        subject = request.data.get('subject')
        name_check = request.data.get('name_checkbox', 'false').lower() == 'true'
        message = request.data.get('message')
        file = request.FILES.get('file', None)
        
        if not subject:
            return Response({"error": "Subject is required."}, status=status.HTTP_400_BAD_REQUEST)

        for registration in registrations:
            recipient_name = registration.user.get_full_name() if name_check else "Alumni"
            
            # Prepare context for the template
            context = {
                'name_check': name_check,
                'subject': subject,
                'message': message,
                'recipient_name': recipient_name,
                'event_title': event.title,
                'event_date': event.start_date.strftime("%A, %d %b %Y"),
                'event_time': event.start_time.strftime("%I:%M %p"),
                'event_venue': event.venue,
                'event_link': f"http://alumni.decodeschool.com/",
                'contact_person': "Admin",
                'contact_id': "Admin@gmail.com"
            }
            
            # Render HTML content
            html_content = render_to_string('email_template.html', context)
            
            # Create email
            email = EmailMultiAlternatives(
                subject=subject,
                body=message,  # This will be the fallback for text-only clients
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[registration.user.email],
            )
            email.attach_alternative(html_content, "text/html")
            
            if file:
                email.attach(file.name, file.read(), file.content_type)

            try:
                email.send()
            except Exception as e:
                # Log error but continue with other emails
                print(f"Failed to send email to {registration.user.email}: {str(e)}")

        return Response({"status": "Emails sent successfully!"}, status=status.HTTP_200_OK)
    
class TestEmail(APIView):
    # permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            recipient_email = request.data.get('recipient_email')
        except KeyError:
            return Response({"error": "Recipient email is required."}, status=status.HTTP_400_BAD_REQUEST)
        subject = 'Testing Email'
        message = 'This is a test email.'
        name_check = 'false'
        context = {
            'name_check': name_check,
            'subject': subject,
            'message': message,
            'recipient_name': recipient_email,
            'event_link': f"http://alumni.decodeschool.com/",
            'contact_person': "Admin",
            'contact_id': "Admin@gmail.com"
        }
        
        # Render HTML content
        html_content = render_to_string('email_template.html', context)
        
        # Create email
        email = EmailMultiAlternatives(
            subject=subject,
            body=message,  # This will be the fallback for text-only clients
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email],
        )
        email.attach_alternative(html_content, "text/html")
        try:
            email.send()
            return Response({"status": "Email sent successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "Failed to send email", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmailSelectedMembers(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Retrieve member_ids from form-data (as a string)
        member_ids_str = request.data.get('member_ids', '')

        # If member_ids is not empty, process it
        if member_ids_str:
            try:
                # Split the string into a list and convert to integers
                member_ids = [int(id.strip()) for id in member_ids_str.split(',')]
            except ValueError:
                return Response({"error": "Invalid member IDs format. Please provide a list of integers."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "No member IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the members based on the provided IDs
        members = Member.objects.filter(id__in=member_ids)

        if not members.exists():
            return Response({"error": "No members found with the provided IDs."}, status=status.HTTP_404_NOT_FOUND)

        # Get the subject and message from the request
        subject = request.data.get('subject')
        message = request.data.get('message')
        file = request.FILES.get('file', None)

        # Ensure subject and message are provided
        if not subject or not message:
            return Response({"error": "Subject and message are required."}, status=status.HTTP_400_BAD_REQUEST)

        responses = []

        # Loop through the members and send email to each one
        for member in members:
            recipient_email = member.email if member else None

            if recipient_email:
                # Create the email message
                email = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[recipient_email],
                )

                # Attach file if provided
                if file:
                    email.attach(file.name, file.read(), file.content_type)

                try:
                    # Send email
                    email.send()
                    responses.append({"status": f"Email sent successfully to {recipient_email}."})
                except Exception as e:
                    responses.append({"status": f"Failed to send email to {recipient_email}", "error": str(e)})
            else:
                responses.append({"status": f"No email found for member {member.id}."})

        return Response(responses, status=status.HTTP_200_OK)


# export event data
class ExportEvent(APIView):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EventExportSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)