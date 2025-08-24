from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import SchoolViewSet, current_user

router = routers.DefaultRouter()
router.register(r'Schools', SchoolViewSet)

urlpatterns= [
    path('', include(router.urls)),
    path('current-user/', current_user, name='current-user'),
]