import os
import json
from datetime import datetime
import requests
from google import genai

def get_weather():
    # 1. Open-Meteo 날씨 API 호출 (서울 기준, 키 불필요, 완전 무료)
    url = "https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&current=temperature_2m,weather_code"
    try:
        response = requests.get(url)
        data = response.json()
        temp = data["current"]["temperature_2m"]
        return f"현재 서울 기온은 {temp}°C입니다."
    except Exception:
        return "날씨 정보를 불러오지 못했습니다."

def get_d_days():
    # 2. deadlines.json 파일을 읽어 오늘 날짜 기준 D-day 계산
    try:
        with open("deadlines.json", "r", encoding="utf-8") as f:
            deadlines = json.load(f)
        
        today = datetime.now().date()
        result = []
        for item in deadlines:
            d_date = datetime.strptime(item["date"], "%Y-%m-%d").date()
            delta = (d_date - today).days
            if delta >= 0:
                result.append(f"- {item['title']}: D-{delta}")
            else:
                result.append(f"- {item['title']}: 마감 지남 (D+{abs(delta)})")
        return "\n".join(result) if result else "등록된 일정이 없습니다."
    except Exception:
        return "마감일 정보를 불러오지 못했습니다."

def generate_morning_briefing(weather_text, d_day_text):
    # 3. Google Gemini API로 아침 인사 요약 생성
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # 키가 없으면 기본 템플릿으로 출력 (안전장치)
        return f"[기본 아침 브리핑]\n{weather_text}\n\n[일정 안내]\n{d_day_text}"
    
    try:
        client = genai.Client(api_key=api_key)
        prompt = f"""
        아래 정보를 바탕으로 대학생을 위한 친근하고 짧은 아침 인사와 브리핑을 3줄 이내로 작성해줘. 이모지를 곁들여줘.
        - 날씨: {weather_text}
        - 일정: {d_day_text}
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        # AI 호출 중 오류가 나면 기본 문장으로 안전하게 대체 (Fallback)
        return f"[아침 브리핑 (기본 모드)]\n{weather_text}\n\n{d_day_text}"

def send_discord(message):
    # 4. 디스코드 웹훅으로 메시지 전송
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("Discord Webhook URL이 설정되지 않았습니다.")
        return
    
    payload = {"content": message}
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204 or response.status_code == 200:
        print("디스코드 전송 성공!")
    else:
        print(f"디스코드 전송 실패 (상태 코드: {response.status_code})")

if __name__ == "__main__":
    print("모닝 브리핑 봇 실행 중...")
    weather = get_weather()
    d_days = get_d_days()
    briefing = generate_morning_briefing(weather, d_days)
    send_discord(briefing)
    print("브리핑 작업 완료!")