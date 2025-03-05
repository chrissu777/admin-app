from django.db import models
from accounts.models import School

class Recording(models.Model):
    s3_filepath = models.CharField(max_length=200)
    rec_date = models.DateTimeField("date captured")
    school = models.ForeignKey(School,blank=False,on_delete=models.CASCADE)
