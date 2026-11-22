@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ==========================================
echo   모닝 브리핑 봇 설정 및 실행 도우미
echo ==========================================
echo.

REM 1. Python 설치 확인
where python >nul 2>nul
if errorlevel 1 (
    echo [오류] Python이 설치되어 있지 않습니다.
    echo Python 3.10 이상을 설치하고 "Add Python to PATH"를 체크한 뒤 다시 실행하세요.
    pause
    exit /b 1
)

REM 2. 가상환경(.venv) 생성
if not exist ".venv\Scripts\python.exe" (
    echo [1/4] 가상환경(.venv)을 생성하는 중...
    python -m venv .venv
    if errorlevel 1 (
        echo [오류] 가상환경 생성에 실패했습니다.
        pause
        exit /b 1
    )
) else (
    echo [1/4] 기존 가상환경(.venv)을 사용합니다.
)

REM 3. 의존성 패키지 설치
if exist "requirements.txt" (
    echo [2/4] 필수 패키지를 설치하는 중...
    ".venv\Scripts\python.exe" -m pip install --upgrade pip >nul
    ".venv\Scripts\pip.exe" install -r requirements.txt
    if errorlevel 1 (
        echo [오류] 패키지 설치 중 문제가 발생했습니다.
        pause
        exit /b 1
    )
) else (
    echo [경고] requirements.txt 파일이 없습니다. 패키지 설치를 건너뜁니다.
)

REM 4. .env 파일 확인 및 생성
echo [3/4] 환경 변수(.env) 파일을 확인하는 중...
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo [안내] .env 파일이 없어 .env.example을 복사해 .env를 생성했습니다.
    ) else (
        (
            echo GOOGLE_APPLICATION_CREDENTIALS=서비스계정-키파일.json
            echo DISCORD_WEBHOOK_URL=여기에_디스코드_웹훅_URL_입력
        ) > ".env"
        echo [안내] 기본 .env 파일을 생성했습니다.
    )
    echo.
    echo [중요] .env 파일에 인증 파일 경로와 DISCORD_WEBHOOK_URL을 입력한 뒤
    echo        setup.bat을 다시 실행해 주세요!
    notepad ".env"
    pause
    exit /b 0
)

REM Vertex AI 서비스 계정 인증 시 API 키 환경 변수 간섭 방지(현재 배치 세션 한정)
set "GEMINI_API_KEY="
set "GOOGLE_API_KEY="

REM 5. 메인 스크립트 실행
echo [4/4] 모닝 브리핑 봇(main.py)을 실행합니다...
echo.
".venv\Scripts\python.exe" main.py
set "EXIT_CODE=%ERRORLEVEL%"

echo.
if %EXIT_CODE% equ 0 (
    echo [완료] 실행이 정상적으로 끝났습니다.
) else (
    echo [실패] 실행 중 오류가 발생했습니다. (종료 코드: %EXIT_CODE%)
)
pause
exit /b %EXIT_CODE%