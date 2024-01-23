from django import forms
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from .models import UserProfile
class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['daysForward','daysBackwards' ]
    

