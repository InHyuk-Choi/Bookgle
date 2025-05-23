from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import User

# 유저 커스터마이징
class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', '')
        return data

    def save(self, request):
        user = super().save(request)
        user.nickname = self.validated_data.get('nickname', '')
        user.save()
        return user

# 팔로우 시리얼라이저
class FollowUserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'followers_count', 'following_count', 'is_following']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj in request.user.following.all()
        return False

class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_image']