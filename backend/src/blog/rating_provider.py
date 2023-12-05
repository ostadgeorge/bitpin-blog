from redis import Redis
from django.conf import settings


class RatingProvider:
    def __init__(self):
        self.redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
    
    def get_rating(self, blog_id: int, phone: str) -> float:
        rating = self.redis.hget(f"blog:{blog_id}", phone)
        if rating:
            return float(rating)

        return None

    def set_rating(self, blog_id: int, phone: str, rating: float):
        self.redis.hset(f"blog:{blog_id}", phone, rating)
    
    def rebuild_ratings(self):
        from blog.models import BlogEntry, RatingHistory

        for blog_entry in BlogEntry.objects.all():
            self.redis.delete(f"blog:{blog_entry.id}")
            for rating_history in RatingHistory.objects.filter(blog_entry=blog_entry).all():
                self.set_rating(blog_entry.id, rating_history.user.phone, rating_history.rating)

    @staticmethod
    def get_instance():
        if not hasattr(RatingProvider, "_instance"):
            RatingProvider._instance = RatingProvider()
        return RatingProvider._instance
