from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Comment, Post, Community
from django.shortcuts import get_list_or_404, get_object_or_404
from .serializers import CategorySerializer, CommentSerializer, PostSerializer
from django.contrib.auth.decorators import login_required
# Create your views here.


@api_view(['GET', 'POST'])
def post(request):
    if request.method == 'GET':
        posts = get_list_or_404(Post)
        category = get_list_or_404(Category)
        postSerializer = PostSerializer(posts, many=True)
        categorySerializer = CategorySerializer(category, many=True)
        context = {
            'posts': postSerializer.data,
            'category': categorySerializer.data
        }
        return JsonResponse(context)
    
    elif request.method == 'POST':
        print(request.data)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
@login_required
def detail(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=post_id)
        post.click_count += 1
        post.save()
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        post = get_object_or_404(Post, pk=post_id)
        serializer = PostSerializer(post, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        post = get_object_or_404(Post, pk=post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        


@api_view(['POST'])
@login_required
def detail_like(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            is_liked = False
            context = {
                'is_liked': is_liked,
                'like_count': post.likes.count(),
            }
        
        else:
            post.likes.add(request.user)
            is_liked = True
            context = {
                'is_liked': is_liked,
                'like_count': post.likes.count(),
            }
        return Response(context, status=status.HTTP_200_OK)


@api_view(['PUT', 'DELETE'])
@login_required
def editPost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'PUT' and request.user == post.user:
        serializer = PostSerializer(instance=post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE' and request.user == post.user:
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'GET'])
@login_required
def comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        comments = Comment.objects.filter(post=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['PUT'])
@login_required
def commentUpdate(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'PUT' and request.user == comment.user:
        post = get_object_or_404(Post, pk=post_id)
        serializer = CommentSerializer(instance=comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@login_required
def commentDelete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'DELETE' and request.user == comment.user:
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)