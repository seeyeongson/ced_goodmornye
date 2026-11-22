# 🌅 모닝 브리핑 봇 (Morning Briefing Bot)

오늘의 날씨와 마감 일정(D-Day)을 모아 **Google Cloud Vertex AI(Gemini)**로 아침 브리핑을 만들고, **Discord 웹훅**으로 보내주는 Python 봇입니다.

---

## ⚡ 가장 쉬운 실행 방법 (Windows · `setup.bat`)

명령어를 직접 치기 어렵다면 프로젝트 폴더에서 **`setup.bat`**을 더블클릭해 실행하세요.

1. **첫 번째 실행**: 가상환경(`.venv`) 생성과 패키지 설치를 자동으로 진행하고, `.env` 파일이 없으면 만든 뒤 **메모장**을 열어 줍니다.
2. **값 입력 및 저장**: 열린 메모장(`.env`)에 아래 항목을 채우고 저장한 뒤 닫습니다.

   ```env
   GOOGLE_APPLICATION_CREDENTIALS=서비스계정-키파일.json
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/채널ID/웹훅토큰
   ```

3. 두 번째 실행부터: `setup.bat`을 다시 실행하면 준비된 환경으로 `main.py`가 바로 실행됩니다.

---

## 📁 주요 파일 안내

```text
ced_goodmornye/
├── setup.bat            # Windows용 자동 세팅 및 실행 스크립트
├── main.py              # 날씨·일정 수집, Gemini 브리핑 생성, Discord 전송
├── weather.py           # 날씨 조회 모듈
├── deadlines.json       # 마감 일정 목록 (YYYY-MM-DD 형식)
├── requirements.txt     # 필요한 Python 패키지 목록
├── .env.example         # 환경 변수 입력 양식
├── .gitignore           # 민감 파일(.env, 서비스 계정 JSON 등) Git 제외 목록
└── README.md            # 사용 설명서
```

---

## 🔑 시작하기 전에 준비할 것

1. **Python 3.10 이상** (설치 시 `Add Python to PATH` 체크 권장)
2. **Google Cloud 서비스 계정 JSON 키 파일**
   * Vertex AI API(`aiplatform.googleapis.com`)가 켜진 프로젝트의 서비스 계정 키
   * 프로젝트/리전에서 사용 가능한 Gemini 모델 ID 확인 필요
3. **Discord 웹훅 URL**
   * 메시지를 받을 Discord 채널 설정에서 생성한 웹훅 주소

---

## 💻 직접 명령어로 설치·실행하고 싶다면 (macOS / Linux / 수동 실행)

### 1. 프로젝트 받기

```bash
git clone https://github.com/seeyeongson/ced_goodmornye.git
cd ced_goodmornye
```

### 2. 가상환경 만들기 및 패키지 설치

```powershell
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. `.env` 파일 설정

`.env.example`을 복사해 `.env` 파일을 만든 뒤 값을 입력합니다.

```powershell
# Windows (PowerShell)
Copy-Item .env.example .env
```

```bash
# macOS / Linux
cp .env.example .env
```

### 4. 일정 파일(`deadlines.json`) 확인

```json
[
  {
    "title": "과제 제출",
    "date": "2026-11-25"
  }
]
```

### 5. 실행

```bash
python main.py
```

---

## ⚠️ 주의 및 문제 해결

* **인증 키 파일(`.json`)과 `.env`는 Git에 올리지 않기**: 개인/서비스 계정 정보가 들어 있으므로 `.gitignore`에 제외되어 있는지 항상 확인하세요.
* **`401` / `403` 권한·인증 오류**: `GOOGLE_APPLICATION_CREDENTIALS` 경로와 서비스 계정 권한을 확인하고, Vertex AI 서비스 계정 인증 시 `GEMINI_API_KEY` / `GOOGLE_API_KEY` 환경 변수가 섞이지 않았는지 점검하세요.
* **`404` 모델·리전 오류**: 현재 프로젝트에서 호출 가능한 Gemini 모델 ID와 리전(`location`)이 코드와 맞는지 확인하세요.
* **Discord 전송 실패**: `.env`의 `DISCORD_WEBHOOK_URL`이 비어 있거나 오타가 없는지 확인하세요.
