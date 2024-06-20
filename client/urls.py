from django.urls import path, include
from .views import UserAPIView, UserRetriewAPIView, UserLoginView, SendCodeAPIView, VerifyEmailView

urlpatterns = [
    path("", UserAPIView.as_view(), name="user"),
    path("<int:pk>/", UserAPIView.as_view(), name="user-edit"),
    path("detail/<int:pk>/", UserRetriewAPIView.as_view(), name="user-detail"),
    path("send/code/", SendCodeAPIView.as_view(), name="user-send-code"),
    path("verify/", VerifyEmailView.as_view(), name="user-verify"),
    path("login/", UserLoginView.as_view(), name="user-login"),
] 