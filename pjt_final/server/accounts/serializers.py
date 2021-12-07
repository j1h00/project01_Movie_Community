from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth import get_user_model
from movies.models import Movie
from reviews.models import Review, Comment

class UserSerializer(serializers.ModelSerializer): 
    class ReviewSerializer(serializers.ModelSerializer):

        class Meta:
            model = Review
            fields = ('id', 'content', 'rating', 'created_at', 'updated_at', 'like_users', 'movie', 'user')

    class CommentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ('id', 'content', 'created_at', 'updated_at', 'review', 'user')

    reviews = ReviewSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta: 
        model= get_user_model()
        fields=('id', 'username', 'password', 'reviews', 'comments')