from rest_framework import serializers
from .models import Pheed, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname','profile_image',]

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