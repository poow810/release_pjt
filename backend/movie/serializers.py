from rest_framework import serializers

from accounts.models import Review
from .models import Movie, Genre, Person
from django.contrib.auth import get_user_model


User = get_user_model()

class MovieGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"
# 장르 조회
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


# 영화 조회
class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    liked_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id',
            'movie_id',
            'title',
            'poster_path',
            'overview',
            'release_date',
            'vote_avg',
            'popularity',
            'genres',
            'liked_count',
            'is_liked',
        ]

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.likes.filter(id=user.id).exists()


class ReviewSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'nickname', 'user_image']
    
    user = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ('user', 'movie')


class ReviewDetailSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'nickname', 'user_image']

    user = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = "__all__"


class MovieSearchSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'genres']

class PersonSerializer(serializers.ModelSerializer):
    movies = MovieSearchSerializer(many=True, read_only=True)  # 배우가 출연한 영화 포함

    class Meta:
        model = Person
        fields = ['id', 'name_kr', 'name_en', 'type', 'movies']
