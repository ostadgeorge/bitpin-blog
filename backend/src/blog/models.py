from django.db import models

# Create your models here.


class UserProfile(models.Model):
    phone = models.CharField(max_length=11, unique=True, db_index=True)

    def __str__(self) -> str:
        return self.phone


class BlogEntry(models.Model):
    title = models.CharField(max_length=100)

    average_rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)

    def insert_rating(self, rating: int):
        self.rating_count += 1
        self.average_rating = (self.average_rating * (self.rating_count - 1) + rating) / self.rating_count
        self.save()
    
    def update_rating(self, old_rating: int, new_rating: int):
        self.average_rating = (self.average_rating * self.rating_count - old_rating + new_rating) / self.rating_count
        self.save()

    def __str__(self) -> str:
        return self.title


class RatingHistory(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, db_index=True)
    blog_entry = models.ForeignKey(BlogEntry, on_delete=models.CASCADE, db_index=True)

    rating = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.user} rated {self.blog_entry} with {self.rating}"
