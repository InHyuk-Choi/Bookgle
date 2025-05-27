# 🐛 꾸북(Kkubook) - 독서 게이미피케이션 서비스

> “읽을수록 자라는 책벌레, 퀴즈로 확인하는 내 지식!”  
> 독서 활동을 기록하고 AI 퀴즈, 성장 시스템, 피드 공유를 통해 **책 읽는 습관을 게임처럼** 만들어가는 웹 서비스입니다.

---

## 👥 팀원 및 역할 분담

| 이름   | 담당 역할     | 상세 업무 |
|--------|----------------|-----------|
| 차성현 | Backend 개발   | Django API 서버 구축, 사용자 인증(Token), AI기반 도서 추천 알고리즘,  DB 모델링 |
| 최인혁 | Frontend 개발  | Vue 기반 SPA 개발, 캐릭터/피드/상점 등 UI 구현, AI 퀴즈 생성 로직, 사용자 경험 개선 |

---

## 🗓️ 개발 기간

- 2025.05.17 ~ 2025.05.27 (총 11일)

---

## 🎯 서비스 개요

**꾸북(Kkubook)**은 AI 기반 퀴즈 생성, 책벌레 성장, 사용자 리뷰 및 피드 기능이 결합된 **독서 게이미피케이션 플랫폼**입니다.  
단순한 책 검색을 넘어서, **독서 이후의 상호작용(퀴즈/리뷰/성장)**까지 경험할 수 있도록 설계되었습니다.

---

## 🔧 기술 스택

| 영역        | 사용 기술 |
|-------------|-----------|
| Frontend    | Vue 3, Vite, Tailwind CSS, Pinia, Vue Router, SweetAlert2 |
| Backend     | Django 4.2, Django REST Framework, dj-rest-auth, JWT(SimpleJWT), Pillow |
| AI 활용     | Google Gemini API |
| 도서 정보 API | Aladin, Naver Book APIs |
| 인증 방식   | JWT 기반 인증 (Access: LocalStorage, Refresh: HttpOnly Cookie) |
| 배포        | 미배포 (추후 모바일 서비스로 배포 예정) |

---

## 🧠 주요 기능 상세 및 핵심 로직

### 1. 📖 도서 검색 및 등록
- **Aladin / Naver Book API** 기반 도서 검색
- 검색된 도서를 클릭하여 `Book` 모델로 등록 (ISBN 기반 중복 제거)
- 등록된 도서는 퀴즈 대상 도서로 사용됨



### 2. 🐛 책벌레 키우기 시스템
- 상점에서 **일반/고급 먹이** 구매 (포인트 차등 소모)
- 먹이를 사용해 책벌레에게 경험치 제공
- 경험치 기반 **레벨업** 시스템 (`LEVEL_EXPERIENCE_TABLE`)
- 레벨 계산은 `models.py`의 `get_experience_to_next_level()` 함수 기반
- 시각적 표현은 `PetStatus.vue`에서 애벌레 상태 출력



### 3. 🔐 사용자 인증 (JWT 기반)
- Access Token → LocalStorage  
- Refresh Token → HttpOnly Cookie  
- API 요청 중 Access Token 만료 시 자동으로 Refresh  
- `dj-rest-auth`, `simplejwt` 기반 토큰 발급 및 인증 흐름 구현



### 4. 🧠 AI 기반 퀴즈 생성기
- 책 완독 시 퀴즈 생성 버튼 활성화
- **Google Gemini API** 기반 줄거리 요약 확보
- **Google Gemini API**에 요약 전달 → 객관식 퀴즈 3~5개 생성
- 퀴즈는 DB에 저장되며, 재시도 시 캐시 사용
- 해당 로직은 `generate_questions_for_book()` 함수에서 일괄 처리


### 5. 📝 사용자 리뷰 및 퀴즈
- 퀴즈 풀이 후 결과 확인 및 **리뷰 작성**
- 리뷰는 `Review` 모델에 저장
- 다른 유저의 리뷰도 책 상세페이지에서 확인 가능



### 6. 💬 피드/댓글 기능
- 사용자가 작성한 독서 경험 공유 가능 (피드 카드 기반)
- 댓글 작성 및 좋아요 기능 지원
- `Feed`, `Comment` 모델 기반 REST API 구성



### 7. 👤 유저 프로필 & 랭킹
- 사용자의 경험치, 보유 포인트, 서재 정보 확인 가능
- 전체 유저를 경험치 기준으로 정렬해 랭킹 표시  
  → `BookwormRankingSerializer` 사용

