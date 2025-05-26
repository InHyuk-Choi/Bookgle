import requests
from django.conf import settings

def search_books_on_naver(keywords, max_results=50):
    headers = {
        'X-Naver-Client-Id': settings.NAVER_CLIENT_ID,
        'X-Naver-Client-Secret': settings.NAVER_CLIENT_SECRET,
    }

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
            'query': keyword,
            'display': 10,
            'start': 1,
            'sort': 'sim',
        }

        try:
            res = requests.get("https://openapi.naver.com/v1/search/book.json", headers=headers, params=params, timeout=5)
            res.raise_for_status()

            for item in res.json().get('items', []):
                isbn = item.get('isbn', '').split()[-1]
                title = item.get('title', '').strip()

                if isbn not in seen_isbns and title not in seen_titles:
                    seen_isbns.add(isbn)
                    seen_titles.add(title)
                    books.append({
                        'isbn': isbn,
                        'title': title,
                        'author': item.get('author'),
                        'publisher': item.get('publisher'),
                        'cover_image': item.get('image'),
                        'description': item.get('description'),
                    })

                if len(books) >= max_results:
                    break

        except Exception as e:
            print(f"❌ Naver API 실패 ({keyword}): {e}")
            continue

    return books