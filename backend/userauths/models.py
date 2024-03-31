from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model with required data fields.

    Args:
        AbstractUser (obj): Inherits from the built-in user model.

    Attributes:
        username (str): User's unique username (limited to 50 characters).
        email (str): User's unique email address.
        full_name (str): User's full name (limited to 100 characters).
        otp (str, optional): One-time password for two-factor authentication.
        refresh_token (str, optional): Token for refreshing authentication.

    Class Variables:
        USERNAME_FIELD (str): Specifies the field used for authentication (here, 'email').
        REQUIRED_FIELDS (list): List of fields required during user registration (here, 'username').

    Methods:
        __str__(): Returns a string representation of the user (email address).
        save(*args, **kwargs): Custom save method to set default values for full_name and username.

    Note:
        - The `AbstractUser` class provides basic user functionality, and we extend it to add custom fields.
        - The `full_name` and `username` fields are derived from the user's email address by default.
    """

    username = models.CharField(unique=True, max_length=50)
    email = models.EmailField(unique=True)
    full_name = models.CharField(unique=True, max_length=100)
    otp = models.CharField(max_length=100, null=True, blank=True)
    refresh_token = models.CharField(max_length=1000, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        """
        Custom save method to set default values for full_name and username.

        If full_name is not provided, it defaults to the part of the email before the '@' symbol.
        If username is not provided, it also defaults to the same value as full_name.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        email_username, _ = self.email.split("@")

        if not self.full_name:
            self.full_name = email_username
        if not self.username:
            self.username = email_username

        super(User, self).save(*args, **kwargs)


class Profile(models.Model):
    """
    Represents a user profile associated with the custom User model.

    Args:
        models (obj): Django's model base class.

    Attributes:
        user (User): A one-to-one relationship with the custom User model.
        image (FileField): An optional user profile image (stored in 'user_folder').
        full_name (str): The user's full name (limited to 100 characters).
        country (str, optional): The user's country (limited to 100 characters).
        about (str, optional): A brief description about the user.
        date (DateTimeField): The timestamp when the profile was created.

    Methods:
        __str__(): Returns a string representation of the profile (full name or user's full name).
        save(*args, **kwargs): Custom save method to set default values for full_name and username.

    Note:
        - The `User` model should be imported from your custom user model module.
        - The `image` field allows users to upload a profile picture.
        - The `about` field can be used for a bio or additional information.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(
        upload_to="user_folder", default="default-user.jpg", null=True, blank=True
    )
    full_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.full_name)

    def save(self, *args, **kwargs):
        """
        Custom save method to set default values for full_name and username.

        If full_name is not provided, it defaults to the part of the email before the '@' symbol.
        If username is not provided, it also defaults to the same value as full_name.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        if not self.full_name:
            self.full_name = self.user.username
        super(Profile, self).save(*args, **kwargs)


def create_user_profile(sender, instance, created, **kwargs):
    """
    Creates a user profile when a new user is created.

    Args:
        sender (str): The sender of the signal (usually the User model).
        instance (User): The newly created user instance.
        created (bool): Indicates whether the user was just created.
    """
    if created:
        # Create a corresponding profile for the new user
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    """
    Saves the user profile associated with the user instance.

    Args:
        sender (str): The sender of the signal (usually the User model).
        instance (User): The user instance whose profile needs to be saved.
    """
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
