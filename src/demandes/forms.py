from django import forms
from .models import Demandes


class DemandesForm(forms.ModelForm):
    class Meta:
        model=Demandes
        fields=['title','slug', 'content', 'category', 'publish_date']
        widgets = {
            'publish_date': forms.TextInput(attrs={'id': 'id_publish_date'}),
        }
    
 