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

    def rate_blog(self, user: UserProfile, rating: int):
        try:
            rating_history = RatingHistory.objects.get(user=user, blog_entry=self)
            old_rating = rating_history.rating
            rating_history.rating = rating
            rating_history.save()
            self.update_rating(old_rating, rating)
        except RatingHistory.DoesNotExist:
            rating_history = RatingHistory.objects.create(user=user, blog_entry=self, rating=rating)
            self.insert_rating(rating)

    def __str__(self) -> str:
        return self.title


class RatingHistory(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, db_index=True)
    blog_entry = models.ForeignKey(BlogEntry, on_delete=models.CASCADE, db_index=True)

    rating = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"{self.user} rated {self.blog_entry} with {self.rating}"
