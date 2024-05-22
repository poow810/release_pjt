from rest_framework import serializers
from .models import Category, Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'username', 'nickname')

    user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'content','created_at','updated_at','click_count', 'user', 'category' ,'likes_count', 'comments_count', 'is_liked_by_user')

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return Comment.objects.filter(post=obj).count()

    def get_is_liked_by_user(self, obj):
        request = self.context.get('request', None)
        if request is not None and not request.user.is_anonymous:
            return obj.likes.filter(id=request.user.id).exists()
        return False
       

class CommentSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'nickname', 'user_image')

    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_at', 'user')
        read_only_fields = ('user', 'post')