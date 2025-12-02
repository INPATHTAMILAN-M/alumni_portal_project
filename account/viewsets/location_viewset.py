from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Country, State, City
from ..serializers import CountrySerializer, StateSerializer, CitySerializer
from ..permissions import IsAlumniManagerOrAdministrator


class CountryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Countries to be viewed or edited.
    """
    queryset = Country.objects.all().order_by('country_name')
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated, IsAlumniManagerOrAdministrator]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country_name', 'currency_active']
    search_fields = ['country_name', 'country_code']
    ordering_fields = ['country_name']

class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all().order_by('state_name')
    serializer_class = StateSerializer
    permission_classes = [IsAuthenticated, IsAlumniManagerOrAdministrator]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['country']
    search_fields = ['state_name']

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all().order_by('city_name')
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated, IsAlumniManagerOrAdministrator]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['state']
    search_fields = ['city_name']