from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=200)
    overview = models.TextField()
    release_date = models.CharField(max_length=100)
    vote_avg = models.DecimalField(max_digits=10, decimal_places=1)
    popularity = models.DecimalField(max_digits=10, decimal_places=1)
    genres = models.ManyToManyField(Genre, related_name='movies')
    likes = models.ManyToManyField(User, related_name='liked_movies')

class Person(models.Model):
    TYPE_CHOICES = [
        ('actor', '배우'),
        ('director', '감독')
    ]
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    name_kr = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
