from unittest.mock import Mock
from django.test import TestCase
from userauths.models import User, Profile, save_user_profile


class UserAuthsModelTest(TestCase):
    """Test cases for User and Profile models."""

    def test_create_user_with_valid_details(self):
        """Test creating a user with valid details."""
        user = User(email="test@example.com", username="test", full_name="Test User")
        user.save()
        assert user.email == "test@example.com"
        assert user.username == "test"
        assert user.full_name == "Test User"

    def test_create_profile_with_required_fields(self):
        """Test creating a profile with required fields."""
        user = User.objects.create(email="test@example.com", username="test")

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=user, full_name="John Doe")

        assert profile.user == user
        assert profile.full_name == "test"
        assert profile.image == "default-user.jpg"
        assert profile.country is None
        assert profile.about is None
        assert profile.date is not None

    def test_create_user_profile_success(self):
        """Test creating a user profile successfully."""
        user = User.objects.create(username="test", email="test@example.com")

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=user)

        assert profile is not None

    def test_save_user_profile_saves_profile(self):
        """Test that saving a user profile calls the profile's save method."""
        sender = "Sender"
        instance = Mock()
        instance.profile = Mock()

        save_user_profile(sender, instance)

        instance.profile.save.assert_called_once()
