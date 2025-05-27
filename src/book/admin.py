from django.contrib import admin

# Register your models here.
from .models import BookItem

admin.site.register(BookItem)