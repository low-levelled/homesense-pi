import os
import requests

def read_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            raw_temp = f.read().strip()
            celsius = int(raw_temp) / 1000.0
            farenheit = (celsius * 9/5) + 32
            
            if farenheit < 130:
                status = "Idle/Light Use"
            elif farenheit < 158:
                status = "Moderate Use"
            elif farenheit < 176:
                status = "Heavy Load"
            else:
                status = "Danger: Throttling Likely"
            return (f"CPU Temperature: {celsius:.2f} C | {farenheit:.2f} F - Status: {status}")
        
    except Exception as e:
        return (f"Failed to read temperature: {e}")
    
    
def get_location_coords():
    try:
        response = requests.get("https://ipinfo.io/json", timeout=5)
        data = response.json()
        loc = data["loc"]
        lat, lon = map(float, loc.split(","))
        city = data.get("city", "Unknown City")
        return lat, lon, city
    except Exception as e:
        print(f"Error getting location: {e}")
        return None, None
    
def get_local_weather():
    lat, lon, city = get_location_coords()
    if lat is None:
        return "Could not get location"
    
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url)
        data = response.json()
        celsius = data["current_weather"]["temperature"]
        farenheit = (celsius * 9/5) + 32
        wind = data["current_weather"]["windspeed"]
        return f"{city} Local weather: {farenheit}*F, Wind: {wind} km/hr (lat: {lat}, lon: {lon})"
    except Exception as e:
        return f"Failed to get weather: {e}"

        
if __name__ == "__main__" :
    print(read_temp())
    print(get_local_weather())