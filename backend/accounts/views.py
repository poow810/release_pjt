from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from .serializers import FindUserNameSerializer, UserCommentSerializer, UserMovieSerializer, UserPostSerializer, UserDetailsSerializer
from community.models import Comment, Post

User = get_user_model()

@api_view(['POST'])
def findId(request, email):
    username = get_object_or_404(User, email=email)
    serializer = FindUserNameSerializer(username)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
@login_required
def profile(request, user_id):
    if request.method == 'GET':
        person = get_object_or_404(User, pk=user_id)
        serializer = UserDetailsSerializer(person)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        person = get_object_or_404(User, pk=user_id)
        user_img = request.data['user_image']
        person.user_image = user_img
        person.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
@login_required
def changeNickname(request, user_id):
    if request.method == 'PUT':
        person = get_object_or_404(User, pk=user_id)
        print(request.data)
        person.nickname = request.data['nickname']
        person.save()
        context = {
            'nickname': person.nickname
        }
        return Response(context)

@api_view(['POST'])
@login_required
def follow(request, user_pk):
    person = get_object_or_404(User, pk=user_pk)
    if person != request.user:
        if person.followers.filter(pk=request.user.pk).exists():
            person.followers.remove(request.user)
            is_followed = False
        else:
            person.followers.add(request.user)
            is_followed = True
        context = {
            'is_followed': is_followed,
            'follower_count': person.followers.count(),
            'following_count': person.followings.count(),
        }
        return Response(context)
    return Response(status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@login_required
def posts(request, user_id):
    if request.method == 'GET':
        posts = get_list_or_404(Post, user=user_id)
        serializer = UserPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

@api_view(['GET'])
@login_required
def movies(request, user_id):
    if request.method == 'GET':
        user = get_object_or_404(User, id=user_id)
        liked_movies = user.liked_movies.all()
        serializer = UserMovieSerializer(liked_movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

@api_view(['GET'])
@login_required
def comments(request, user_id):
    if request.method == 'GET':
        comments = get_list_or_404(Comment, user=user_id)
        serializer = UserCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)