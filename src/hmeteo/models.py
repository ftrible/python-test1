from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
# Create your models here.
User = settings.AUTH_USER_MODEL
    
class TheItem(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL,related_name='hmeteo')
    image = models.ImageField(upload_to="image/", blank=True, null=True)
    location = models.CharField(max_length=144)
    slug = models.SlugField(unique=True)
 
    class Meta:
        ordering=['-location']
    def get_absolute_url(self):
        return f"/hmeteo/{self.slug}"
    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"
    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"