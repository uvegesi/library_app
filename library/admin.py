from django.contrib import admin

# Register your models here.

from .models import Book, User, Issue
admin.site.register(Book)
admin.site.register(Issue)

