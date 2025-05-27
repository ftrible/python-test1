from django import forms
from .models import BookItem,Author
from django.utils.text import slugify

class BookForm(forms.ModelForm):
    new_author_name = forms.CharField(required=False, label="New Author Name")
    new_author_bio = forms.CharField(required=False, label="New Author Bio", widget=forms.Textarea)

    class Meta:
        model=BookItem
        fields=['title','image', 'content', 'publish_date', 'author']
        widgets = {
            'publish_date': forms.TextInput(attrs={'id': 'id_publish_date'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        author = cleaned_data.get('author')
        new_author_name = cleaned_data.get('new_author_name')
        if not author and not new_author_name:
            raise forms.ValidationError("Please select an author or enter a new author.")
        return cleaned_data

    def save(self, commit=True):
        author = self.cleaned_data.get('author')
        new_author_name = self.cleaned_data.get('new_author_name')
        new_author_bio = self.cleaned_data.get('new_author_bio')
        if not author and new_author_name:
            author = Author.objects.create(name=new_author_name, bio=new_author_bio)
            self.instance.author = author
        return super().save(commit=commit)

    def generate_unique_slug(title):
        slug_base = slugify(title)
        slug = slug_base
        count = 1
        while BookItem.objects.filter(slug=slug).exists():
            slug = f"{slug_base}_{count}"
            count += 1
            print(slug)
        return slug
    
class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio']

