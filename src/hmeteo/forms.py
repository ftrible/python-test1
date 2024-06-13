from django import forms
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from .models import HTheItem
# https://opencagedata.com/dashboard#geocoding
# See full Python tutorial:
# https://opencagedata.com/tutorials/geocode-in-python
from opencage.geocoder import OpenCageGeocode
class HObjForm(forms.ModelForm):
    class Meta:
        model=HTheItem
        fields=['location','image' ]

    def __init__(self, *args, **kwargs):
        super(HObjForm, self).__init__(*args, **kwargs)
        # Set default value for location if not provided
        if not self.data.get('location'):
            self.data = self.data.copy()
            self.data['location'] = 'Default Location'  # Set your default value here
    def save(self, commit=True):
        instance = super(HObjForm, self).save(commit=False)
        # Get latitude and longitude from OpenCageGeocode API
        location_name = self.cleaned_data['location']
        OCG = OpenCageGeocode('e3dd0f92c031405abba83cfeefbacd4e')
        results = OCG.geocode(location_name)
        if len(results) > 1:
            # Show a dialog to select the desired location
            print("More than 1 " + str(len(results)))
            pass
        elif len(results) == 1:
            result = results[0]
            instance.lat = result['geometry']['lat']
            instance.lng = result['geometry']['lng']
            instance.slug = self.generate_unique_slug(location_name)
        else:
            raise ValidationError("Geocoding failed for the provided location.")
        if commit:
            instance.save()
        return instance
    @staticmethod
    def generate_unique_slug(location_name):
        slug_base = slugify(location_name)
        slug = slug_base
        count = 1
        while HTheItem.objects.filter(slug=slug).exists():
            slug = f"{slug_base}_{count}"
            count += 1
            print(slug)
        return slug
    def clean_title(self, *args, **kwargs):
        location=self.cleaned_data.get('location')
        instance=self.instance
        qs=HTheItem.objects.filter(location=location)
        if instance is not None:
                qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError("This location already exists")
        return location