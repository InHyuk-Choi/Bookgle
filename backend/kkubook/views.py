from datetime import date
import json
import re
import requests

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import IntegrityError

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import ReadingRecord, Bookworm, Pheed, Comment, Book, Question, Review
from .serializers import PheedSerializer, CommentSerializer, BookSerializer, ReviewSerializer
from .utils.gemini import generate_quiz_with_gemini, extract_keywords_with_gemini
from .utils.aladinbooks import search_books_on_aladin
from .utils.naverbooks import search_books_on_naver

User = get_user_model()

# 📌 [GET] /bookworm/status/
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
        "progress": round(progress, 3),
    })

# 📌 [POST] /bookworm/feed/
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def feed_bookworm(request):
    bookworm, _ = Bookworm.objects.get_or_create(owner=request.user)
    user = request.user
    food_type = request.data.get('type')

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

# 📌 [GET, POST] /pheeds/
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

# 📌 [GET, PUT, PATCH, DELETE] /pheeds/<int:pheed_id>/
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
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
    elif request.method == 'PATCH':
        if pheed.user != request.user:
            return Response({'error': '수정 권한 없음'}, status=403)
        serializer = PheedSerializer(pheed, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        if pheed.user != request.user:
            return Response({'error': '삭제 권한 없음'}, status=403)
        pheed.delete()
        return Response({'message': '피드 삭제 완료'}, status=204)

# 📌 [POST] /pheeds/<int:pheed_id>/like/
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

# 📌 [GET] /pheeds/me/
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_pheeds(request):
    pheeds = Pheed.objects.filter(user=request.user).order_by('-created_at')
    serializer = PheedSerializer(pheeds, many=True, context={'request': request})
    return Response(serializer.data)

# 📌 [GET] /pheeds/user/<str:username>/
@api_view(['GET'])
@permission_classes([AllowAny])
def user_pheeds_by_username(request, username):
    user = get_object_or_404(User, username=username)
    pheeds = Pheed.objects.filter(user=user).order_by('-created_at')
    serializer = PheedSerializer(pheeds, many=True, context={'request': request})
    return Response(serializer.data)

# 📌 [GET, POST] /pheeds/<int:pheed_id>/comments/
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

# 📌 [PUT, DELETE] /comments/<int:comment_id>/
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

# 📌 [POST] /pages/set/
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_pages(request):
    try:
        pages = int(request.data.get('pages', 0))
        if pages < 0:
            raise ValueError("음수는 안됨")
    except:
        return Response({'error': '유효한 페이지 수를 입력하세요.'}, status=400)

    record = ReadingRecord.objects.filter(
        user=request.user,
        is_finished=False
    ).order_by('-created_at').first()

    if not record:
        return Response({'error': '진행 중인 책이 없습니다.'}, status=400)

    if record.last_updated == timezone.now().date():
        return Response({'already_recorded': True})

    record.pages = pages
    record.last_updated = timezone.now().date()
    record.save()

    return Response({'message': '페이지 기록 완료', 'already_recorded': False})

# 📌 [GET] /books/search/
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_books(request):
    query = request.GET.get('q', '')
    query_type = request.GET.get('type', 'Title')
    if not query:
        return Response({'error': '검색어(q)는 필수입니다.'}, status=400)

    naver_headers = {
        'X-Naver-Client-Id': settings.NAVER_CLIENT_ID,
        'X-Naver-Client-Secret': settings.NAVER_CLIENT_SECRET,
    }

    aladin_params = {
        'ttbkey': settings.ALADIN_API_KEY,
        'Query': query,
        'QueryType': query_type if query_type in ['Title', 'Author', 'ISBN'] else 'Title',
        'MaxResults': 10,
        'start': 1,
        'SearchTarget': 'Book',
        'output': 'js',
        'Version': '20131101',
        'Cover': 'Big',
    }

    try:
        response = requests.get('https://www.aladin.co.kr/ttb/api/ItemSearch.aspx', params=aladin_params, timeout=5)
        response.raise_for_status()
        items = response.json().get('item', [])

        results = []
        for item in items:
            results.append({
                'isbn': item.get('isbn13'),
                'title': item.get('title'),
                'author': item.get('author'),
                'publisher': item.get('publisher'),
                'cover_image': item.get('cover'),
                'description': item.get('description'),
            })

        if results:
            return Response(results)

    except Exception as e:
        print(f"❌ 알라딘 API 실패: {e}")
        print("🔄 네이버 API로 우회 시도")

    try:
        naver_params = {
            'query': query,
            'display': 10,
            'start': 1,
            'sort': 'sim',
        }
        response = requests.get("https://openapi.naver.com/v1/search/book.json", headers=naver_headers, params=naver_params, timeout=5)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get('items', []):
            isbn = item.get('isbn', '')
            isbn13 = isbn.split()[-1] if ' ' in isbn else isbn

            results.append({
                'isbn': isbn13,
                'title': item.get('title'),
                'author': item.get('author'),
                'publisher': item.get('publisher'),
                'cover_image': item.get('image'),
                'description': item.get('description'),
            })

        return Response(results)

    except Exception as e:
        return Response({'error': '책 검색 실패 (알라딘, 네이버 모두)', 'detail': str(e)}, status=500)

# 📌 [POST] /books/register/
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_book(request):
    user = request.user

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
    description = request.data.get('description', '')

    if not all([isbn, title]):
        return Response({'error': 'isbn과 title은 필수입니다.'}, status=400)

    book, _ = Book.objects.get_or_create(
        isbn=isbn,
        defaults={
            'title': title,
            'author': author,
            'publisher': publisher,
            'cover_image': cover_image,
            'description': description,
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

# 📌 [POST] /books/finish/
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def finish_current_book(request):
    title = request.data.get('book_title')
    record = request.user.readingrecord_set.filter(is_finished=False).first()
    if record and title in record.book.title:
        record.is_finished = True
        record.save()
        return Response({'message': '완독 처리 완료'})
    return Response({'error': '기록을 찾을 수 없습니다.'}, status=404)

# 📌 [GET] /books/recommend/
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_books(request):
    user = request.user
    books = Book.objects.filter(readingrecord__user=user).distinct()
    if not books.exists():
        return Response({'error': '추천을 위해 등록된 책이 없습니다.'}, status=400)

    all_genres = set()
    all_keywords = set()

    for book in books:
        if not book.genres or not book.keywords:
            try:
                result = extract_keywords_with_gemini(book.title, book.description or "")
                book.genres = result.get("genres", [])
                book.keywords = result.get("keywords", [])
                book.save()
            except Exception as e:
                print(f"❌ Gemini 추출 실패 ({book.title}): {e}")
                continue

        all_genres.update(book.genres)
        all_keywords.update(book.keywords)

    if not (all_genres or all_keywords):
        return Response({'error': '추천 키워드 생성에 실패했습니다.'}, status=500)

    combined_terms = list(all_genres.union(all_keywords))

    try:
        recommended_books = search_books_on_aladin(combined_terms, max_results=50)
        if len(recommended_books) < 50:
            additional = search_books_on_naver(combined_terms, max_results=50 - len(recommended_books))
            seen_isbns = {b['isbn'] for b in recommended_books}
            for book in additional:
                if book['isbn'] not in seen_isbns:
                    recommended_books.append(book)
                    seen_isbns.add(book['isbn'])
                if len(recommended_books) >= 50:
                    break
    except Exception as e:
        print("❌ 추천 API 전체 실패:", e)
        return Response({'error': '추천 도서 검색 실패', 'detail': str(e)}, status=500)

    return Response({
        'based_on': [book.title for book in books],
        'genres': list(all_genres),
        'keywords': list(all_keywords),
        'results': recommended_books,
    })

# 📌 [GET] /books/<str:isbn>/
@api_view(['GET'])
@permission_classes([AllowAny])
def get_book_detail(request, isbn):
    title = request.GET.get('title', '')
    author = request.GET.get('author', '')
    publisher = request.GET.get('publisher', '')
    cover_image = request.GET.get('cover_image', '')
    description = request.GET.get('description', '')

    book, _ = Book.objects.get_or_create(
        isbn=isbn,
        defaults={
            'title': title,
            'author': author,
            'publisher': publisher,
            'cover_image': cover_image,
            'description': description,
        }
    )

    book_data = BookSerializer(book).data
    reviews = book.reviews.order_by('-created_at')
    review_data = ReviewSerializer(reviews, many=True).data

    return Response({
        'book': book_data,
        'reviews': review_data
    })

# 📌 [GET, POST] /books/<str:isbn>/reviews/
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def list_create_reviews(request, isbn):
    book = get_object_or_404(Book, isbn=isbn)
    if request.method == 'GET':
        reviews = book.reviews.all().order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            rating = serializer.validated_data.get('rating')
            if not (1 <= rating <= 5):
                return Response({'error': '별점은 1~5 사이여야 합니다.'}, status=400)
            if Review.objects.filter(user=request.user, book=book).exists():
                return Response({'error': '이미 리뷰를 작성하셨습니다.'}, status=400)
            review = serializer.save(user=request.user, book=book)
            return Response(ReviewSerializer(review).data, status=201)
        return Response(serializer.errors, status=400)

# 📌 [PUT, DELETE] /reviews/<int:review_id>/
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data, context={'request': request})
        if serializer.is_valid():
            rating = serializer.validated_data.get('rating')
            if not (1 <= rating <= 5):
                return Response({'error': '별점은 1~5 사이여야 합니다.'}, status=400)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        review.delete()
        return Response({'message': '리뷰 삭제 완료'}, status=204)

# 📌 [POST] /questions/generate/
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_quiz_view(request):
    print("✅ quiz view 진짜 들어옴")
    print(f"인증 사용자: {request.user}")
    print(f"요청 데이터: {request.data}")

    title = request.data.get("title")
    if not title:
        return Response({"error": "책 제목이 필요합니다"}, status=400)

    gemini_api_key = settings.GEMINI_API_KEY

    prompt = f"""
    책 제목: {title}
    이 책 내용을 기반으로 객관식 퀴즈 3개를 만들어줘.
    각 문제는 보기 4개와 정답 1개를 포함해야 해.
    백틱이나 설명 없이 **JSON 문자열만** 반환해줘. 예시는 다음과 같아:

    [
      {{
        "question": "주인공은 누구입니까?",
        "options": ["A", "B", "C", "D"],
        "answer": "B"
      }}
    ]
    """

    quiz_raw = generate_quiz_with_gemini(prompt, gemini_api_key)
    print('[DEBUG] 응답 내용:', quiz_raw)

    try:
        if isinstance(quiz_raw, str):
            quiz_clean = re.sub(r"^```json|```$", "", quiz_raw.strip()).strip()
            parsed = json.loads(quiz_clean)
        elif isinstance(quiz_raw, list):
            parsed = quiz_raw
        else:
            raise ValueError("예상치 못한 Gemini 응답 형식")

        for q in parsed:
            ans = q.get("answer", "").strip().upper()
            if ans in ["A", "B", "C", "D"]:
                idx = ord(ans) - ord("A")
                if 0 <= idx < len(q["options"]):
                    q["answer"] = q["options"][idx]
                else:
                    q["answer"] = ""
            q["options"] = [opt.strip() for opt in q["options"]]

        return Response({"quiz": parsed})

    except Exception as e:
        print("[❌ JSON 파싱 실패]:", str(e))
        print("[🧾 원본]:", quiz_raw)
        return Response({
            "error": "퀴즈 파싱 실패",
            "debug": str(e)
        }, status=500)


# 📌 [POST] /questions/quiz-complete/
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def quiz_complete_view(request):
    user = request.user
    title = request.data.get('title')
    print(f"[DEBUG] 사용자: {user}, 제목: {title}")

    if not title:
        print("[ERROR] 제목이 없음")
        return Response({'error': '책 제목이 누락되었습니다.'}, status=400)

    try:
        record = ReadingRecord.objects.filter(user=user, book__title=title).order_by('-created_at').first()
        if not record:
            return Response({'error': '읽은 책 기록이 없습니다.'}, status=404)

        if record.quiz_completed:
            return Response({'error': '이미 퀴즈를 완료한 책입니다.'}, status=409)

        user.total_points += 50
        user.save()

        record.quiz_completed = True
        record.save()

        return Response({'message': '포인트 지급 완료!'}, status=200)

    except Exception as e:
        print(f"[FATAL ERROR] quiz_complete_view: {e}")
        return Response({'error': '서버 오류가 발생했습니다.'}, status=500)
