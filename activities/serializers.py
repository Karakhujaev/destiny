from .models import Activity
from rest_framework.serializers import ModelSerializer

class ActivitySerializer(ModelSerializer):
    class Meta:
        model = Activity
        fields = ("id", "title", "description", "email", "phone_number", "is_active", "is_payed", "created_at", "modified_at")