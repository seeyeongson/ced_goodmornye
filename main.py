# main.py
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import requests
import time
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

        if not results:
            return "현재 등록된 일정이 없습니다."

        return "\n".join(results)

    except Exception as e:
        return f"D-Day 계산 오류: {e}"

def generate_morning_briefing(weather_text, d_day_text):
    try:
        client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        prompt = f"""
당신은 대학생을 위한 AI 모닝 브리핑 도우미입니다.

날씨:
{weather_text}

마감 일정:
{d_day_text}

다음을 포함하여 150~200자 내외의 한국어 브리핑을 작성하세요.

- 오늘의 날씨 요약
- 가장 임박한 일정
- 오늘의 우선순위 제안
- 긍정적인 응원 문구
"""

        for _ in range(3):
            try:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                return response.text

            except Exception as e:
                print(f"Gemini 재시도 중: {e}")
                time.sleep(3)

        return (
            "AI 서버가 현재 혼잡합니다.\n\n"
            f"날씨: {weather_text}\n\n"
            f"일정:\n{d_day_text}"
        )

    except Exception as e:
        return f"브리핑 생성 실패: {e}"

def send_discord(message):
    # TODO: 팀원 D (feature/discord) - Discord Webhook 전송 구현
    pass

if __name__ == "__main__":
    print("모닝 브리핑 봇 실행 시작...")
    weather = get_weather()
    d_days = get_d_days()
    briefing = generate_morning_briefing(weather, d_days)
    print(briefing) #테스트 용
    #send_discord(briefing)
    print("브리핑 완료!")
