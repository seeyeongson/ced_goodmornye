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
├── .github/
│   └── workflows/
│       └── morning.yml  # GitHub Actions 자동 실행 설정 (매일 오전 7시)
├── .vscode/
│   └── settings.json    # VS Code에서 .env 자동 로드 설정
├── setup.bat            # Windows용 자동 세팅 및 실행 스크립트
├── main.py              # 날씨·일정 수집, Gemini 브리핑 생성, Discord 전송
├── weather.py           # 날씨 조회 모듈 (Open-Meteo API)
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

---

## 🔄 자동 실행 (GitHub Actions)

`.github/workflows/morning.yml`에 설정되어 있어, 매일 **한국 시간 오전 7시**(UTC 22:00)에 자동으로 브리핑이 전송됩니다. GitHub의 **Actions** 탭에서 `Run workflow` 버튼으로 수동 실행도 할 수 있습니다.

자동 실행을 쓰려면 저장소의 **Settings → Secrets and variables → Actions**에 아래 값을 등록하세요.

| Secret 이름 | 설명 |
| --- | --- |
| `DISCORD_WEBHOOK_URL` | 브리핑을 받을 Discord 웹훅 URL |
| `GEMINI_API_KEY` | 워크플로에서 전달하는 키 (아래 ⚠️ 참고) |

> ⚠️ **참고**: 현재 `main.py`는 Vertex AI 서비스 계정 인증(`GOOGLE_APPLICATION_CREDENTIALS`)을 사용하지만, 워크플로는 `GEMINI_API_KEY`만 전달합니다. 자동 실행에서 Gemini 인증이 실패하면 서비스 계정 키를 Secret으로 등록하고 워크플로에서 파일로 복원하는 방식으로 맞춰야 합니다.

---

## 🧩 동작 흐름

`main.py`는 아래 순서로 실행됩니다.

1. **날씨 조회** (`weather.py`): Open-Meteo API에서 현재 기온과 날씨 코드를 가져옵니다. API 키는 필요 없습니다.
2. **D-Day 계산** (`main.py`의 `get_d_days`): `deadlines.json`을 읽어 남은 일수를 계산합니다.
3. **브리핑 생성**: 날씨와 일정을 Gemini에 전달해 150~200자 내외의 한국어 브리핑을 만듭니다.
   * 날씨 요약, 가장 임박한 일정, 오늘의 우선순위, 응원 문구를 포함합니다.
   * Gemini 호출이 3회 모두 실패하면 AI 없이 날씨와 일정 원문을 그대로 보내는 대체 메시지를 사용합니다.
4. **Discord 전송**: 완성된 메시지를 웹훅으로 보냅니다. 전송에 실패하면 종료 코드 `1`로 끝납니다.

---

## ⚙️ 설정 옵션

### 날씨 지역 변경

기본 지역은 서울입니다. `.env`에 아래 값을 추가하면 다른 지역의 날씨를 받을 수 있습니다.

```env
WEATHER_CITY=Busan
WEATHER_LAT=35.1796
WEATHER_LON=129.0756
```

* 세 값 중 하나라도 비어 있으면 서울 기본값이 사용됩니다.
* 위도/경도가 숫자가 아니면 경고를 출력하고 서울 기본값을 씁니다.
* 날씨 설명은 영어(예: `Clear sky`)로 받아오고, 최종 브리핑은 Gemini가 한국어로 작성합니다.

### Gemini 모델 및 프로젝트 변경

`main.py`의 `generate_morning_briefing` 함수에서 아래 값을 본인 환경에 맞게 수정해야 합니다.

```python
client = genai.Client(
    vertexai=True,
    project="604391155797",   # ← 본인의 Google Cloud 프로젝트 ID 또는 번호로 변경
    location="global",        # ← 사용 가능한 리전으로 변경
    ...
)
model="publishers/google/models/gemini-3.8-flash"  # ← 사용 가능한 모델 ID로 변경
```

---

## 📅 마감 일정(`deadlines.json`) 작성 규칙

```json
[
  {
    "title": "자료구조 중간고사",
    "date": "2026-11-25"
  }
]
```

* `title`: 브리핑에 표시될 일정 이름
* `date`: `YYYY-MM-DD` 형식. 다른 형식이면 D-Day 계산 오류가 납니다.
* 출력 예시: `D-3`, `D-Day`, `마감 지남 (2일 전)`
* **자동 정리**: 봇을 실행할 때마다 마감일이 **5일 넘게 지난 일정은 파일에서 삭제**됩니다. 마감 후 5일까지는 "마감 지남"으로 표시됩니다.
* 등록된 일정이 없으면 "현재 등록된 일정이 없습니다."라고 표시됩니다.

---

## 🪟 `setup.bat` 동작 상세

1. `python` 명령이 없으면 설치 안내 후 종료합니다.
2. `.venv`가 없으면 생성하고, `requirements.txt`를 설치합니다.
3. `.env`가 없으면 `.env.example`을 복사한 뒤 메모장을 열고 **한 번 종료**합니다. 값을 입력한 후 다시 실행하세요.
4. 실행 전에 `GEMINI_API_KEY`, `GOOGLE_API_KEY` 환경 변수를 비웁니다. 서비스 계정 인증과 API 키가 섞이는 것을 막기 위해서입니다. (이 설정은 해당 배치 창 안에서만 적용됩니다.)
5. `main.py`를 실행하고 결과 코드를 표시한 뒤 창이 닫히기 전에 대기합니다.

---

## 🛠 개발 환경 참고

* `.vscode/settings.json`에 `"python.terminal.useEnvFile": true`가 설정되어 있어, VS Code 터미널을 열 때 `.env` 값이 자동으로 로드됩니다.
* `.env` 파일이 없으면 `main.py`는 안내 메시지를 출력하고 종료합니다. (GitHub Actions 환경에서는 이 검사를 건너뜁니다.)

---

## 📦 의존성

| 패키지 | 용도 |
| --- | --- |
| `requests` | 날씨 API 및 Discord 웹훅 요청 |
| `google-genai` | Vertex AI(Gemini) 호출 |
| `python-dotenv` | `.env` 파일 로드 |

---

## 📚 참고 자료

* 날씨 데이터: [Open-Meteo Forecast API](https://open-meteo.com/)
* 브리핑 생성: [Google Gen AI SDK (Python)](https://github.com/googleapis/python-genai)
* 메시지 전송: [Discord 웹훅 문서](https://discord.com/developers/docs/resources/webhook)

---

## ⚠️ 주의 및 문제 해결

* **인증 키 파일(`.json`)과 `.env`는 Git에 올리지 않기**: 개인/서비스 계정 정보가 들어 있으므로 `.gitignore`에 제외되어 있는지 항상 확인하세요.
* **`401` / `403` 권한·인증 오류**: `GOOGLE_APPLICATION_CREDENTIALS` 경로와 서비스 계정 권한을 확인하고, Vertex AI 서비스 계정 인증 시 `GEMINI_API_KEY` / `GOOGLE_API_KEY` 환경 변수가 섞이지 않았는지 점검하세요.
* **`404` 모델·리전 오류**: 현재 프로젝트에서 호출 가능한 Gemini 모델 ID와 리전(`location`)이 코드와 맞는지 확인하세요.
* **Discord 전송 실패**: `.env`의 `DISCORD_WEBHOOK_URL`이 비어 있거나 오타가 없는지 확인하세요.
