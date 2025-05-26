import requests

def get_wikipedia_summary(book_title):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{book_title}"
    print("[DEBUG] Wikipedia 요청 URL:", url)  # 요청한 URL 로그

    try:
        response = requests.get(url, timeout=5)
        print("[DEBUG] Wikipedia 응답 코드:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            print("[DEBUG] Wikipedia 응답 데이터 요약:", data.get("extract", "")[:150], "...")
            return data.get("extract", "")  # 책 줄거리 요약

        else:
            print("[DEBUG] Wikipedia 응답 실패: ", response.status_code)

    except requests.RequestException as e:
        print("[ERROR] Wikipedia 요청 예외 발생:", e)

    return ""
