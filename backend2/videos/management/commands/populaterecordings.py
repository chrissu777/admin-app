from django.core.management.base import BaseCommand
from videos.models import Recording
from accounts.models import School
import boto3

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
            
            s3_key = bucket_item['Key'] # object naming convention: schoolname*nces_id
            s3_keys.add(s3_key)
            item_details = s3_key.split('*') # ['school', 'nces_id', 'date' -> unused]
            school_name = item_details[0]
            ncesid = item_details[1]

            last_modified = bucket_item['LastModified'] # DateTime object

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

        
