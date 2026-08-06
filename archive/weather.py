import requests

def get_coordinates(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    response = requests.get(url)
    data = response.json()
    if "results" not in data:
        return None
    result = data["results"][0]
    return result["latitude"], result["longitude"], result["name"], result["country"]

def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    return response.json()["current_weather"]

def main():
    city = input("Unesi ime grada: ")
    coords = get_coordinates(city)
    
    if coords is None:
        print("Grad nije pronađen.")
        return
    
    lat, lon, name, country = coords
    weather = get_weather(lat, lon)
    
    print(f"\nVrijeme u {name}, {country}:")
    print(f"Temperatura: {weather['temperature']}°C")
    print(f"Brzina vjetra: {weather['windspeed']} km/h")

if __name__ == "__main__":
    main()