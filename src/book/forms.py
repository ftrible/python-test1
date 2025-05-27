from django import forms
from .models import BookItem
from django.utils.text import slugify

class BookForm(forms.ModelForm):
    class Meta:
        model=BookItem
        fields=['title','image', 'content', 'publish_date']
        widgets = {
            'publish_date': forms.TextInput(attrs={'id': 'id_publish_date'}),
        }

    # def clean_title(self, *args, **kwargs):
    #     title=self.cleaned_data.get('title')
    #     instance=self.instance
        
    #     qs=BookItem.objects.filter(title=title)
    #     if instance is not None:
    #             qs.exclude(pk=instance.pk)
    #     if qs.exists():
    #         raise forms.ValidationError("This title already exists")
    #     return title

    def generate_unique_slug(title):
        slug_base = slugify(title)
        slug = slug_base
        count = 1
        while BookItem.objects.filter(slug=slug).exists():
            slug = f"{slug_base}_{count}"
            count += 1
            print(slug)
        return slug

