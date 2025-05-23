# kkubook/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Bookworm

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
