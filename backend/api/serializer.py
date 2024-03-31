from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from userauths.models import Profile, User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom TokenObtainPairSerializer with additional user information.

    Args:
        TokenObtainPairSerializer (type): The base TokenObtainPairSerializer class.

    Returns:
        type: A token containing user's full name, email, and username.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["full_name"] = user.full_name
        token["email"] = user.email
        token["username"] = user.username

        return token


class RegisterSerializer(serializers.ModelSerializer):
    """
    Custom serializer for user registration.

    Args:
        serializers (type): The base serializers class.

    Raises:
        serializers.ValidationError: Raised if password fields do not match.

    Returns:
        type: A new user instance.
    """

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_matched = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["full_name", "email", "password", "password_matched"]

    def validate(self, attr):
        if attr["password"] != attr["password_matched"]:
            raise serializers.ValidationError(
                {"password": "Password fields do not match."}
            )

        return attr

    def create(self, validated_data):
        user = User.objects.create(
            full_name=validated_data["full_name"],
            email=validated_data["email"],
        )

        email_username, _ = user.email.split("@")
        user.username = email_username
        user.set_password(validated_data["password"])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes User model data.

    Args:
        serializers (type): The serializer class for User model.
    """

    class Meta:
        model = User
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializes Profile model data.

    Args:
        serializers (type): The serializer class for the Profile model.
    """

    class Meta:
        model = Profile
        fields = "__all__"
