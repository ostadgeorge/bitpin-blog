from django.urls import path
from blog.views import get_blog_entries, rate_blog_entry

urlpatterns = [
    path("blog_entries/", get_blog_entries),
    path("rate_blog_entry/", rate_blog_entry),
]
