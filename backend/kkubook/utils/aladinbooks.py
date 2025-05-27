import requests
import time
from django.conf import settings

def search_books_on_aladin(keywords, max_results=50, timeout=10):
    base_url = "https://www.aladin.co.kr/ttb/api/ItemSearch.aspx"
    seen_isbns = set()
    seen_titles = set()
    books = []

    keywords = list(dict.fromkeys(keywords))[:7]  # 대표 키워드 7개 제한

    if not keywords:
        return []

    for keyword in keywords:
        print(f"📘 Aladin 검색: {keyword}")
        for attempt in range(3):
            try:
                time.sleep(0.3 * attempt)  # ✅ 요청 간 딜레이 및 점진적 backoff
                res = requests.get(base_url, params={
                    'ttbkey': settings.ALADIN_API_KEY,
                    'Query': keyword,
                    'QueryType': 'Keyword',
                    'MaxResults': 10,
                    'start': 1,
                    'SearchTarget': 'Book',
                    'output': 'js',
                    'Version': '20131101',
                }, timeout=timeout)
                res.raise_for_status()

                for item in res.json().get('item', []):
                    isbn = item.get('isbn13')
                    title = item.get('title', '').strip()

                    if isbn and isbn not in seen_isbns and title not in seen_titles:
                        seen_isbns.add(isbn)
                        seen_titles.add(title)
                        books.append({
                            'isbn': isbn,
                            'title': title,
                            'author': item.get('author'),
                            'publisher': item.get('publisher'),
                            'cover_image': item.get('cover'),
                            'description': item.get('description'),
                        })

                    if len(books) >= max_results:
                        return books
                break  # ✅ 성공 시 루프 탈출
            except Exception as e:
                print(f"❌ Aladin API 실패 ({keyword}) [시도 {attempt + 1}]: {e}")
                if attempt == 2:
                    raise  # 최종 실패 시 상위로 예외 전달
    return books
