from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
# Create your models here.
User = settings.AUTH_USER_MODEL
class BookQuerySet(models.QuerySet):
    def published(self):
        now=timezone.now()
        return self.filter(publish_date__lte=now)
    def search(self, query):
        lookup=(Q(content__icontains=query) |
                Q(title__icontains=query) |
                Q(user__username__icontains=query))
        return self.filter(lookup)
        
class BookManager(models.Manager):
    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)
    def published(self):
        return self.get_queryset().published()
    def search(self, query=None):
        if  query is None:
            return self.get_queryset().none()
        return self.published().search(query)
    
class BookItem(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL,related_name='book')
    image = models.ImageField(upload_to="image/", blank=True, null=True)
    title = models.CharField(max_length=144)
    slug = models.SlugField(unique=True)
    content = models.TextField(null=True, blank=True)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects=BookManager()
    def __str__(self):
        return f"{self.title} by {self.user}: {self.publish_date}, {self.timestamp}"
    class Meta:
        ordering=['-publish_date', '-updated', '-timestamp']
    def get_absolute_url(self):
        return f"/book/{self.slug}"
    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"
    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"