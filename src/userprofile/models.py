from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional user-specific fields here
    daysForward=models.IntegerField(default=3)
    daysBackwards=models.IntegerField(default=10)
    def __str__(self):
        return f"{self.user}: {self.daysForward}, {self.daysBackwards}"