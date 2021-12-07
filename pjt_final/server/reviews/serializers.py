from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers

from movies.models import Movie
from .models import Review, Comment

# 리뷰 상세 정보, 생성, 수정 시 사용하는 serializer 
# 리뷰 상세 정보 조회 시에만 user, movie 를 같이 prefetch 하여 응답 (read_only_fields)  
class ReviewSerializer(serializers.ModelSerializer):    
    
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('id', 'username',)

    user = UserSerializer(read_only=True)

    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('id', 'title', 'backdrop_path')

    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'content', 'rating', 'created_at', 'updated_at', 'user', 'like_users', 'movie')
        read_only_fields = ('user', 'movie', 'like_users')
        

class CommentSerializer(serializers.ModelSerializer):
    
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('id', 'username',)

    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'user', 'review')