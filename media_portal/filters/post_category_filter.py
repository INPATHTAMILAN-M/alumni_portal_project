import django_filters
from ..models import PostCategory  # Assuming your model is named PostCategory

class PostCategoryFilterSet(django_filters.FilterSet):
    for_create = django_filters.BooleanFilter(method='filter_for_create')

    class Meta:
        model = PostCategory
        fields = ['for_create']

    def filter_for_create(self, queryset, name, value):
        if value:
            exclude_names = ['Event', 'Job', 'Memories', 'Internship']
            return queryset.exclude(name__in=exclude_names)
        return queryset
