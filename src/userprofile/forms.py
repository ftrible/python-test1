from django import forms
from .models import UserProfile
class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['daysForward','daysBackwards' ]
        labels = {
            'daysForward': 'Days Forward',
            'daysBackwards': 'Days Backward'
        }