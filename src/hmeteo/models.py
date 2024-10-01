from django.db import models
from django.conf import settings
from django.db.models import Q
from openmeteo_requests import Client  # Import the Open-Meteo API client
from retry_requests import retry  # Import retry library for handling API errors
from datetime import datetime, timedelta  # Import datetime for date calculations
from requests_cache import CachedSession  # Import caching library for API responses
from django.core.exceptions import ValidationError  # Import validation error handling
import pandas as pd  # Import pandas for data manipulation
from userprofile.models import UserProfile  # Import UserProfile model
import requests
# Create your models here.
User = settings.AUTH_USER_MODEL  # Get the User model from settings

# Define a custom QuerySet for HTheItem
class HTheQuerySet(models.QuerySet):
    def search(self, query):
        """
        Performs a case-insensitive search on the 'location' field.

        Args:
            query: The search term.

        Returns:
            A QuerySet containing matching HTheItem objects.
        """
        lookup = (Q(location__icontains=query))  # Create a Q object for case-insensitive search
        return self.filter(lookup)  # Filter the QuerySet based on the lookup

# Define a custom Manager for HTheItem
class HTheManager(models.Manager):
    def get_queryset(self):
        """
        Returns a custom HTheQuerySet for this Manager.
        """
        return HTheQuerySet(self.model, using=self._db)

    def search(self, query=None):
        """
        Searches for HTheItem objects based on the query.

        Args:
            query: The search term.

        Returns:
            A QuerySet containing matching HTheItem objects.
        """
        if query is None:
            return self.get_queryset().none()  # Return an empty QuerySet if no query is provided
        return self.get_queryset().search(query)  # Use the custom search method on the QuerySet

# Define the HTheItem model
class HTheItem(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL, related_name='hmeteo')
    """
    The user associated with this location.
    """
    image = models.ImageField(upload_to="image/", blank=True, null=True)
    """
    An optional image for the location.
    """
    location = models.CharField(max_length=144)
    """
    The name of the location.
    """
    lat = models.FloatField(null=True, verbose_name='Latitude')
    """
    The latitude of the location.
    """
    lng = models.FloatField(null=True, verbose_name='Longitude')
    """
    The longitude of the location.
    """
    slug = models.SlugField(unique=True)
    """
    A unique slug for the location, used in URLs.
    """
    objects = HTheManager()  # Use the custom Manager
    """
    The webcam image
    """
    webcam_image = None

    def __str__(self):
        """
        Returns a string representation of the HTheItem object.
        """
        return f"{self.slug} by {self.user}: '{self.location}' {self.lat}°, {self.lng}°"

    def clean(self):
        """
        Validates the latitude and longitude values.
        """
        super().clean()  # Call the parent class's clean method
