import json
import requests

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
