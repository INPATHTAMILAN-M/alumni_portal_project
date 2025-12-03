import django_filters
from ..models import Chapter


class ChapterFilter(django_filters.FilterSet):
    """
    Custom filter for the Chapter model.
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')

    class Meta:
        model = Chapter
        fields = ['name', 'description', 'chapter_type', 'city', 'state', 'country', 'location', 'start_date', 'end_date']