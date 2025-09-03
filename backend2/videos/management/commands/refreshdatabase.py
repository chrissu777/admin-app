from django.core.management.base import BaseCommand
from videos.models import Recording
from accounts.models import School
import boto3
from datetime import datetime
from django.utils import timezone

class Command(BaseCommand):
    help = 'Refreshes the database by clearing all existing data and repopulating from S3'

    def handle(self, *args, **options):
        # Clear existing data
        Recording.objects.all().delete()
        School.objects.all().delete()
        
        # Fetch from S3
        client = boto3.client('s3')
        bucket_name = 'weaponwatch-demo'
        response = client.list_objects_v2(Bucket=bucket_name)
        bucket_content = response.get('Contents', [])
        
        for bucket_item in bucket_content:
            s3_key = bucket_item['Key']
            item_details = s3_key.split('*')
            
            if len(item_details) < 5:
                continue
            
            school_name = item_details[0]
            ncesid = item_details[1]
            cam_id = item_details[2]
            cam_name = item_details[3]
            timestamp_with_ext = item_details[4]
            
            # Extract timestamp from filename
            timestamp_str = timestamp_with_ext.rsplit('.', 1)[0]
            
            # Parse timestamp
            try:
                recording_timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                recording_timestamp = timezone.make_aware(recording_timestamp)
            except ValueError:
                continue
            
            last_modified = bucket_item['LastModified']
            
            # Get or create school
            school_model, created = School.objects.get_or_create(
                nces_id=ncesid,
                defaults={'name': school_name.replace('_', ' ')}
            )
            
            # Create recording
            Recording.objects.create(
                s3_filepath=s3_key,
                rec_date=last_modified,
                timestamp=recording_timestamp,
                cam_id=cam_id,
                camera_name=cam_name,
                school=school_model
            )