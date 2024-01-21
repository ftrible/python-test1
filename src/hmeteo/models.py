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
    
class HTheItem(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL,related_name='hmeteo')
    image = models.ImageField(upload_to="image/", blank=True, null=True)
    location = models.CharField(max_length=144)
    lat=models.FloatField(null=True, verbose_name='Latitude')
    lng=models.FloatField(null=True, verbose_name='Longitude')
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
#        print(params)
        try:
            responses = openmeteo.weather_api(url, params=params)
            response = responses[0]
            # Process daily data. The order of variables needs to be the same as requested.
            daily = response.Daily()
            daily_tmax = daily.Variables(0).ValuesAsNumpy()
            daily_tmin = daily.Variables(1).ValuesAsNumpy()
            daily_rain = daily.Variables(2).ValuesAsNumpy()
            daily_data = {"date": pd.date_range(
                start = pd.to_datetime(daily.Time(), unit = "s"),
                end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
                freq = pd.Timedelta(seconds = daily.Interval()),
                inclusive = "left"
            )}
            daily_data["tmax"] = daily_tmax
            daily_data["tmin"] = daily_tmin
            daily_data["rain"] = daily_rain
            daily_dataframe = pd.DataFrame(data = daily_data)
            daily_dataframe.fillna(0)
            dates = [date.strftime("%Y-%m-%d") for date in daily_dataframe["date"]]
            tmax = daily_dataframe["tmax"].tolist()
            tmin = daily_dataframe["tmin"].tolist()
            rain = daily_dataframe["rain"].tolist()
            return {'dates': dates, 'tmax': tmax,'tmin': tmin,'rain': rain}
#            daily_data = []
#            for date, tmax,tmin in zip(daily_dataframe["date"], daily_dataframe["tmax"], daily_dataframe["tmin"]):
#                daily_data.append({"date": date, "tmax": tmax, "tmin": tmin})
#            return daily_data
        except Exception as e:
            # Handle the exception (e.g., log the error, display a message)
            print(f"Error fetching historical temperature data: {e}")
            return None
