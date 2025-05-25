from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from datetime import date
from .models import ReadingRecord   
import requests

from .models import Bookworm, Pheed, Comment, Book, ReadingRecord, Question
from .serializers import PheedSerializer, CommentSerializer



User = get_user_model()


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


@api_view(['GET'])
@permission_classes([AllowAny])
def user_pheeds_by_username(request, username):
    user = get_object_or_404(User, username=username)
    pheeds = Pheed.objects.filter(user=user).order_by('-created_at')
    serializer = PheedSerializer(pheeds, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_pages(request):
    try:
        pages = int(request.data.get('pages', 0))
        if pages < 0:
            raise ValueError("음수는 안됨")
    except:
        return Response({'error': '유효한 페이지 수를 입력하세요.'}, status=400)

    # ✅ 아직 완독하지 않은 가장 최근 기록 하나 찾기
    record = ReadingRecord.objects.filter(
        user=request.user,
        is_finished=False
    ).order_by('-created_at').first()

    if not record:
        return Response({'error': '진행 중인 책이 없습니다.'}, status=400)

    # ✅ 하루 한 번만 기록
    if record.last_updated == timezone.now().date():
        return Response({'already_recorded': True})

    record.pages = pages
    record.last_updated = timezone.now().date()
    record.save()

    # ✅ 포인트 지급 등 다른 로직 있으면 여기 추가

    return Response({'message': '페이지 기록 완료', 'already_recorded': False})





ALADIN_API_KEY = settings.ALADIN_API_KEY
ALADIN_API_URL = 'https://www.aladin.co.kr/ttb/api/ItemSearch.aspx'

# 📘 [1] 책 검색 (GET) 알라딘 API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_books(request):
    query = request.GET.get('q', '')
    query_type = request.GET.get('type', 'Title')
    if not query:
        return Response({'error': '검색어(q)는 필수입니다.'}, status=400)

    params = {
        'ttbkey': ALADIN_API_KEY,
        'Query': query,
        'QueryType': query_type,
        'MaxResults': 10,
        'start': 1,
        'SearchTarget': 'Book',
        'output': 'js',
        'Version': '20131101',
        'Cover': 'Big',
    }

    try:
        response = requests.get(ALADIN_API_URL, params=params)
        response.raise_for_status()
        items = response.json().get('item', [])
    except Exception as e:
        return Response({'error': '알라딘 API 요청 실패', 'detail': str(e)}, status=500)

    # 필요한 필드만 추출
    results = []
    for item in items:
        results.append({
            'isbn': item.get('isbn13'),
            'title': item.get('title'),
            'author': item.get('author'),
            'publisher': item.get('publisher'),
            'cover_image': item.get('cover'),
        })

    return Response(results)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_book(request):
    user = request.user

    # 이미 등록된 책이 있는지 확인
    existing_record = ReadingRecord.objects.filter(
        user=user,
        created_at=timezone.now().date(),
        is_finished=False
    ).first()

    if existing_record:
        return Response({'error': '오늘은 이미 책을 등록했어요! 먼저 완독을 완료하세요!'}, status=400)

    isbn = request.data.get('isbn')
    title = request.data.get('title')
    author = request.data.get('author')
    publisher = request.data.get('publisher')
    cover_image = request.data.get('cover_image')

    if not all([isbn, title]):
        return Response({'error': 'isbn과 title은 필수입니다.'}, status=400)

    book, _ = Book.objects.get_or_create(
        isbn=isbn,
        defaults={
            'title': title,
            'author': author,
            'publisher': publisher,
            'cover_image': cover_image,
        }
    )

    ReadingRecord.objects.create(
        user=user,
        book=book,
        pages=0
    )

    return Response({
        'message': '책 등록 및 읽기 시작 완료',
        'book_id': book.id,
        'title': book.title,
        'start_page': 0,
    }, status=201)


# views.py
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def finish_current_book(request):
    title = request.data.get('book_title')
    record = request.user.readingrecord_set.filter(book__title=title, is_finished=False).first()

    if record:
        record.is_finished = True
        record.save()
        return Response({'message': '완독 처리 완료'})

    return Response({'error': '기록을 찾을 수 없습니다.'}, status=404)
