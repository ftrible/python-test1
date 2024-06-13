from django import forms
from .models import TheItem


class ObjForm(forms.ModelForm):
    class Meta:
        model=TheItem
        fields=['title','slug','image', 'content', 'publish_date']
        widgets = {
            'publish_date': forms.TextInput(attrs={'id': 'id_publish_date'}),
        }
#   title=forms.CharField()
#    slug=forms.SlugField()
#   content=forms.CharField(widget=forms.Textarea)

def clean_title(self, *args, **kwargs):
   title=self.cleaned_data.get('title')
   instance=self.instance
   
   qs=TheItem.objects.filter(title=title)
   if instance is not None:
        qs.exclude(pk=instance.pk)
   if qs.exists():
       raise forms.ValidationError("This title already exists")
   return title
    
 