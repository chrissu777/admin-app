from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import School, Profile
from .serializers import SchoolSerializer

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class=SchoolSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Get current authenticated user information"""
    user = request.user
    try:
        profile = user.profile
        return Response({
            'uid': user.username,  # Firebase UID stored as username
            'email': user.email,
            'profile': {
                'role': profile.role,
                'school': profile.school.name if profile.school else None,
                'jurisdiction': [school.name for school in profile.jursidction.all()]
            }
        })
    except Profile.DoesNotExist:
        return Response({
            'uid': user.username,
            'email': user.email,
            'profile': None
        })