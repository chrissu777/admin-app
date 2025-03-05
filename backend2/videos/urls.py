from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import RecordingViewSet
router = routers.DefaultRouter()

router.register(r'recordings', RecordingViewSet)

urlpatterns= [
    path('', include(router.urls))
]