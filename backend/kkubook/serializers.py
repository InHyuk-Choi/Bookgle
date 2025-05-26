from rest_framework import serializers
from .models import Pheed, Comment, Book, Review
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSimpleSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'profile_image'] 

    def get_profile_image(self, obj):
        request = self.context.get('request')
        if obj.profile_image:
            return request.build_absolute_uri(obj.profile_image.url)
        return request.build_absolute_uri('/media/default-profile.png')
class CommentSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'updated_at']

class PheedSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    like_users_count = serializers.IntegerField(source='like_users.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.like_users.all()
        return False

    class Meta:
        model = Pheed
        fields = ['id', 'user', 'content', 'image', 'like_users_count', 'comments_count', 'comments', 'created_at', 'updated_at', 'is_liked']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'publisher', 'cover_image', 'description']

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'username', 'content', 'rating', 'created_at']
        read_only_fields = ['user', 'created_at']