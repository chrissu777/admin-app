from django.db import models

class Recording(models.Model):
    s3_filepath = models.CharField(max_length=200)
    rec_date = models.DateTimeField("date captured")
