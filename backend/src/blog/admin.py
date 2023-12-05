from django.contrib import admin
from blog.models import BlogEntry, RatingHistory, UserProfile


admin.site.register(UserProfile)
admin.site.register(BlogEntry)
admin.site.register(RatingHistory)
