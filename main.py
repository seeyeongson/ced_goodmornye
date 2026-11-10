# main.py
import os
import json
from datetime import datetime
import requests
from google import genai

def get_weather():
    # TODO: 팀원 B (feature/weather) - Open-Meteo 날씨 수집 구현
    pass

def get_d_days():
    # TODO: 팀원 C (feature/ai-dday) - deadlines.json 읽기 & D-day 계산 구현
    pass

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