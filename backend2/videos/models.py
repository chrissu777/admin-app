from django.db import models
from accounts.models import School
from django.utils import timezone

class Recording(models.Model):
    s3_filepath = models.CharField(max_length=200)
    rec_date = models.DateTimeField("date captured")
    timestamp = models.DateTimeField("recording start time", default=timezone.now)
    cam_id = models.CharField(max_length=50, default="unknown")
    camera_name = models.CharField(max_length=100, default="unknown")
    school = models.ForeignKey(School,blank=False,on_delete=models.CASCADE)
