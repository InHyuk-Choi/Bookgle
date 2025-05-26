import json
import re
import requests
from django.conf import settings

# 퀴즈 생성기
def generate_quiz_with_gemini(summary, api_key):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    prompt = f"""
    아래는 책에 대한 위키백과 요약입니다. 이 내용을 바탕으로 객관식 퀴즈 3개를 만들어주세요.
    각 문제는 보기 4개(정답 1개 포함)를 포함해야 하며 JSON 형식으로 만들어주세요.
    
    책 요약:
    {summary}
    """

    body = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    response = requests.post(f"{url}?key={api_key}", headers=headers, json=body)

    if response.status_code == 200:
        candidates = response.json().get("candidates", [])
        if candidates:
            raw_text = candidates[0]["content"]["parts"][0]["text"]
            print("[DEBUG] 응답 내용:", raw_text)

            # ✅ 백틱, json 태그 제거
            cleaned_text = raw_text.strip().strip("```").replace("json", "").strip()

            try:
                quiz_data = json.loads(cleaned_text)
                return quiz_data
            except json.JSONDecodeError as e:
                print("[DEBUG] JSON 파싱 실패 내용:", cleaned_text)
                return {"error": "JSON 파싱 실패", "debug": cleaned_text}
    return {"error": "Gemini 요청 실패", "debug": None}

# 추천 알고리즘 생성기
def extract_keywords_with_gemini(title, description=''):
    api_key = settings.GEMINI_API_KEY
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}

    prompt = f"""
    아래는 책에 대한 정보입니다. 이 책을 바탕으로 다음 항목을 추출해주세요:

    1. 도서 장르 1개 (예: 문학, 심리학, 철학, 소설, SF)
    2. 핵심 키워드 3개 (이 책의 고유 주제, 감정, 개념 등)

    정확히 아래 JSON 형식으로 출력해주세요:

    ```json
    {{
      "genres": ["장르1"],
      "keywords": ["키워드1", "키워드2", "키워드3"]
    }}
    ```

    제목: {title}
    설명: {description or "설명이 없는 경우 제목만 참고해서 추론해주세요."}
    """

    body = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    try:
        response = requests.post(f"{url}?key={api_key}", headers=headers, json=body, timeout=7)
        response.raise_for_status()
        content = response.json().get("candidates", [])[0]["content"]["parts"][0]["text"]

        # JSON 블록만 추출
        match = re.search(r'```json\s*({.*?})\s*```', content, re.DOTALL)
        if match:
            return json.loads(match.group(1))  # genres, keywords 포함된 dict 반환
        else:
            print("⚠️ Gemini 응답에서 JSON 블록을 찾지 못함")
            return {"genres": [], "keywords": []}

    except Exception as e:
        print("❌ Gemini 장르/키워드 추출 실패:", e)
        return {"genres": [], "keywords": []}