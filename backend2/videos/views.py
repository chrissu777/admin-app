from django.shortcuts import render
from rest_framework import permissions, viewsets
from .models import Recording
from .serializers import RecordingSerializer

class RecordingViewSet(viewsets.ModelViewSet):
    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer