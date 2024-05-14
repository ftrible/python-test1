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
from userprofile.models import UserProfile
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
    def fetch_weather_data(self, url, params):
        cache_session = CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = Client(session=retry_session)

        try:
            responses = openmeteo.weather_api(url, params=params)
            response = responses[0].Daily()
            data = {
                "date": pd.date_range(
                    start=pd.to_datetime(response.Time(), unit="s", utc = True),
                    end=pd.to_datetime(response.TimeEnd(), unit="s", utc = True),
                    freq=pd.Timedelta(seconds=response.Interval()),
                    inclusive="left"
                ),
                "tmax": response.Variables(0).ValuesAsNumpy(),
                "tmin": response.Variables(1).ValuesAsNumpy(),
                "rain": response.Variables(2).ValuesAsNumpy()
            }
#            print(data)
            dataframe = pd.DataFrame(data=data)
            dataframe.fillna(0, inplace=True)
            dataframe["date"] = dataframe["date"].dt.strftime("%a %d %b")

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
        url = "https://archive-api.open-meteo.com/v1/archive"
        current_date = datetime.now()
        if not hasattr(self.user, 'userprofile'):
            UserProfile.objects.create(user=self.user)
        user_profile = self.user.userprofile
        start_date = current_date - timedelta(days=user_profile.daysBackwards)
        end_date = current_date - timedelta(days=1)
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
        url = "https://api.open-meteo.com/v1/forecast"
        if not hasattr(self.user, 'userprofile'):
            UserProfile.objects.create(user=self.user)
        user_profile = self.user.userprofile
        params = {
            "latitude": self.lat,
            "longitude": self.lng,
            "daily": ["temperature_2m_max", "temperature_2m_min", "rain_sum"],
            "forecast_days": user_profile.daysForward
        }
        return self.fetch_weather_data(url, params)
