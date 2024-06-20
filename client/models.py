
from django.db import models
from django.contrib.auth.models import AbstractUser
from activities.models import Activity

class ProUser(AbstractUser):
    username = None
    avatar_id = models.IntegerField(default=1)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    verification_code = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=150)
    activites = models.ManyToManyField(Activity, related_name="activities", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"