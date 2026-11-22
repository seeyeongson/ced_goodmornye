# 🌅 모닝 브리핑 봇 (Morning Briefing Bot)

오늘의 날씨 정보와 마감 일정(D-Day)을 취합해 **Google Cloud Vertex AI(Gemini)**로 아침 브리핑을 생성하고, **Discord 웹훅**으로 전송하는 Python 자동화 스크립트입니다.

---
## ⚡ 가장 쉬운 실행 방법 (Windows · `setup.bat`)

명령어를 직접 치기 어렵다면 프로젝트 폴더에서 **`setup.bat`**을 더블클릭해 실행하세요.

1. **첫 번째 실행**: 가상환경(`.venv`) 생성과 패키지 설치를 자동으로 진행하고, `.env` 파일이 없으면 만든 뒤 **메모장**을 열어 줍니다.
2. **값 입력 및 저장**: 열린 메모장(`.env`)에 아래 항목을 채우고 저장한 뒤 닫습니다.
   ```env
   GOOGLE_APPLICATION_CREDENTIALS=서비스계정-키파일.json
   DISCORD_WEBHOOK_URL=[https://discord.com/api/webhooks/채널ID/웹훅토큰](https://discord.com/api/webhooks/채널ID/웹훅토큰)
---
## ✨ 주요 기능

* **날씨 정보 수집 (`weather.py`)**: 현재 위치/도시 기준 날씨 및 기온 정보를 조회합니다.
* **마감 일정 D-Day 계산 (`deadlines.json`)**: 등록된 일정의 남은 일수(`D-N`, `D-Day`, 마감 경과 등)를 계산하고, 기준을 초과한 오래된 일정은 정리합니다.
* **AI 브리핑 생성 (`main.py`)**: 날씨와 마감 일정을 바탕으로 오늘의 날씨 요약, 가장 임박한 일정, 우선순위 제안, 응원 문구가 담긴 브리핑을 생성합니다.
* **Discord 웹훅 전송 (`main.py`)**: 생성된 브리핑 메시지를 지정된 Discord 채널로 발송합니다.

---

## 📁 프로젝트 구조

```text
ced_goodmornye/
├── main.py              # 메인 실행 파이프라인 (날씨·일정 수집, Gemini 생성, Discord 전송)
├── weather.py           # 날씨 조회 모듈
├── deadlines.json       # 마감 일정 데이터 파일
├── requirements.txt     # 필수 Python 패키지 목록
├── .env.example         # 환경 변수 설정 예시 파일
├── .gitignore           # Git 제외 파일 설정 (.env, 서비스 계정 JSON 등)
└── README.md            # 프로젝트 안내 문서

## ⚙️ 사전 준비물
1. Python 3.10 이상

2. Google Cloud 프로젝트 및 Vertex AI 설정

    Vertex AI API (aiplatform.googleapis.com)가 활성화된 프로젝트

    Vertex AI 호출 권한이 부여된 서비스 계정(Service Account) 및 JSON 키 파일

    현재 프로젝트 및 지정한 리전(location)에서 호출 가능한 Gemini 모델 ID 확인

3. Discord 웹훅 URL

    브리핑을 수신할 Discord 채널의 웹훅 URL (https://discord.com/api/webhooks/...)

## 🚀 설치 및 실행 방법
1. 저장소 클론 및 이동

    git clone [https://github.com/seeyeongson/ced_goodmornye.git](https://github.com/seeyeongson/ced_goodmornye.git)
    
    cd ced_goodmornye


2. 가상환경 생성 및 패키지 설치

    # 가상환경 생성
    python -m venv .venv

    # 가상환경 활성화 (Windows PowerShell)
    .\.venv\Scripts\Activate.ps1

    # 가상환경 활성화 (macOS / Linux)
    # source .venv/bin/activate

    # 의존성 설치
    pip install -r requirements.txt


3. 환경 변수(.env) 설정
    (1) .env.example 파일을 복사해 .env 파일을 생성합니다.

        # Windows PowerShell 사용 시
        Copy-Item .env.example .env

        # macOS / Linux 사용 시
        cp .env.example .env

    (2).env 파일에 인증 파일 경로와 Discord 웹훅 URL을 입력합니다.

    코드 스니펫
    GOOGLE_APPLICATION_CREDENTIALS=경로/서비스계정-키파일.json
    DISCORD_WEBHOOK_URL=[https://discord.com/api/webhooks/채널ID/웹훅토큰](https://discord.com/api/webhooks/채널ID/웹훅토큰)
⚠️ 
    보안 주의: 서비스 계정 .json 키 파일과 .env 파일은 민감한 인증 정보를 포함하므로 절대 Git에 커밋하거나 푸시하지 마세요. .gitignore에 포함되어 있는지 항상 확인하세요.


4. 일정 데이터(deadlines.json) 작성
deadlines.json에 관리할 일정을 JSON 배열 형태로 입력합니다.

[
  {
    "title": "팀 프로젝트 발표 자료 제출",
    "date": "2026-11-28"
  },
  {
    "title": "기말고사 대비 복습",
    "date": "2026-12-05"
  }
]
날짜 형식은 YYYY-MM-DD를 사용합니다.


5. 봇 실행

python main.py
🛠️ 자주 발생하는 오류 및 해결 방법
[.env 파일 없음] 안내 후 종료되는 경우

프로젝트 루트 폴더에 .env 파일이 존재하는지 확인하세요.

401 UNAUTHENTICATED / 403 PERMISSION_DENIED

GOOGLE_APPLICATION_CREDENTIALS 경로가 정확한지, 해당 서비스 계정에 Vertex AI 사용 권한이 있는지 확인하세요.

403 API_KEY_SERVICE_BLOCKED

Vertex AI 서비스 계정 인증 사용 시 genai.Client에 문자열 api_key가 전달되지 않았는지, 환경 변수(GEMINI_API_KEY, GOOGLE_API_KEY)가 함께 설정되어 있지 않은지 확인하세요.

404 NOT_FOUND

코드에 지정된 모델 ID와 리전(location)이 현재 Google Cloud 프로젝트에서 지원되는 조합인지 Model Garden 및 리전 가용성에서 확인하세요.

Discord 전송 실패

.env의 DISCORD_WEBHOOK_URL 값이 올바른지, 인터넷 연결 및 Discord 웹훅 상태가 정상인지 확인하세요.


---

저장소에 이미 있는 `requirements.txt` 패키지 이름이나 `.env.example`의 변수명, 실제 사용 중인 모