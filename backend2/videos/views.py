from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from .models import Recording
from .serializers import RecordingSerializer
import boto3
import aws_encryption_sdk

from rest_framework.response import Response
class RecordingViewSet(viewsets.ModelViewSet):
    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        recording = self.get_object()
        s3_client = boto3.client('s3', region_name='us-east-1')

        
        presigned_url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': 'weaponwatch-demo',
                'Key': recording.s3_filepath,
            },
            ExpiresIn=3600,
        )
        return Response({'download_url': presigned_url})


