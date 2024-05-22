from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer

from accounts.models import Review
from movie.serializers import MovieSerializer
from community.models import Comment, Post
from movie.models import Movie


User = get_user_model()

# 프로필 페이지에서 작성한 게시글 조회
class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'category']

# 프로필 페이지에서 좋아요 누른 영화 조회
class UserMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'movie_id', 'title', 'poster_path', 'overview', 'release_date', 'vote_avg', 'popularity', 'genres']

    
# 프로필 페이지에서 작성한 댓글 조회
class UserCommentSerializer(serializers.ModelSerializer):
    class PostSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = '__all__'
    
    post = PostSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

class UserReviewSerializer(serializers.ModelSerializer):
    movie_data = MovieSerializer(source='movie', read_only=True)  

    class Meta:
        model = Review
        fields = ['user', 'movie', 'title', 'content', 'rating', 'created_at', 'movie_data'] 



class UserDetailsSerializer(serializers.ModelSerializer):
    followings_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()
    liked_movies = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_image', 'username', 'nickname', 'followings_count', 'followers_count', 'review_count',
                  'posts', 'liked_movies', 'review'] 

    def get_followings_count(self, obj):
        return obj.followings.count()

    def get_followers_count(self, obj):
        return obj.followers.count()
    
    def get_review_count(self, obj):
        return Review.objects.filter(user=obj).count()
    
    def get_posts(self, obj):
        posts = Post.objects.filter(user=obj)
        return UserPostSerializer(posts, many=True).data

    def get_liked_movies(self, obj):
        movies = Movie.objects.filter(likes=obj)
        return UserMovieSerializer(movies, many=True).data
    
    def get_review(self, obj):
        review = Review.objects.filter(user=obj)
        return UserReviewSerializer(review, many=True).data


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(
      required=False,
      allow_blank=True,
      max_length=255
    )

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'nickname': self.validated_data.get('nickname', ''),
            'email': self.validated_data.get('email', ''),
        }
    

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        extra_fields = []
        # see https://github.com/iMerica/dj-rest-auth/issues/181
        # UserModel.XYZ causing attribute error while importing other
        # classes from `serializers.py`. So, we need to check whether the auth model has
        # the attribute or not
        if hasattr(User, 'USERNAME_FIELD'):
            extra_fields.append(User.USERNAME_FIELD)
        if hasattr(User, 'EMAIL_FIELD'):
            extra_fields.append(User.EMAIL_FIELD)
        if hasattr(User, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(User, 'last_name'):
            extra_fields.append('last_name')
        if hasattr(User, 'nickname'):
            extra_fields.append('nickname')    
        model = User
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)


class FindUserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

