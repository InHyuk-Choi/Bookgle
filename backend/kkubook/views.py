from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Bookworm, Pheed, Comment
from .serializers import PheedSerializer, CommentSerializer


# 📌 [1] 책벌레 상태 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_bookworm_status(request):
    bookworm, _ = Bookworm.objects.get_or_create(owner=request.user)
    progress = bookworm.experience / bookworm.experience_to_next_level()
    return Response({
        "name": bookworm.name,
        "level": bookworm.level,
        "experience": bookworm.experience,
        "exp_to_next": bookworm.experience_to_next_level(),
        "progress": round(progress, 3), # 경험치바 용도
    })


# 📌 [2] 책벌레 먹이주기 (먹이 소모 + 경험치 증가 + 레벨업 처리)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def feed_bookworm(request):
    bookworm, _ = Bookworm.objects.get_or_create(owner=request.user)
    user = request.user
    food_type = request.data.get('type')

    # 먹이 타입에 따라 경험치량 다르게 설정
    if food_type == 'basic':
        if user.basic_food < 1:
            return Response({'error': '일반 먹이가 부족합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        user.basic_food -= 1
        gain_exp = 10

    elif food_type == 'premium':
        if user.premium_food < 1:
            return Response({'error': '고급 먹이가 부족합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        user.premium_food -= 1
        gain_exp = 40

    else:
        return Response({'error': '유효하지 않은 먹이 타입입니다.'}, status=status.HTTP_400_BAD_REQUEST)

    # 경험치 부여 및 레벨업 처리
    bookworm.add_experience(gain_exp)
    user.save()

    return Response({
        "message": f"{food_type} 먹이를 먹였습니다. 경험치 +{gain_exp}",
        "level": bookworm.level,
        "experience": bookworm.experience,
        "exp_to_next": bookworm.experience_to_next_level(),
        "basic_food": user.basic_food,
        "premium_food": user.premium_food,
    })

# 피드 전체 조회
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def list_create_pheeds(request):
    if request.method == 'GET':
        pheeds = Pheed.objects.all().order_by('-created_at')
        serializer = PheedSerializer(pheeds, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PheedSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            pheed = serializer.save(user=request.user)
            request.user.total_points += 10
            request.user.save()
            return Response(PheedSerializer(pheed, context={'request': request}).data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])  # ← 여기에 GET 추가!
@permission_classes([IsAuthenticated])
def update_delete_pheed(request, pheed_id):
    pheed = get_object_or_404(Pheed, id=pheed_id)

    if request.method == 'GET':
        serializer = PheedSerializer(pheed, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        if pheed.user != request.user:
            return Response({'error': '수정 권한 없음'}, status=403)
        serializer = PheedSerializer(pheed, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if pheed.user != request.user:
            return Response({'error': '삭제 권한 없음'}, status=403)
        pheed.delete()
        return Response({'message': '피드 삭제 완료'}, status=204)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_pheeds(request):
    pheeds = Pheed.objects.filter(user=request.user).order_by('-created_at')
    serializer = PheedSerializer(pheeds, many=True, context={'request': request})
    return Response(serializer.data)


# 피드 좋아요/취소
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like_pheed(request, pheed_id):
    pheed = get_object_or_404(Pheed, id=pheed_id)
    user = request.user

    if user in pheed.like_users.all():
        pheed.like_users.remove(user)
        liked = False
    else:
        pheed.like_users.add(user)
        liked = True

    return Response({
        'liked': liked,
        'like_count': pheed.like_users.count()
    })



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def list_create_comments(request, pheed_id):
    pheed = get_object_or_404(Pheed, id=pheed_id)

    if request.method == 'GET':
        comments = pheed.comments.all().order_by('created_at')
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            comment = serializer.save(user=request.user, pheed=pheed)
            request.user.total_points += 3
            request.user.save()
            return Response(CommentSerializer(comment, context={'request': request}).data, status=201)
        return Response(serializer.errors, status=400)
    

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)

    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        comment.delete()
        return Response({'message': '댓글 삭제 완료'}, status=204)
