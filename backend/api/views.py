from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from api import serializer as api_serializer
from userauths.models import User, Profile

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from random import randint


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining token pairs.

    Args:
        TokenObtainPairView (type): Base class for token obtain views.
    """

    serializer_class = api_serializer.MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    """
    Custom view for user registration.

    Args:
        generics (type): Base class for generic views.
    """

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = api_serializer.RegisterSerializer


def generate_random_otp(length=7):
    """
    Generates a random one-time password (OTP).

    Args:
        length (int, optional): Length of the OTP. Defaults to 7.

    Returns:
        str: A randomly generated OTP.
    """
    otp = "".join([str(randint(0, 9)) for _ in range(length)])

    return otp


class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
    """
    Custom view for verifying password reset email.

    Args:
        generics (type): Base class for generic views.
    """

    permission_classes = [AllowAny]
    serializer_class = api_serializer.UserSerializer

    def get_object(self):
        email = self.kwargs["email"]
        user = User.objects.filter(email=email).first()

        if user:
            uuidb64 = user.pk
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh.access_token)

            user.refresh_token = refresh_token
            user.otp = generate_random_otp()
            user.save()

            link = f"http://localhost:5173/create-new-password/?otp={user.otp}&uuidb64={uuidb64}&refresh_token={refresh_token}"

            context = {"link": link, "username": user.username}

            html_body = render_to_string("email/password_reset.html", context)

            msg = EmailMultiAlternatives(
                subject="Password Rest Email",
                body="",
                from_email=settings.FROM_EMAIL,
                to=[user.email],
            )

            msg.attach_alternative(html_body, "text/html")
            msg.send()

        return user


class PasswordChangeAPIView(generics.CreateAPIView):
    """
    Custom view for changing user passwords.

    Args:
        generics (type): Base class for generic views.

    Returns:
        Response: A response indicating success or failure.
    """

    serializer_class = api_serializer.UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        otp = request.data["otp"]
        uuidb64 = request.data["uuidb64"]
        password = request.data["password"]

        user = User.objects.get(id=uuidb64, otp=otp)

        if user:
            user.set_password(password)
            user.otp = ""
            user.save()

            return Response(
                {"message": "Password Changed Successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": "User Does Not Exists"}, status=status.HTTP_404_NOT_FOUND
            )
