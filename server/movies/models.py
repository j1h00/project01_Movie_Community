# movie/models.py 
from django.db import models
from django.conf import settings

# Create your models here.
class Crew(models.Model):
    name = models.CharField(max_length=20)
    role = models.CharField(max_length=20)
    profile_path = models.URLField(null=True)
    # biography = models.TextField()


class Genre(models.Model):
    name = models.CharField(max_length=50)

class Keyword(models.Model):
    name = models.CharField(max_length=50)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    overview = models.TextField(null=True)
    backdrop_path = models.URLField(null=True)
    poster_path = models.URLField(null=True)
    trailer_path = models.URLField(null=True)
    release_date = models.DateField(null=True)
    runtime = models.IntegerField(null=True)
    production_countries = models.TextField(null=True)
    adult = models.BooleanField(null=True)
    genres = models.ManyToManyField(Genre, related_name='movies')
    crews = models.ManyToManyField(Crew, related_name='movies')
    keywords = models.ManyToManyField(Keyword, related_name='movies')
    similar_movies = models.ManyToManyField("self", through="Similarity", symmetrical=False)
    # like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies', blank=True, through="Playlist")

class Similarity(models.Model):
    source = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='source')
    target = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='target')
    similarity = models.FloatField()


# 사용안함 
# class Playlist(models.Model):
#     p_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='p_user')
#     p_movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='p_movie')
#     status = models.IntegerField()
    