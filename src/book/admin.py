from django.contrib import admin

# Register your models here.
from .models import BookItem,Author

admin.site.register(BookItem)
admin.site.register(Author)