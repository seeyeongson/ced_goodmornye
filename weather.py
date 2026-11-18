
# 팀 프로젝트 B: 날씨 데이터 수집
# Open-Meteo API를 이용하여 서울의 현재 날씨 정보를 가져옵니다.

import requests


# WMO 날씨 코드를 영어 설명으로 변환
weather_descriptions = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}


# 현재 날씨 정보를 가져오는 함수
def get_weather():

    # API 주소 및 요청할 날씨 데이터 설정
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": 37.5665,
        "longitude": 126.9780,
        "current": "temperature_2m,weather_code",
        "timezone": "Asia/Seoul"
    }

    try:
        # 타임아웃이 발생하면 한 번만 다시 요청
        try:
            response = requests.get(url, params=params, timeout=10)
        except requests.exceptions.Timeout:
            response = requests.get(url, params=params, timeout=10)

        response.raise_for_status()

        # JSON 응답을 Python 데이터로 변환
        data = response.json()

        # 현재 날씨 정보 추출
        current = data["current"]
        temperature = current["temperature_2m"]
        weather_code = current["weather_code"]

        # 필수 데이터가 없는 경우 오류 처리
        if temperature is None or weather_code is None:
            raise ValueError("Missing weather data")

        # 날씨 코드를 영어 설명으로 변환
        weather = weather_descriptions.get(
            weather_code, "Unknown weather"
        )

        # 정상적으로 가져온 날씨 정보 반환
        return {
            "city": "Seoul",
            "temperature": temperature,
            "weather": weather,
            "status": "success"
        }

    except (requests.exceptions.RequestException,
            ValueError, KeyError, TypeError) as error:

        # 오류 발생 시 대체 메시지 반환
        print("Weather API error:", error)

        return {
            "city": "Seoul",
            "temperature": None,
            "weather": "Weather information unavailable",
            "status": "error"
        }


# 파일을 직접 실행한 경우에만 테스트 결과 출력
if __name__ == "__main__":

    weather_data = get_weather()

    print("===== MORNING WEATHER =====")
    print("City:", weather_data["city"])
    print("Temperature:", weather_data["temperature"])
    print("Weather:", weather_data["weather"])
    print("Status:", weather_data["status"])
