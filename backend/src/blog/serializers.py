from rest_framework import serializers
from blog.models import BlogEntry, RatingHistory, UserProfile


class BlogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogEntry
        fields = ["id", "title", "average_rating", "rating_count"]
