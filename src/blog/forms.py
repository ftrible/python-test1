from django import forms
from .models import BlogPost


class BlogForm(forms.ModelForm):
    class Meta:
        model=BlogPost
        fields=['title','slug','image', 'content', 'publish_date']
#   title=forms.CharField()
#    slug=forms.SlugField()
#   content=forms.CharField(widget=forms.Textarea)

def clean_title(self, *args, **kwargs):
   title=self.cleaned_data.get('title')
   instance=self.instance
   
   qs=BlogPost.objects.filter(title=title)
   if instance is not None:
        qs.exclude(pk=instance.pk)
   if qs.exists():
       raise forms.ValidationError("This title already exists")
   return title
    
 