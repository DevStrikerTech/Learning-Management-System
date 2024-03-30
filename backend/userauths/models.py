from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Creates user model with required data fields.

    Args:
        AbstractUser (obj): inherits from built-in user model
    """
    username = models.CharField(unique=True, max_length=50)
    email = models.EmailField(unique=True)
    full_name = models.CharField(unique=True, max_length=100)
    otp = models.CharField(max_length=100, null=True, blank=True)
    refresh_token = models.CharField(max_length=1000, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        email_username, full_name = self.email.split("@")
        if self.full_name == "" or self.full_name == None:
            self.full_name == email_username
        if self.username == "" or self.username == None:
            self.username = email_username
        super(User, self).save(*args, **kwargs)
   
class Profile(models.Model):
    """
    Creates a profile based on given user.
    
    Args:
        models (obj): uses the custom user model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="user_folder", default="default-user.jpg", null=True, blank=True)
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
        if self.full_name == "" or self.full_name == None:
            self.full_name == self.user.username
        super(Profile, self).save(*args, **kwargs)

def create_user_profile(sender, instance, created, **kwargs):
    """
    Creates a user profile

    Args:
        sender (str): Specifies a particular sender to receive signals from.
        instance (str): user data
        created (str): timestamp
    """
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    """
    Saves user profile

    Args:
        sender (str): Specifies a particular sender to receive signals from.
        instance (str): user data
    """
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
