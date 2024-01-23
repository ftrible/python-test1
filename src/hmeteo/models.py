from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.db.models import Q
from openmeteo_requests import Client
from retry_requests import retry
from datetime import datetime, timedelta
from requests_cache import CachedSession
import pandas as pd
import json
# Create your models here.
User = settings.AUTH_USER_MODEL
# https://open-meteo.com/en/docs/historical-weather-api/
class HTheQuerySet(models.QuerySet):
     def search(self, query):
        lookup=(Q(location__icontains=query))
        return self.filter(lookup)
        
class HTheManager(models.Manager):
    def get_queryset(self):
        return HTheQuerySet(self.model, using=self._db)
    def search(self, query=None):
        if  query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)


class HTheItem(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL,related_name='hmeteo')
    image = models.ImageField(upload_to="image/", blank=True, null=True)
    location = models.CharField(max_length=144)
    lat=models.FloatField(null=True, verbose_name='Latitude')
    lng=models.FloatField(null=True, verbose_name='Longitude')
    slug = models.SlugField(unique=True)
    objects=HTheManager()
 
    class Meta:
        ordering=['-location']
    def get_absolute_url(self):
        return f"/hmeteo/{self.slug}"
    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"
    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"
    def get_historical_temperature(self): #,start_date, end_date):
        cache_session = CachedSession('.cache', expire_after = -1)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = Client(session = retry_session)
        url = "https://archive-api.open-meteo.com/v1/archive"
        # Get the current date
        current_date = datetime.now()
        # Calculate the start date by subtracting 10 days from the current date
        start_date = current_date - timedelta(days=10)
        end_date = current_date - timedelta(days=1)
        # Format the dates as strings in the required format ("%Y-%m-%d")
        formatted_start_date = start_date.strftime("%Y-%m-%d")
        formatted_end_date = end_date.strftime("%Y-%m-%d")
        params = {
            "latitude": self.lat,
            "longitude": self.lng,
            "start_date": formatted_start_date,
            "end_date":formatted_end_date,
	        "daily": ["temperature_2m_max", "temperature_2m_min", "rain_sum"],
	        "timezone": "auto"
        }
        try:
            responses = openmeteo.weather_api(url, params=params)
            response = responses[0]
            # Process daily data. The order of variables needs to be the same as requested.
            daily = response.Daily()
            daily_data = {
                "date": pd.date_range(
                    start = pd.to_datetime(daily.Time(), unit = "s"),
                    end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
                    freq = pd.Timedelta(seconds = daily.Interval()),
                    inclusive = "left"
                ),
                "tmax": daily.Variables(0).ValuesAsNumpy(),
                "tmin": daily.Variables(1).ValuesAsNumpy(),
                "rain": daily.Variables(2).ValuesAsNumpy()
            }
            # Create a DataFrame from the extracted data
            daily_dataframe = pd.DataFrame(data=daily_data)

            # Fill NaN values with 0
            daily_dataframe.fillna(0, inplace=True)

            # Convert date column to string in the desired format
            daily_dataframe["date"] = daily_dataframe["date"].dt.strftime("%Y-%m-%d")

            # Extract lists from DataFrame
            dates = daily_dataframe["date"].tolist()
            tmax = daily_dataframe["tmax"].tolist()
            tmin = daily_dataframe["tmin"].tolist()
            rain = daily_dataframe["rain"].tolist()

            return {'dates': dates, 'tmax': tmax,'tmin': tmin,'rain': rain}
        except Exception as e:
            # Handle the exception (e.g., log the error, display a message)
            print(f"Error fetching historical temperature data: {e}")
            return None
    def get_forecast_temperature(self):
        try:
            cache_session = CachedSession('.cache', expire_after=3600)
            retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
            openmeteo = Client(session=retry_session)
            url = "https://api.open-meteo.com/v1/forecast"

            # Construct the parameters using self.lat and self.lng
            params = {
                "latitude": self.lat,
                "longitude": self.lng,
                "daily": ["temperature_2m_max", "temperature_2m_min", "rain_sum"],
                "forecast_days": 7
            }

            # Make the API request
            responses = openmeteo.weather_api(url, params=params)
            response = responses[0]

            # Process forecast data
            forecast = response.Daily()
            forecast_data = {
                "date": pd.date_range(
                    start=pd.to_datetime(forecast.Time(), unit="s"),
                    end = pd.to_datetime(forecast.TimeEnd(), unit = "s"),
                    freq=pd.Timedelta(seconds=forecast.Interval()),
                    inclusive="left"
                ),
                "tmax": forecast.Variables(0).ValuesAsNumpy(),
                "tmin": forecast.Variables(1).ValuesAsNumpy(),
                "rain": forecast.Variables(2).ValuesAsNumpy()
            }

            # Create a DataFrame from the extracted data
            forecast_dataframe = pd.DataFrame(data=forecast_data)

            # Fill NaN values with 0
            forecast_dataframe.fillna(0, inplace=True)

            # Convert date column to string in the desired format
            forecast_dataframe["date"] = forecast_dataframe["date"].dt.strftime("%Y-%m-%d")

            # Extract lists from DataFrame
            dates = forecast_dataframe["date"].tolist()
            tmax = forecast_dataframe["tmax"].tolist()
            tmin = forecast_dataframe["tmin"].tolist()
            rain = forecast_dataframe["rain"].tolist()

            return {'dates': dates, 'tmax': tmax, 'tmin': tmin,'rain': rain}
        except Exception as e:
            # Handle the exception (e.g., log the error, display a message)
            print(f"Error fetching forecast temperature data: {e}")
            return None
