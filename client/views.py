from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from  rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from django.urls import reverse
from config import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
import random
from client.models import ProUser
from client.serializers import UserSerializer

class SendCodeAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                "Email is required", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = ProUser.objects.get(email=email)
            code = random.randint(1000, 9999)
            user.verification_code = f"{code}"
            user.save()
            
        except ProUser.DoesNotExist:
            return Response({"message": "User Not Found"}, status=status.HTTP_400_BAD_REQUEST)
        
        send_mail(
            'Verify your email',
            f'Your verification code is: {code}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return Response({'success': True, "message": "Verification Code Successfully sent"}, status=status.HTTP_200_OK)

class VerifyEmailView(APIView):
    def get(self, request):
        user_id = request.data.get('user_id')
        code = request.data.get('code')

        try:
            user = ProUser.objects.get(pk=user_id)
        except ProUser.DoesNotExist:
            return Response({'error': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)

        if user.verification_code == code:
            user.is_verified = True
            user.verification_code = None
            user.save()
            return Response({'message': 'Email verified successfully!'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
        
class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)

        try:
            user = ProUser.objects.get(email=email)

        except ProUser.DoesNotExist:
            return Response(
                {"message": f"There is no user with  - {email}"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # if user.is_verified == False:
        #     return Response(
        #         {"message": "User is not verified"},
        #         status=status.HTTP_401_UNAUTHORIZED,
        #     )

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response(
                {
                    "user_id": user.pk,
                    "avatar_id": user.avatar_id,
                    "phone_number": user.phone_number,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "access": access_token,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

class UserAPIView(GenericAPIView):
    queryset = ProUser.objects.all()
    serializer_class = UserSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {"error": "User is not authenticated."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_200_OK)

    def get_object(self, pk):
        try:
            users = ProUser.objects.get(pk=pk)
            return users
        except ProUser.DoesNotExist:
            return None
        
class UserRetriewAPIView(RetrieveAPIView):
    queryset = ProUser.objects.all()
    serializer_class = UserSerializer