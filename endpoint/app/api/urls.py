from django.urls import path

from .views import EntryListAPIView

urlpatterns = [
    path('api/endpoint', EntryListAPIView.as_view())
]
