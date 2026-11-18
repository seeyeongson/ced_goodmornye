# main.py
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import requests
from google import genai
from weather import get_weather as fetch_weather

# .env 파일이 없으면 친절하게 에러를 띄우고 중단
if not os.path.exists(".env"):
    print("❌ [.env 파일 없음] .env.example 파일을 복사하여 .env 파일을 만들고 API 키를 입력해주세요!")
    exit(1)

load_dotenv()

def get_weather():
    # TODO: 팀원 B (feature/weather) - Open-Meteo 날씨 수집 구현

    # 날씨 데이터를 브리핑에 사용할 문장으로 변환
    result = fetch_weather()

    if result["status"] == "error":
        return "현재 날씨 정보를 가져올 수 없습니다."

    return (
        f"{result['city']} 현재 기온: {result['temperature']}°C, "
        f"날씨: {result['weather']}"
    )

def get_d_days():
    try:
        with open("deadlines.json", "r", encoding="utf-8") as f:
            deadlines = json.load(f)

        today = datetime.today().date()
        results = []
        updated_deadlines = []

        for item in deadlines:
            title = item["title"]
            deadline = datetime.strptime(
                item["date"], "%Y-%m-%d"
            ).date()

            diff = (deadline - today).days

            # 마감 후 5일 초과 시 제거
            if diff < -5:
                continue

            updated_deadlines.append(item)

            if diff > 0:
                results.append(f"{title}: D-{diff}")
            elif diff == 0:
                results.append(f"{title}: D-Day")
            else:
                results.append(
                    f"{title}: 마감 지남 ({abs(diff)}일 전)"
                )

        # 제거된 일정 반영
        with open("deadlines.json", "w", encoding="utf-8") as f:
            json.dump(
                updated_deadlines,
                f,
                ensure_ascii=False,
                indent=2
            )

        return "\n".join(results)

    except Exception as e:
        return f"D-Day 계산 오류: {e}"

def generate_morning_briefing(weather_text, d_day_text):
    # TODO: 팀원 C (feature/ai-dday) - Gemini API 연동 & 요약 프롬프트 작성
    pass

def send_discord(message):
    # TODO: 팀원 D (feature/discord) - Discord Webhook 전송 구현
    pass

if __name__ == "__main__":
    print("모닝 브리핑 봇 실행 시작...")
    weather = get_weather()
    d_days = get_d_days()
    briefing = generate_morning_briefing(weather, d_days)
    send_discord(briefing)
    print("브리핑 완료!")
