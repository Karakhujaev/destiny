from django.shortcuts import render
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Activity
from .serializers import ActivitySerializer
from random import randint

#CRUD
class ActivityAPIView(GenericAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request,  pk=None):
        activities = self.get_queryset()
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        activity = self.get_object(pk)
        serializer = self.get_serializer(activity, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        activity = self.get_object(pk)
        if activity is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        activity.delete()
        return Response(status=status.HTTP_200_OK)

    def get_object(self, pk):
        try:
            activity = Activity.objects.get(pk=pk)
            return activity
        except Activity.DoesNotExist:
            return None

class ActivityRetriewAPIView(RetrieveAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class GeneratorAPIView(APIView):
    def get(self, request):
        activities = Activity.objects.all()
        count = activities.count()
        if count > 0:
            random_index = randint(0, count - 1)
            random_activity = activities[random_index]
            serializer = ActivitySerializer(random_activity)

        else:
            return Response({"success": False}, status=status.HTTP_200_OK)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    

