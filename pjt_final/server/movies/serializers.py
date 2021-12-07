from django.db.models import fields
from rest_framework import serializers

from reviews.models import Review
from .models import Keyword, Movie, Genre, Crew, Similarity

# 영화 상세 정보 응답 시 사용하는 Serializer, prefetch 를 위해 내부에 추가로 serializer 선언
class MovieSerializer(serializers.ModelSerializer):

    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = ('id', 'name',)

    class CrewSerializer(serializers.ModelSerializer):
        class Meta:
            model = Crew
            fields = ('id', 'name', 'role', 'profile_path')

    class KeywordSerializer(serializers.ModelSerializer):
        class Meta:
            model = Keyword
            fields = ('id', 'name',)

    keywords = KeywordSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    crews = CrewSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = (
            'id', 'title', 'original_title', 'overview', 'backdrop_path', 'poster_path', 
            'release_date', 'runtime', 'production_countries', 'adult', 'genres', 'crews',
            'trailer_path', 'keywords')


# 단순 영화 리스트 응답 시 사용하는 serializer 
class MovieListSerializer(serializers.ModelSerializer):
    
    class ReviewSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Review
            fields = ('id', 'rating')

    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'backdrop_path', 'poster_path', 'release_date', 'reviews')

    
class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genre
        fields = '__all__'
        
class CrewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Crew
        fields = '__all__'

class SimilaritySerializer(serializers.ModelSerializer):
    
    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('id', 'title', 'poster_path')

    target = MovieSerializer(read_only=True)

    class Meta:
        model = Similarity
        fields = ('id', 'similarity', 'target')

# class ScoreSerializer(serializers.ModelSerializer):
    
#     class MovieSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = Movie
#             fields = ('id', 'title', 'poster_path')

#     target = MovieSerializer(read_only=True)

#     class Meta:
#         model = Similarity
#         fields = ('id', 'source', 'similarity', 'target')