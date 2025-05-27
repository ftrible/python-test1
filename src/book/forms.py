from django import forms
from .models import BookItem


class ObjForm(forms.ModelForm):
    class Meta:
        model=BookItem
        fields=['title','slug','image', 'content', 'publish_date']
        widgets = {
            'publish_date': forms.TextInput(attrs={'id': 'id_publish_date'}),
        }

def clean_title(self, *args, **kwargs):
   title=self.cleaned_data.get('title')
   instance=self.instance
   
   qs=BookItem.objects.filter(title=title)
   if instance is not None:
        qs.exclude(pk=instance.pk)
   if qs.exists():
       raise forms.ValidationError("This title already exists")
   return title
    
 