### 8. 📚 AI 기반 도서 추천 알고리즘

- 사용자가 등록한 도서 리스트(내 서재)를 기반으로 **선호 주제 및 저자**를 추정
- 해당 정보를 바탕으로 **Aladin Open API**를 활용하여 유사한 도서를 추천


#### 출력 방식
- 최대 50권까지 추천 도서 구성
- `RecommendedBooksView.vue`에서 **카드형 UI**로 시각화 출력

> 추천 뷰에서는 사용자가 관심 있는 도서를 **즉시 등록하거나 서재에 추가할 수 있으며**,  
> 추천 알고리즘은 사용자의 독서 패턴이 누적될수록 점점 **정교하게 발전**합니다.

---

## 🖼️ 주요 UI 예시

- 홈화면: 책벌레 캐릭터 + 서재 + 상점
- 책 상세: 줄거리 + 퀴즈 생성 + 리뷰 확인
- 퀴즈 페이지: 질문 + 선택지 + 정답 결과
- 피드 페이지: 카드형 UI + 댓글
- 상점: 먹이 구매
- 랭킹: 유저 레벨/포인트 정렬

> 💡 상세 구조는 아래 컴포넌트 구조도 참고

---

## 📊 ERD 및 컴포넌트 구조

- **ERD 다이어그램**  
  
![erd](https://github.com/user-attachments/assets/5dbb6618-08f1-4eed-a7c8-0bb591b1938f)

- **Vue 컴포넌트 구조도**  
![vue_components](https://github.com/user-attachments/assets/cb0f677c-633d-40c5-b21c-809ea56c86ff)

---

## 🔍 API 명세

[API 명세서.pdf](https://github.com/user-attachments/files/20453544/API.pdf)

---

## 💬 프로젝트 회고

### 👨‍💻 차성현 (Backend) *수정 예정*

#### 👍 배운 점
- Refresh Cookie 방식을 적용한 JWT 인증 흐름을 통해 보안과 사용자 편의성 모두 고려한 설계 경험
- AI API 연동 및 예외 처리 구조를 설계하며 실시간 응답 처리 능력 향상
- 데이터 모델 설계 및 책벌레 성장 로직 구성에서 사용자의 행동 데이터를 구조화하는 방법을 익힘

#### 😓 어려웠던 점
- Gemini API의 응답 포맷이 예측 불가능해 파싱 예외처리 코드가 복잡해졌음
- 피드/댓글/유저 모델 간 순환 참조 방지 및 직렬화 구조 설계에 시간 소요

---

### 👨‍🎨 최인혁 (Frontend) *수정 예정*

#### 👍 배운 점
- Pinia와 Vue Router 간의 데이터 흐름을 구조적으로 설계하며 상태관리 전반에 대한 이해도 향상
- Tailwind 기반 반응형 UI 구현과 사용자 피드백을 반영한 인터랙션 설계 경험
- 퀴즈 생성/결과/리뷰 흐름을 UX 기반으로 설계하여 사용자 경험 강화

#### 😓 어려웠던 점
- 페이지 간 상태 전이 시 캐시/리렌더링 이슈 → 구조 개선 필요
- 퀴즈 생성~리뷰 작성의 전반 흐름을 연결하며 사용자 몰입도를 유지하는 데 UX 고민 필요

---

## 🔮 향후 개선 방향

- ✅ 모바일 기반(앱스토어) 배포 및 CI/CD 연동
- ✅ 퀴즈 성과 기반 포인트/뱃지 시스템
- ✅ 반응형 모바일 UI 최적화
- ✅ 유사 독서 성향 사용자 추천 알고리즘
- ✅ 친구/팔로우 기반 피드 필터링

---

이 프로젝트는 실제 서비스를 고려한 기능 설계, UI 구현, AI 연동까지 폭넓게 다룬 팀 프로젝트입니다.  
프로젝트 진행과정은 Jira에서 확인해주세요.
[https://cjn112070.atlassian.net/jira/software/projects/SCRUM/boards/1/timeline](https://cjn112070.atlassian.net/jira/software/projects/SCRUM/boards/1/timeline?atlOrigin=eyJpIjoiMmJlOTc2OTEyMjc0NGNhMmJhMjU3ZDZiYWQyMjhhNWQiLCJwIjoiaiJ9)