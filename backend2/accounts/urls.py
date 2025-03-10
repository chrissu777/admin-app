from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import SchoolViewSet
router = routers.DefaultRouter()

router.register(r'Schools', SchoolViewSet)

urlpatterns= [
    path('', include(router.urls))
]