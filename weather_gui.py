import tkinter as tk
from tkinter import font
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

def weather_icon(code):
    # Open-Meteo weather codes -> emoji
    if code == 0:
        return "☀️"
    elif code in [1, 2, 3]:
        return "⛅"
    elif code in [45, 48]:
        return "🌫️"
    elif code in range(51, 68):
        return "🌧️"
    elif code in range(71, 78):
        return "❄️"
    elif code in range(80, 83):
        return "🌦️"
    elif code in range(95, 100):
        return "⛈️"
    else:
        return "🌡️"

def search_weather():
    city = entry.get()
    if not city:
        result_label.config(text="Unesi ime grada.")
        return

    coords = get_coordinates(city)
    if coords is None:
        result_label.config(text="Grad nije pronađen.")
        return

    lat, lon, name, country = coords
    weather = get_weather(lat, lon)
    icon = weather_icon(weather["weathercode"])

    result_label.config(
        text=f"{icon}  {name}, {country}\n\n"
             f"Temperatura: {weather['temperature']}°C\n"
             f"Vjetar: {weather['windspeed']} km/h"
    )

# --- GUI setup ---
root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")
root.configure(bg="#1c1c1e")

title_font = font.Font(family="Segoe UI", size=18, weight="bold")
label_font = font.Font(family="Segoe UI", size=13)
result_font = font.Font(family="Segoe UI", size=14)

title = tk.Label(root, text="Weather App", font=title_font, bg="#1c1c1e", fg="#ff9f0a")
title.pack(pady=20)

entry = tk.Entry(root, font=label_font, justify="center")
entry.pack(pady=10, ipadx=10, ipady=5)
entry.insert(0, "Unesi grad...")

search_btn = tk.Button(
    root, text="Provjeri vrijeme", font=label_font,
    bg="#ff9f0a", fg="black", relief="flat",
    command=search_weather
)
search_btn.pack(pady=10, ipadx=10, ipady=5)

result_label = tk.Label(
    root, text="", font=result_font, bg="#1c1c1e", fg="white", justify="center"
)
result_label.pack(pady=20)

root.mainloop