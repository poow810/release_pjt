from itertools import combinations
import os
import random
import re
from django.conf import settings
from django.http import JsonResponse
from openai import OpenAI
import openai
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import Review
from .models import Movie, Genre, Person
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from .serializers import MovieGenreSerializer, MovieSerializer, GenreSerializer, PersonSerializer, ReviewDetailSerializer, ReviewSerializer
from django.db.models import Count, Q

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
client = OpenAI(
    # This is the default and can be omitted
    api_key=settings.OPENAI_API_KEY,
)


@api_view(['GET'])
def getMovies(request, movie_id):
    if request.method == 'GET':
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieSerializer(movie, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@login_required
def genre_select(request):
    if request.method == 'GET':
        genreIds = request.GET.getlist('genre[]')
        movies = Movie.objects.annotate(num_genres=Count('genres', filter=Q(genres__id__in=genreIds))
        ).filter(num_genres__gt=0).order_by('-num_genres', '-popularity')[:20]
        serializer = MovieGenreSerializer(movies, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['POST'])
@login_required
def movie_like(request, movie_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, movie_id=movie_id)
        if request.user in movie.likes.all():
            movie.likes.remove(request.user)
            is_liked = False
            context = {
                'is_liked': is_liked,
                'like_count': movie.likes.count(),
            }
        
        else:
            movie.likes.add(request.user)
            is_liked = True
            context = {
                'is_liked': is_liked,
                'like_count': movie.likes.count(),
            }
        return Response(context, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@login_required
def detail(request, movie_id):
    if request.method == 'GET':
        movie = get_object_or_404(Movie, movie_id=movie_id)
        serializer = MovieSerializer(movie, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@login_required
def review(request, movie_id):
    if request.method == 'POST':
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        movie = get_object_or_404(Movie, movie_id=movie_id)
        if serializer.is_valid():
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        movie = get_object_or_404(Movie, movie_id=movie_id)
        reviews = Review.objects.filter(movie=movie)
        if reviews.exists():
            serializer = ReviewSerializer(reviews, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "리뷰가 없습니다."}, status=status.HTTP_404_NOT_FOUND) 
        

@api_view(['GET'])
@login_required
def detailReview(request, review_id):
    if request.method == 'GET':
        review = get_object_or_404(Review, pk=review_id)
        serializer = ReviewDetailSerializer(review, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@login_required
def weather(request, genre_id):
    if request.method == 'GET':
        genre = get_object_or_404(Genre, id=genre_id)
        
        movies = Movie.objects.filter(genres=genre)        
        if movies:
            random_movie = random.choice(movies)
            
            movie_data = {
                'movie_id': random_movie.movie_id,
                'title': random_movie.title,
                'poster_path': random_movie.poster_path,
                'overview': random_movie.overview,
                'release_date': random_movie.release_date,
                'vote_avg': float(random_movie.vote_avg),
                'popularity': float(random_movie.popularity),
            }
            
            return JsonResponse(movie_data)
        else:
            return JsonResponse({'message': '해당 장르의 영화가 없습니다.'}, status=404)
        

@api_view(['GET'])
def search(request):
    text = request.GET.get('text')
    search_type = request.GET.get('type')  # 검색 타입 (영화, 배우)

    if not text:
        return Response({"error": "No search text provided"}, status=status.HTTP_400_BAD_REQUEST)

    movies = Movie.objects.none()
    persons = Person.objects.none()
    if search_type == '영화':
        movies = Movie.objects.filter(title__icontains=text).distinct()
    elif search_type == '이름':
        persons = Person.objects.filter(name_kr__icontains=text).distinct()
    else:
        return Response({"error": "Invalid search type"}, status=status.HTTP_400_BAD_REQUEST)

    movie_count = movies.count()
    person_count = persons.count()

    # 영화와 배우 검색 결과 합치기
    total_count = movie_count + person_count

    if total_count >= 10:
        movie_serializer = MovieSerializer(movies[:10], many=True, context={'request': request})
        person_serializer = PersonSerializer(persons[:10 - movie_count], many=True, context={'request': request})
        data = movie_serializer.data + person_serializer.data
        return Response(data, status=status.HTTP_200_OK)

    # 장르 기반 추가 영화 검색
    if movie_count > 0:
        genre_ids = movies.values_list('genres', flat=True).distinct()
        additional_movies = Movie.objects.none()

        for i in range(len(genre_ids), 0, -1):
            if total_count >= 10:
                break
            genre_combinations = combinations(genre_ids, i)
            selected_movies = Movie.objects.none()

            for combination in genre_combinations:
                current_count = selected_movies.count()
                needed = 10 - total_count

                additional_movies = Movie.objects.filter(genres__id__in=combination).exclude(id__in=selected_movies).distinct()
                additional_movies = additional_movies.annotate(genre_count=Count('genres')).order_by('-genre_count')[:needed]

                selected_movies = selected_movies | additional_movies
                total_count += selected_movies.count()

                if total_count >= 10:
                    break

        movies = list(movies) + list(selected_movies[:10 - len(movies)])

    movie_serializer = MovieSerializer(movies, many=True, context={'request': request})
    person_serializer = PersonSerializer(persons, many=True, context={'request': request})
    data = movie_serializer.data + person_serializer.data

    return Response(data, status=status.HTTP_200_OK)



genre_list = [
    { 'id': 28, 'name': "action"},
    { 'id': 12, 'name': "adventure"},
    { 'id': 16, 'name': "animation"},
    { 'id': 35, 'name': "comedy"},
    { 'id': 80, 'name': "crime"},
    { 'id': 99, 'name': "documentary"},
    { 'id': 18, 'name': "drama"},
    { 'id': 10751, 'name': "family"},
    { 'id': 14, 'name': "fantasy"},
    { 'id': 36, 'name': "history"},
    { 'id': 27, 'name': "horror"},
    { 'id': 10402, 'name': "music"},
    { 'id': 9648, 'name': "mystery"},
    { 'id': 10749, 'name': "romance"},
    { 'id': 878, 'name': "science fiction"},
    { 'id': 10770, 'name': "tv Movie"},
    { 'id': 53, 'name': "thriller"},
    { 'id': 10752, 'name': "war"},
    { 'id': 37, 'name': "western"}
]


def random_select(genres):
    movies_with_genres = Movie.objects.annotate(
        genres_count=Count(
            'genres', filter=Q(genres__id__in=genres)
        )
    ).order_by('-genres_count', '?')
    max_genres_count = movies_with_genres.first().genres_count if movies_with_genres.exists() else 0

    movies_with_max_genres = movies_with_genres.filter(genres_count=max_genres_count)
    selected_movie = random.choice(list(movies_with_max_genres)) if movies_with_max_genres else None

    return selected_movie


def find_genre(genres):
    genre_names = []
    for genre in genres:
        genre = Genre.objects.get(id=genre)
        genre_names.append(genre.name)
    
    return genre_names


@api_view(['GET'])
@login_required
def recommend(request):
    if request.method == 'GET':
        weather_data = request.query_params.get('weather', '')
        
        genre_recommendation_ids = recommendWeather(weather_data)
        recommend_movie = random_select(genre_recommendation_ids)
        if recommend_movie:
            genres_names = find_genre(genre_recommendation_ids)
            serializer = MovieSerializer(recommend_movie, context={'request': request})
            return Response({'recommend': serializer.data, 'genres': genres_names })
        else:
            return Response({'message': '추천할 영화가 없습니다.'})

def findGenreIdsByNames(genre_names):
    genre_ids = [genre['id'] for genre in genre_list if genre['name'] in genre_names]
    return genre_ids

def recommendWeather(weather):
    genre_names = [genre['name'] for genre in genre_list]
    genre_names_str = ', '.join(genre_names)
    question = f"The weather today is {weather}. Based on the following genres: {genre_names_str}, what movie genres would be suitable for this weather? Please recommend two genres and answer in the form of **genre**."
    try:
        chat_completion = client.chat.completions.create(
        messages=[
            {
            "role": "user",
            "content": question
            }
        ],
        model="gpt-4o",
        )
        response_text = chat_completion.choices[0].message.content.strip()
        
        genre_pattern = re.compile(r'\*\*([\w\s/]+)\*\*')
        recommended_genres = genre_pattern.findall(response_text)

        return findGenreIdsByNames(recommended_genres)
    
    except Exception as e:
        print(f"Error occurred while calling the OpenAI API: {e}")
        return []
    