#        if self.lat < -180 or self.lat > 180:
#            raise ValidationError('Latitude out of range')
#        if self.lng < -180 or self.lng > 180:
#            raise ValidationError('Longitude out of range')

    class Meta:
        ordering = ['-location']  # Order items by location in descending order

    def get_windy_webcam_image(self):
        if (self.webcam_image is not None):
            return self.webcam_image
        windykey="FLGHmea20gemHtaSa56lyD6OGkiCnwBc"
        url = f"https://api.windy.com/webcams/api/v3/webcams?offset=0&nearby={self.lat},{self.lng},10&include=images"
        headers = {
            "x-windy-api-key": windykey
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        if data['webcams'][0]:
#            webcam_id = data['webcams'][0]['webcamId']
            self.webcam_image=data['webcams'][0]['images']['current']['preview']
            return self.webcam_image
        print("Error fetching webcam image")
        return None
    def get_absolute_url(self):
        """
        Returns the absolute URL for the location detail view.
        """
        return f"/hmeteo/{self.slug}"

    def get_edit_url(self):
        """
        Returns the URL for editing the location.
        """
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        """
        Returns the URL for deleting the location.
        """
        return f"{self.get_absolute_url()}/delete"

    def fetch_weather_data(self, url, params):
        """
        Fetches weather data from the Open-Meteo API.

        Args:
            url: The API endpoint URL.
            params: A dictionary of parameters for the API request.

        Returns:
            A dictionary containing weather data, or None if an error occurs.
        """
        cache_session = CachedSession('.cache', expire_after=3600)  # Create a cached session
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)  # Create a retry session
        openmeteo = Client(session=retry_session)  # Create an Open-Meteo API client

        try:
            responses = openmeteo.weather_api(url, params=params)  # Make the API request
            response = responses[0].Daily()  # Get the daily weather data
            data = {
                "date": pd.date_range(
                    start=pd.to_datetime(response.Time(), unit="s", utc=True),  # Convert time to datetime
                    end=pd.to_datetime(response.TimeEnd(), unit="s", utc=True),
                    freq=pd.Timedelta(seconds=response.Interval()),
                    inclusive="left"
                ),
                "tmax": response.Variables(0).ValuesAsNumpy(),  # Get maximum temperature values
                "tmin": response.Variables(1).ValuesAsNumpy(),  # Get minimum temperature values
                "rain": response.Variables(2).ValuesAsNumpy()  # Get rainfall values
            }
            dataframe = pd.DataFrame(data=data)  # Create a pandas DataFrame
            dataframe.fillna(0, inplace=True)  # Fill missing values with 0
            dataframe["date"] = dataframe["date"].dt.strftime("%a %d %b")  # Format dates

            return {
                'dates': dataframe["date"].tolist(),
                'tmax': dataframe["tmax"].tolist(),
                'tmin': dataframe["tmin"].tolist(),
                'rain': dataframe["rain"].tolist()
            }
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None

    def get_historical_temperature(self):
        """
        Fetches historical temperature data for the location.

        Returns:
            A dictionary containing historical temperature data, or None if an error occurs.
        """
        url = "https://archive-api.open-meteo.com/v1/archive"
        current_date = datetime.now()
        if not hasattr(self.user, 'userprofile'):
            UserProfile.objects.create(user=self.user)  # Create a UserProfile if it doesn't exist
        user_profile = self.user.userprofile
        start_date = current_date - timedelta(days=user_profile.daysBackwards)  # Calculate start date
        end_date = current_date - timedelta(days=1)  # Calculate end date
        formatted_start_date = start_date.strftime("%Y-%m-%d")
        formatted_end_date = end_date.strftime("%Y-%m-%d")
        params = {
            "latitude": self.lat,
            "longitude": self.lng,
            "start_date": formatted_start_date,
            "end_date": formatted_end_date,
            "daily": ["temperature_2m_max", "temperature_2m_min", "rain_sum"],
            "timezone": "auto"
        }
        return self.fetch_weather_data(url, params)

    def get_forecast_temperature(self):
        """
        Fetches forecast temperature data for the location.

        Returns:
            A dictionary containing forecast temperature data, or None if an error occurs.
        """
        url = "https://api.open-meteo.com/v1/forecast"
        if not hasattr(self.user, 'userprofile'):
            UserProfile.objects.create(user=self.user)  # Create a UserProfile if it doesn't exist
        user_profile = self.user.userprofile
        params = {
            "latitude": self.lat,
            "longitude": self.lng,
            "daily": ["temperature_2m_max", "temperature_2m_min", "rain_sum"],
            "forecast_days": user_profile.daysForward
        }
        return self.fetch_weather_data(url, params)

    def get_max_and_min_temps(self):
        """
        Retrieves the maximum and minimum temperatures from all locations.

        Returns:
            A dictionary containing the maximum and minimum temperatures.
        """
        max_of_max, min_of_min = HTheItem.compute_max_of_max_and_min_of_min()
        context = {
            "max": max_of_max,
            "min": min_of_min
        }
        return context

    @classmethod
    def compute_max_of_max_and_min_of_min(cls):
        """
        Calculates the maximum of maximum temperatures and minimum of minimum temperatures
        across all locations.

        Returns:
            A tuple containing the maximum of maximums and minimum of minimums.
        """
        all_items = cls.objects.all()
        max_temps = []
        min_temps = []

        for item in all_items:
            weather_data = item.get_forecast_temperature()
            if weather_data:
                max_temps.extend(weather_data['tmax'])
                min_temps.extend(weather_data['tmin'])

        max_of_max = max(max_temps) if max_temps else None
        min_of_min = min(min_temps) if min_temps else None

        return max_of_max, min_of_min
