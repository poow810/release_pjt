from itertools import combinations
import random
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.models import Review
from .models import Movie, Genre, Person
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from .serializers import MovieGenreSerializer, MovieSerializer, GenreSerializer, PersonSerializer, ReviewDetailSerializer, ReviewSerializer
from django.db.models import Count, Q


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
        serializer = ReviewSerializer(data=request.data, many=True, context={'request': request})
        movie = get_object_or_404(Movie, movie_id=movie_id)
        if serializer.is_valid():
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
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
    print(request)
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