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
            self.stdout.write("Bucket empty or no content found")
            return

        for bucket_item in bucket_content:
            
            s3_key = bucket_item['Key'] # object naming convention: schoolname*nces_id
            item_details = s3_key.split('*') # ['school', 'nces_id', 'date' -> unused]
            school_name = item_details[0]
            ncesid = item_details[1]

            last_modified = bucket_item['LastModified'] # DateTime object

            school_model = School.objects.first()
            # School.objects.filter(nces_id = ncesid) TODO try this later
            if not Recording.objects.filter(s3_filepath=s3_key).exists():
                
                Recording.objects.create(
                    s3_filepath = s3_key,
                    rec_date = last_modified,
                    school = school_model
                )

        
