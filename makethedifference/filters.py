import django_filters
from .models import *
from django_filters import DateFilter, CharFilter


class AllEventsFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='start_date')
    description = CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Event
        fields = ['start_date', 'tag', 'description']


class AllCausesFilter(django_filters.FilterSet):
    description = CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Cause
        fields = ['description', 'tags']

