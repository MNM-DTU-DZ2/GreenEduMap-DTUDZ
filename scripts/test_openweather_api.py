#!/usr/bin/env python3
"""
Test OpenWeather API Key
Test xem API key có hoạt động không
"""

import requests
import json
from datetime import datetime

# API Configuration
API_KEY = "30de77839a05db1dfe983c341a297838"
BASE_URL = "https://api.openweathermap.org/data/2.5"

# Test location: Da Nang, Vietnam
LAT = 16.0544
LON = 108.2022

def test_current_weather():
    """Test Current Weather API"""
    print("=" * 60)
    print("🌤️  Testing OpenWeather API - Current Weather")
    print("=" * 60)
    
    url = f"{BASE_URL}/weather"
    params = {
        "lat": LAT,
        "lon": LON,
        "appid": API_KEY,
        "units": "metric"  # Celsius
    }
    
    print(f"\n📍 Location: Da Nang ({LAT}, {LON})")
    print(f"🔑 API Key: {API_KEY[:10]}...")
    print(f"🌐 Request URL: {url}")
    print(f"📋 Parameters: {params}\n")
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"⏱️  Response Time: {response.elapsed.total_seconds():.2f}s\n")
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ SUCCESS! API Key is valid!\n")
            print("=" * 60)
            print("📦 Weather Data:")
            print("=" * 60)
            
            # Parse and display weather info
            main = data.get('main', {})
            weather = data.get('weather', [{}])[0]
            wind = data.get('wind', {})
            
            print(f"🏙️  City: {data.get('name')}")
            print(f"🌡️  Temperature: {main.get('temp')}°C")
            print(f"🤔 Feels Like: {main.get('feels_like')}°C")
            print(f"💧 Humidity: {main.get('humidity')}%")
            print(f"🌬️  Wind Speed: {wind.get('speed')} m/s")
            print(f"☁️  Weather: {weather.get('main')} - {weather.get('description')}")
            print(f"🔬 Pressure: {main.get('pressure')} hPa")
            
            # Full response
            print("\n" + "=" * 60)
            print("📄 Full API Response:")
            print("=" * 60)
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            return True
            
        elif response.status_code == 401:
            print("❌ FAILED! API Key is invalid or unauthorized")
            print(f"Response: {response.text}")
            return False
            
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ ERROR: Request timeout!")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")
        return False


def test_forecast():
    """Test Forecast API"""
    print("\n\n" + "=" * 60)
    print("🌦️  Testing OpenWeather API - 5-Day Forecast")
    print("=" * 60)
    
    url = f"{BASE_URL}/forecast"
    params = {
        "lat": LAT,
        "lon": LON,
        "appid": API_KEY,
        "units": "metric"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            forecast_list = data.get('list', [])[:5]  # First 5 items
            
            print(f"✅ SUCCESS! Got {len(forecast_list)} forecast entries\n")
            
            for item in forecast_list:
                dt = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M')
                temp = item['main']['temp']
                weather_desc = item['weather'][0]['description']
                print(f"  📅 {dt}: {temp}°C - {weather_desc}")
            
            return True
        else:
            print(f"❌ FAILED! Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def main():
    """Main test function"""
    print("\n" + "🌍" * 30)
    print("OpenWeather API Key Tester")
    print("🌍" * 30 + "\n")
    
    # Test current weather
    current_ok = test_current_weather()
    
    # Test forecast
    forecast_ok = test_forecast()
    
    # Summary
    print("\n\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"Current Weather: {'✅ PASS' if current_ok else '❌ FAIL'}")
    print(f"Forecast API: {'✅ PASS' if forecast_ok else '❌ FAIL'}")
    
    if current_ok and forecast_ok:
        print("\n🎉 All tests passed! API key is working perfectly!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check API key or network.")
        return 1


if __name__ == "__main__":
    exit(main())
