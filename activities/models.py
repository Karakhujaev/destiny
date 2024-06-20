from django.db import models

class Activity(models.Model):
    photo = models.ImageField(upload_to="media/buissnesses/")
    title = models.CharField(max_length=50)
    description = models.TextField()
    email = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    is_active = models.BooleanField()
    is_payed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)