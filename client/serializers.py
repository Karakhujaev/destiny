from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import ProUser
from activities.serializers import ActivitySerializer, Activity

class UserSerializer(serializers.ModelSerializer):
    activities = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Activity.objects.all()
    )

    class Meta:
        model = ProUser
        fields = ("id", "first_name", "last_name", "email", "phone_number", "password", "is_verified", "activities", "created_at", "modified_at")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # Extract activities data and remove from validated_data
        activities_data = validated_data.pop('activities', [])

        # Hash the password
        password = make_password(validated_data["password"])

        # Remove the password from the validated data
        validated_data.pop("password")

        # Create the ProUser instance
        user_instance = ProUser.objects.create(password=password, **validated_data)

        # Now, add activities to the user_instance
        user_instance.activites.set(activities_data)

        return user_instance

    def get_activities(self, obj):
        activities = obj.activites.all()
        return ActivitySerializer(activities, many=True).data
