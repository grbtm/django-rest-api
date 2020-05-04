from app.models import Entry
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView

from .filters import EntryFilter
from .serializers import EntrySerializer


class EntryListAPIView(ListAPIView):
    serializer_class = EntrySerializer
    queryset = Entry.objects.extend_with_derived_metric()

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = EntryFilter
