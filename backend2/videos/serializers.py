from rest_framework import serializers
from .models import Recording

class RecordingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recording
        fields = ['s3_filepath', 'rec_date','school']