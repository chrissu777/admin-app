from django.db import models

class School(models.Model):
    name = models.CharField(max_length=255)
    nces_id = models.CharField(max_length=20,default=0)

class Profile(models.Model):
    ROLE_CHOICES=[
        ("SC_ADMIN", "School Admin"),
        ("POLICE", "Police"),
    ]
    role = models.CharField(max_length=50,choices=ROLE_CHOICES)
    school = models.ForeignKey(School, blank=True, on_delete=models.CASCADE, related_name='admins')
    jursidction = models.ManyToManyField(School, blank=True, related_name='officers')