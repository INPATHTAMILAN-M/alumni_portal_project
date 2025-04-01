from django_filters.rest_framework import FilterSet
from django_filters import filters
from ..models import Member_Milestone

class MemberMilestoneFilter(FilterSet):
    year = filters.NumberFilter(field_name='year', lookup_expr='exact')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    member = filters.NumberFilter(field_name='member__id', lookup_expr='exact')

    class Meta:
        model = Member_Milestone
        fields = ['year', 'title', 'member']
