from django.contrib import admin
from .models import Category, BlogPost, UserProfile

# Register your models here.
admin.site.register(Category)
admin.site.register(BlogPost)
admin.site.register(UserProfile)
