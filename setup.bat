@echo off
echo ========================================
echo ☀️ ced_goodmornye 자동 세팅을 시작합니다...
echo ========================================

:: 1. 가상환경 생성
if not exist .venv (
    echo [1/3] 파이썬 가상환경(.venv)을 생성합니다...
    python -m venv .venv
) else (
    echo [1/3] 이미 가상환경이 존재합니다.
)

:: 2. 가상환경 활성화 및 패키지 설치
echo [2/3] 필수 패키지를 설치합니다...
call .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

:: 3. .env 파일 체크
if not exist .env (
    echo [경고] .env 파일이 없습니다! .env.example을 복사해 .env를 만들어주세요.
)

echo ========================================
echo 🎉 세팅이 완료되었습니다!
echo 실행하려면: .venv\Scripts\python main.py
echo ========================================
pause