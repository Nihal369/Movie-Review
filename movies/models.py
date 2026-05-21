from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField(max_length=255)

    description = models.TextField()

    release_date = models.DateField()

    genre = models.CharField(max_length=100)

    language = models.CharField(max_length=100)

    duration = models.CharField(max_length=50)

    director = models.CharField(max_length=255)

    cast = models.TextField()

    poster = models.URLField()

    banner = models.URLField()

    trailer = models.URLField()

    rating = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    review_count = models.IntegerField(
        default=0
    )

    def __str__(self):
        return self.title
    

    
class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.IntegerField()

    review_text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = ['user', 'movie']

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"