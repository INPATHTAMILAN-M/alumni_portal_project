from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Chapter, ChapterMembership
from ..serializers import ChapterSerializer, ChapterMembershipSerializer
from ..filters.chapter_filters import ChapterFilter
from ..permissions import IsAlumniManagerOrAdministrator


class ChapterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Chapters to be viewed or edited.
    """
    queryset = Chapter.objects.all().order_by('-created_at')
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter] 
    filterset_class = ChapterFilter
    search_fields = ['name', 'description', 'city__city_name', 'state__state_name', 'country__country_name', 'chapter_type']
    ordering_fields = ['name', 'created_at']

class ChapterMembershipViewSet(viewsets.ModelViewSet):
    queryset = ChapterMembership.objects.all().order_by('-joined_at')
    serializer_class = ChapterMembershipSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['chapter', 'user', 'chapter__location']
    search_fields = ['chapter__name', 'user__email', 'user__first_name', 'user__last_name']
    ordering_fields = ['joined_at']

    def create(self, request, *args, **kwargs):
        user_ids = request.data.get('user_ids', [])
        chapter_id = request.data.get('chapter_id')

        if not isinstance(user_ids, list):
            return Response({"error": "user_ids must be a list."}, status=status.HTTP_400_BAD_REQUEST)

        if not chapter_id:
            return Response({"error": "chapter_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        memberships = []
        for user_id in user_ids:
            data = {'user_id': user_id, 'chapter_id': chapter_id}
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            memberships.append(serializer.data)

        return Response(memberships, status=status.HTTP_201_CREATED)