from rest_framework import serializers
from .models import School, Profile

class SchoolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = School
        fields = ['name', 'nces_id']