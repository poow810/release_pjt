from itertools import combinations
import random
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.models import Review
from .models import Movie, Genre
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from .serializers import MovieSerializer, GenreSerializer, ReviewSerializer
from django.db.models import Count, Q


@api_view(['GET'])
def getMovies(request, movie_id):
    if request.method == 'GET':
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_genre(request):
    if request.method == 'GET':
        movies = get_list_or_404(Movie)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@login_required
def genre_select(request):
    if request.method == 'GET':
        genreIds = request.GET.getlist('genre[]')
        movies = Movie.objects.annotate(num_genres=Count('genres', filter=Q(genres__id__in=genreIds))
        ).filter(num_genres__gt=0).order_by('-num_genres', '-popularity')[:20]
        serializer = MovieSerializer(movies, many=True)
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
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@login_required
def review(request, movie_id):
    if request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        movie = get_object_or_404(Movie, movie_id=movie_id)
        if serializer.is_valid():
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        movie = get_object_or_404(Movie, movie_id=movie_id)
        reviews = Review.objects.filter(movie=movie, user=request.user)
        if reviews.exists():
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "리뷰가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        
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
    if not text:
        return Response({"error": "No search text provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    # 검색어를 포함하는 영화 검색
    movies = Movie.objects.filter(title__icontains=text).distinct()
    movie_count = movies.count()
    
    if movie_count == 0:
        return Response({"message": "No movies found"}, status=status.HTTP_404_NOT_FOUND)
    
    # 검색 결과가 10개 이상인 경우 바로 반환
    if movie_count >= 10:
        serializer = MovieSerializer(movies[:10], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 장르 기반 추가 영화 검색
    genre_ids = movies.values_list('genres', flat=True).distinct()
    additional_movies = Movie.objects.none()
    
    for i in range(len(genre_ids), 0, -1):
        if movie_count >= 10:
            break
        genre_combinations = combinations(genre_ids, i)
        selected_movies = Movie.objects.none()

        for combination in genre_combinations:
            # 현재 선택된 영화의 수
            current_count = selected_movies.count()
            
            # 필요한 영화의 수를 계산 (최대 10개)
            needed = 10 - current_count
            
            # 현재 조합에 맞는 영화들을 필터링 (단, 이미 선택된 영화는 제외)
            additional_movies = Movie.objects.filter(genres__id__in=combination).exclude(id__in=selected_movies).distinct()[:needed]
            
            # 추가된 영화를 selected_movies에 추가
            selected_movies = selected_movies | additional_movies
            
            # 만약 10개의 영화를 모두 찾았다면 반복 종료
            if selected_movies.count() >= 10:
                break

    final_movies = list(movies)
    if 10 - len(final_movies) > 0:
        final_movies += list(additional_movies[:10 - len(final_movies)])
    
    if final_movies:
        serializer = MovieSerializer(final_movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)