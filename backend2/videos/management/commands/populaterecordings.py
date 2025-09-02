from django.core.management.base import BaseCommand
from videos.models import Recording
from accounts.models import School
import boto3
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetches recording data from S3 and populates DB.'

    def handle(self, *args, **options):
        client = boto3.client('s3')
        bucket_name = 'weaponwatch-demo'
        response = client.list_objects_v2(Bucket=bucket_name)
        bucket_content = response.get('Contents', [])

        if not bucket_content:
            all_recordings_count = Recording.objects.count()
            if all_recordings_count > 0:
                Recording.objects.all().delete()
                self.stdout.write(f"Bucket empty - deleted all {all_recordings_count} recordings")
            else:
                self.stdout.write("Bucket empty or no content found")
            return

        s3_keys = set()
        
        for bucket_item in bucket_content:
            
            s3_key = bucket_item['Key'] # UMD*163286*0EOTah3Irg2N8MRshq2a*Camera 1*20250902_004430.mp4
            # NAMING CONVENTION SCHOOL*NCESID*CAMID*CAMNAME*TIMESTAMP
            s3_keys.add(s3_key)
            item_details = s3_key.split('*') # ['school', 'nces_id', 'cam_id', 'cam_name', 'timestamp.mp4']
            
            if len(item_details) < 5:
                self.stdout.write(f"Skipping invalid S3 key format: {s3_key}")
                continue
                
            school_name = item_details[0]
            ncesid = item_details[1]
            cam_id = item_details[2]
            cam_name = item_details[3]
            timestamp_with_ext = item_details[4]
            
            # Extract timestamp from filename (remove .mp4 extension)
            timestamp_str = timestamp_with_ext.rsplit('.', 1)[0]
            
            # Parse timestamp (format: YYYYMMDD_HHMMSS)
            try:
                recording_timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
            except ValueError:
                self.stdout.write(f"Invalid timestamp format in {s3_key}: {timestamp_str}")
                continue

            last_modified = bucket_item['LastModified'] # DateTime object (upload time)

            try:
                school_model = School.objects.get(nces_id=ncesid)
            except School.DoesNotExist:
                school_model = School.objects.create(
                    name=school_name.replace('_', ' '),
                    nces_id=ncesid
                )
                self.stdout.write(f"Created school: {school_model.name} (NCES: {ncesid})")
            
            if not Recording.objects.filter(s3_filepath=s3_key).exists():
                Recording.objects.create(
                    s3_filepath = s3_key,
                    rec_date = last_modified,
                    timestamp = recording_timestamp,
                    cam_id = cam_id,
                    camera_name = cam_name,
                    school = school_model
                )

        if s3_keys:
            deleted_recordings = Recording.objects.exclude(s3_filepath__in=s3_keys)
            deleted_count = deleted_recordings.count()
            if deleted_count > 0:
                deleted_recordings.delete()
                self.stdout.write(f"Deleted {deleted_count} recordings that no longer exist in S3")
        else:
            all_recordings_count = Recording.objects.count()
            if all_recordings_count > 0:
                Recording.objects.all().delete()
                self.stdout.write(f"Deleted all {all_recordings_count} recordings (S3 bucket is empty)")

        
