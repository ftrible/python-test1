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
    def save(self, commit=True):
        instance = super(HObjForm, self).save(commit=False)
        # Get latitude and longitude from OpenCageGeocode API
        location_name = self.cleaned_data['location']
        OCG = OpenCageGeocode('e3dd0f92c031405abba83cfeefbacd4e')
        results = OCG.geocode(location_name)
#        print(results[0])
        print(results[0]['components']['country'])
        if results and results[0].get('geometry'):
            instance.lat = results[0]['geometry']['lat']
            instance.lng = results[0]['geometry']['lng']
        else:
            raise ValidationError("Geocoding failed for the provided location.")
        instance.slug=slugify(self.cleaned_data['location'])
        if commit:
            instance.save()
        return instance
    def clean_title(self, *args, **kwargs):
        location=self.cleaned_data.get('location')
        instance=self.instance
        qs=HTheItem.objects.filter(location=location)
        if instance is not None:
                qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError("This location already exists")
        return location
    

