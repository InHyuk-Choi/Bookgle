from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

# 유저 정보 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail_view(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'nickname': user.nickname,
        'total_points': user.total_points,
        'read_pages': user.total_pages_read,
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
