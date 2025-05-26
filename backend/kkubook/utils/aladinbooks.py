import requests
from django.conf import settings

def search_books_on_aladin(keywords, max_results=50):
    base_url = "https://www.aladin.co.kr/ttb/api/ItemSearch.aspx"
    seen_isbns = set()
    seen_titles = set()
    books = []
    round_robin_index = 0

    if not keywords:
        return []

    while len(books) < max_results:
        if round_robin_index >= len(keywords):
            round_robin_index = 0

        keyword = keywords[round_robin_index]
        round_robin_index += 1

        params = {
            'ttbkey': settings.ALADIN_API_KEY,
            'Query': keyword,
            'QueryType': 'Keyword',
            'MaxResults': 10,
            'start': 1,
            'SearchTarget': 'Book',
            'output': 'js',
            'Version': '20131101',
        }

        try:
            res = requests.get(base_url, params=params, timeout=5)
            res.raise_for_status()
            items = res.json().get('item', [])

            for item in items:
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
                        'description': item.get('description'),  # ✅ 줄거리 설명
                    })

                if len(books) >= max_results:
                    break

        except Exception as e:
            print(f"❌ Aladin API 실패 ({keyword}): {e}")
            continue

    return books
