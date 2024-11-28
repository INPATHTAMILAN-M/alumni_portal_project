import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import *
from account.permissions import *
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist

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
        event_categories = EventCategory.objects.all()
        data = [
            {
                "category_id": event_category.id,
                "title": event_category.title,
            }
            for event_category in event_categories
        ]
        return Response(data, status=status.HTTP_200_OK)

class UpdateEventCategory(APIView):
    def Post(self, request, category_id):
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

    def post(self, request):
        event_data = request.data.copy()
        event_data['posted_by'] = request.user.id  
        
        event_serializer = EventSerializer(data=event_data)
        
        if event_serializer.is_valid():
            event = event_serializer.save()  

            event_questions = request.data.get('event_question', [])

            for question_data in event_questions:
                question = None
                if 'question' in question_data:
                    try:
                        question = Question.objects.get(question=question_data['question'])
                    except ObjectDoesNotExist:
                        pass
                
                if not question:
                    question = Question.objects.create(
                        question=question_data.get('question', ''),
                        help_text=question_data.get('help_text', ''),
                        options=question_data.get('option', ''),
                        is_faq=question_data.get('is_faq', False)
                    )
                
                EventQuestion.objects.create(event=event, question=question)

            return Response({
                "message": "Event created successfully",
            }, status=status.HTTP_201_CREATED)
        
        return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrieveEvent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Event.objects.all()  # Fetch all events
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
        events = Event.objects.filter(is_active=True)
        serializer = EventRetrieveSerializer(events, many=True, context={'request': request})
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
    def get(self, request, category_id):
        events = Event.objects.filter(category_id=category_id)
        serializer = EventRetrieveSerializer(events, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

# delete question

class DeleteQuestion(APIView):
    def delete(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
            question.delete()
            return Response({"message": "Question deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
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