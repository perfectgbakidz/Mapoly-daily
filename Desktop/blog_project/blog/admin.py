from django.contrib import admin
from .models import Category, Profile, BlogPost, Comment

admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(BlogPost)
admin.site.register(Comment)
