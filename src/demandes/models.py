from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Q

User = settings.AUTH_USER_MODEL
# Create your models here.
class Demandes(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL,related_name='demandes')
    title = models.CharField(max_length=144)
    slug = models.SlugField(unique=True)
    content = models.TextField(null=True, blank=True)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects=models.Manager()
    CATEGORY_CHOICES = [
        ('courses', 'Courses'),
        ('livraison', 'Livraison'),
        ('transport', 'Transport'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.title} by {self.user}: {self.publish_date}, {self.timestamp}"
    class Meta:
        ordering=['-publish_date', '-updated', '-timestamp']
    def get_absolute_url(self):
        return f"/demandes/{self.slug}"
    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"
    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"
#   
#  class CustomUser(AbstractUser):
#    is_admin = models.BooleanField(default=False)
#    is_volunteer = models.BooleanField(default=False)
#
#class Senior(models.Model):
#    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#    # Ajoutez d'autres champs spécifiques aux seniors

