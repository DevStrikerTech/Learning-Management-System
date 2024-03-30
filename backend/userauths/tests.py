from django.test import TestCase
from userauths.models import User, Profile

class UserAuthsModelTest(TestCase):
    def test_create_user_with_valid_details(self):
        user = User(email="test@example.com", username="testuser", full_name="Test User")
        user.save()
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.full_name == "Test User"

    def test_create_profile_with_required_fields(self):
        user = User.objects.create(email="test@example.com", username="test")
        profile = Profile.objects.create(user=user, full_name="John Doe")
    
        assert profile.user == user
        assert profile.full_name == "John Doe"
        assert profile.image == "default-user.jpg"
        assert profile.country == None
        assert profile.about == None
        assert profile.date != None