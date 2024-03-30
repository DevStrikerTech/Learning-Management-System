from unittest.mock import Mock
from django.test import TestCase
from userauths.models import User, Profile, create_user_profile, save_user_profile

class UserAuthsModelTest(TestCase):
    def test_create_user_with_valid_details(self):
        user = User(email="test@example.com", username="test", full_name="Test User")
        user.save()
        assert user.email == "test@example.com"
        assert user.username == "test"
        assert user.full_name == "Test User"

    def test_create_profile_with_required_fields(self):
        user = User.objects.create(email="test@example.com", username="test")

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=user, full_name="John Doe")

        assert profile.user == user
        assert profile.full_name == ""
        assert profile.image == "default-user.jpg"
        assert profile.country is None
        assert profile.about is None
        assert profile.date is not None
        
    def test_create_user_profile_success(self):
        user = User.objects.create(username="test", email="test@example.com")

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=user)

        assert profile is not None
        
    def test_saves_user_profile_with_valid_arguments(self):
        sender = "Sender"
        instance = Mock()
        instance.profile = Mock()
    
        save_user_profile(sender, instance)
    
        instance.profile.save.assert_called_once()