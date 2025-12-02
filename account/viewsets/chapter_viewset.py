from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Chapter, ChapterMembership
from ..serializers import ChapterSerializer, ChapterMembershipSerializer
from ..permissions import IsAlumniManagerOrAdministrator


class ChapterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Chapters to be viewed or edited.
    """
    queryset = Chapter.objects.all().order_by('-created_at')
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated, IsAlumniManagerOrAdministrator]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city', 'state', 'country']
    search_fields = ['name', 'description', 'city', 'state', 'country']
    ordering_fields = ['name', 'created_at']

class ChapterMembershipViewSet(viewsets.ModelViewSet):
    queryset = ChapterMembership.objects.all().order_by('-joined_at')
    serializer_class = ChapterMembershipSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['chapter', 'user']
    search_fields = ['chapter__name', 'user__email', 'user__first_name', 'user__last_name']
    ordering_fields = ['joined_at']