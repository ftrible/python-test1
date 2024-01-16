from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.db.models import Q
from openmeteo_requests import Client
from retry_requests import retry
from datetime import datetime
from requests_cache import CachedSession
import pandas as pd
import json
# Create your models here.
User = settings.AUTH_USER_MODEL
    
class HTheItem(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL,related_name='hmeteo')
    image = models.ImageField(upload_to="image/", blank=True, null=True)
    location = models.CharField(max_length=144)
    lat=models.FloatField(null=True, editable=False, verbose_name='Latitude')
    lng=models.FloatField(null=True, editable=False, verbose_name='Longitude')
    slug = models.SlugField(unique=True)
 
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
        params = {
            "latitude": self.lat,
            "longitude": self.lng,
            "start_date": '2023-12-31', #start_date.strftime("%Y-%m-%d"),
            "end_date":'2024-01-10', #end_date.strftime("%Y-%m-%d"),
	        "daily": ["temperature_2m_max", "temperature_2m_min"],
	        "timezone": "auto"
        }
        try:
            responses = openmeteo.weather_api(url, params=params)
            response = responses[0]
            # Process hourly data. The order of variables needs to be the same as requested.
            daily = response.Daily()
            daily_temperature_max = daily.Variables(0).ValuesAsNumpy()
            daily_temperature_min = daily.Variables(1).ValuesAsNumpy()
            daily_data = {"date": pd.date_range(
                start = pd.to_datetime(daily.Time(), unit = "s"),
                end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
                freq = pd.Timedelta(seconds = daily.Interval()),
                inclusive = "left"
            )}
            daily_data["tmax"] = daily_temperature_max
            daily_data["tmin"] = daily_temperature_min
            daily_dataframe = pd.DataFrame(data = daily_data)
            dates = [date.strftime("%Y-%m-%d") for date in daily_dataframe["date"]]
            tmax = daily_dataframe["tmax"].tolist()
            tmin = daily_dataframe["tmin"].tolist()
            return {'dates': dates, 'tmax': tmax,'tmin': tmin}
#            daily_data = []
#            for date, tmax,tmin in zip(daily_dataframe["date"], daily_dataframe["tmax"], daily_dataframe["tmin"]):
#                daily_data.append({"date": date, "tmax": tmax, "tmin": tmin})
#            return daily_data
        except Exception as e:
            # Handle the exception (e.g., log the error, display a message)
            print(f"Error fetching historical temperature data: {e}")
            return None
