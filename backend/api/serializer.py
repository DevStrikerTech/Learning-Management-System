from rest_framework import serializers

from userauths.models import Profile, User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializes User model data.

    Args:
        serializers (type): The serializer class for User model.
    """
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializes Profile model data.

    Args:
        serializers (type): The serializer class for the Profile model.
    """
    class Meta:
        model = Profile
        fields = "__all__"
