from django.urls import path, include
from .views import ActivityAPIView, ActivityRetriewAPIView, GeneratorAPIView

urlpatterns = [
    path("activity/", ActivityAPIView.as_view(), name="activity"),
    path("activity/<int:pk>/", ActivityAPIView.as_view(), name="activity-edit"),
    path("activity/detail/<int:pk>/", ActivityRetriewAPIView.as_view(), name="activity-detail"),

    path("activity/random/", GeneratorAPIView.as_view(), name="activity-random"),
] 