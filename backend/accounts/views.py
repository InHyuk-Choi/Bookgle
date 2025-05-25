from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from .serializers import FollowUserSerializer, ProfileImageSerializer, RankingUserSerializer
from kkubook.models import Bookworm
from accounts.serializers import BookwormRankingSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


User = get_user_model()


# JWT 쿠키 로그인
@api_view(['POST'])
def custom_login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({'error': '로그인 실패'}, status=401)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    response = Response({'access': access_token})  # access는 JSON으로 전달
    response.set_cookie(
        key='refresh_token',
        value=str(refresh),
        httponly=True,
        secure=False,  # 배포 시 True
        samesite='Lax',
        max_age=60 * 60 * 24 * 7,  # 7일
    )
    return response


# JWT 쿠키 로그아웃
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def custom_logout_view(request):
    response = Response({'message': '로그아웃 성공'})
    response.delete_cookie('refresh_token')
    return response

# Access 토큰 만료시 Refresh 토큰으로 재발급
@api_view(['POST'])
def refresh_access_token_view(request):
    refresh_token = request.COOKIES.get('refresh_token')
    if not refresh_token:
        return Response({'error': 'Refresh token이 없습니다.'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)
        return Response({'access': access_token}, status=status.HTTP_200_OK)
    except TokenError:
        return Response({'error': '유효하지 않은 refresh token입니다.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail_view(request):
    user = request.user

    try:
        latest_record = user.readingrecord_set.filter(is_finished=False).order_by('-created_at').first()
        current_book_title = latest_record.book.title if latest_record and latest_record.book else None
        read_pages = latest_record.pages if latest_record else 0
    except Exception as e:
        print(f"[DEBUG] 책 제목 조회 실패: {e}")
        current_book_title = None
        read_pages = 0

    profile_url = (
        request.build_absolute_uri(user.profile_image.url)
        if user.profile_image
        else request.build_absolute_uri('/media/default-profile.png')
    )

    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'nickname': user.nickname,
        'total_points': user.total_points,
        'read_pages': read_pages,  # ✅ 여기!
        'followers_count': user.followers.count(),
        'following_count': user.following.count(),
        'basic_food': user.basic_food,
        'premium_food': user.premium_food,
        'profile_image': profile_url,
        'current_book_title': current_book_title,
    })




# 포인트 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_points(request):
    return Response({'total_points': request.user.total_points})


# 포인트 추가
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_user_points(request):
    amount = int(request.data.get('amount', 0))
    request.user.total_points += amount
    request.user.save()
    return Response({'total_points': request.user.total_points})


# 포인트 차감
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subtract_user_points(request):
    amount = int(request.data.get('amount', 0))
    if request.user.total_points >= amount:
        request.user.total_points -= amount
        request.user.save()
        return Response({'total_points': request.user.total_points})
    return Response({'error': '잔여 포인트 부족'}, status=status.HTTP_400_BAD_REQUEST)

# 페이지 수 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_pages(request):
    return Response({'total_pages_read': request.user.total_pages_read})


# 페이지 수 갱신
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_user_pages(request):
    try:
        pages = int(request.data.get('pages', 0))
        if pages < 0:
            raise ValueError("음수는 안됨")
    except:
        return Response({'error': '유효한 페이지 수를 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)

    request.user.total_pages_read = pages
    request.user.save()
    return Response({'total_pages_read': request.user.total_pages_read})

# 먹이 구매
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def purchase_food(request):
    food_type = request.data.get('type')
    quantity = int(request.data.get('quantity', 1))
    cost = int(request.data.get('cost', 0))

    user = request.user

    if food_type == 'basic':
        if user.total_points < cost:
            return Response({'error': '포인트가 부족합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        user.total_points -= cost
        user.basic_food += quantity

    elif food_type == 'premium':
        if user.total_points < cost:
            return Response({'error': '포인트가 부족합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        user.total_points -= cost
        user.premium_food += quantity

    else:
        return Response({'error': '잘못된 음식 유형입니다.'}, status=status.HTTP_400_BAD_REQUEST)

    user.save()
    return Response({
        'total_points': user.total_points,
        'basic_food': user.basic_food,
        'premium_food': user.premium_food,
    })



# 팔로우/언팔로우
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_follow(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    user = request.user

    if target_user == user:
        return Response({"detail": "자기 자신은 팔로우할 수 없습니다."}, status=400)

    if target_user in user.following.all():
        user.following.remove(target_user)
        return Response({"detail": "언팔로우 완료"}, status=200)
    else:
        user.following.add(target_user)
        return Response({"detail": "팔로우 완료"}, status=200)

# views.py
@api_view(['GET'])
@permission_classes([AllowAny])
def user_followers(request, username):
    user = get_object_or_404(User, username=username)
    followers = user.followers.all()
    serializer = FollowUserSerializer(followers, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def user_following(request, username):
    user = get_object_or_404(User, username=username)
    following = user.following.all()
    serializer = FollowUserSerializer(following, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_following(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    user = request.user
    is_following = target_user in user.following.all()
    return Response({"is_following": is_following})



# 프로필 이미지 업로드
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_profile_image(request):
    user = request.user
    serializer = ProfileImageSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'profile_image': serializer.data['profile_image']})
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([AllowAny])
def bookworm_ranking(request):
    bookworms = Bookworm.objects.select_related('owner').all().order_by('-level', '-experience')[:50]

    serializer = BookwormRankingSerializer(
            bookworms,
            many=True,
            context={'request': request}  # ← 이거 추가!
        )

    # rank 번호 붙이기
    response_data = serializer.data
    for idx, user in enumerate(response_data, start=1):
        user['rank'] = idx

    return Response(response_data)



# views.py 하단에 추가
@api_view(['GET'])
@permission_classes([AllowAny])
def user_profile_by_username(request, username):
    user = get_object_or_404(User, username=username)

    profile_url = (
        request.build_absolute_uri(user.profile_image.url)
        if user.profile_image
        else request.build_absolute_uri('/media/default-profile.png')
    )

    serializer = FollowUserSerializer(user, context={'request': request})
    return Response({
        **serializer.data,
        'email': user.email,
        'total_points': user.total_points,
        'read_pages': user.total_pages_read,
        'basic_food': user.basic_food,
        'premium_food': user.premium_food,
        'profile_image': profile_url,
    })
