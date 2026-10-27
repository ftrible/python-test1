from django import forms
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from .models import MeteoItem
from geopy.geocoders import Nominatim
class MeteoForm(forms.ModelForm):
    class Meta:
        model=MeteoItem
        fields=['location','image' ]

    def __init__(self, *args, **kwargs):
        super(MeteoForm, self).__init__(*args, **kwargs)
        # Set default value for location if not provided
        if not self.data.get('location'):
            self.data = self.data.copy()
            self.data['location'] = 'Default Location'  # Set your default value here
    def save(self, commit=True):
        instance = super(MeteoForm, self).save(commit=False)
        # Get latitude and longitude from Nominatim geocoding API
        location_name = self.cleaned_data['location']
        geolocator = Nominatim(user_agent="hmeteo_geocoder")
        location = geolocator.geocode(location_name)
        if location:
            instance.lat = location.latitude
            instance.lng = location.longitude
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
        while MeteoItem.objects.filter(slug=slug).exists():
            slug = f"{slug_base}_{count}"
            count += 1
            print(slug)
        return slug
    def clean_title(self, *args, **kwargs):
        location=self.cleaned_data.get('location')
        instance=self.instance
        qs=MeteoItem.objects.filter(location=location)
        if instance is not None:
                qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError("This location already exists")
        return location