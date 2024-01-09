from django import forms
from .models import TheItem


class ObjForm(forms.ModelForm):
    class Meta:
        model=TheItem
        fields=['location','slug','image' ]

def clean_title(self, *args, **kwargs):
   location=self.cleaned_data.get('location')
   instance=self.instance
   
   qs=TheItem.objects.filter(location=location)
   if instance is not None:
        qs.exclude(pk=instance.pk)
   if qs.exists():
       raise forms.ValidationError("This location already exists")
   return location
    
 