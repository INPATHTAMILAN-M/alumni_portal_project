from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from account.filters.members_milestone_filters import MemberMilestoneFilter
from ..models import Member_Milestone
from ..serializers import (
    MemberMilestoneCreateSerializer,
    MemberMilestoneListSerializer,
    MemberMilestoneUpdateSerializer,
    MemberMilestoneRetrieveSerializer
)

class MemberMilestoneViewSet(viewsets.ModelViewSet):
    queryset = Member_Milestone.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = MemberMilestoneFilter
    
    def get_serializer_class(self):
        """
        Determine the serializer class based on the action being performed.
        """
        if self.action == 'create':
            return MemberMilestoneCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return MemberMilestoneUpdateSerializer
        elif self.action == 'retrieve':
            return MemberMilestoneRetrieveSerializer
        elif self.action == 'list':
            return MemberMilestoneListSerializer
        return MemberMilestoneListSerializer  # Default serializer (used in list or retrieve actions)

