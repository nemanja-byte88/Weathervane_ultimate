import tkinter as tk
from tkinter import ttk, font
import requests
import datetime

# ---------- OSNOVNO ----------

def get_coordinates(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    response = requests.get(url)
    data = response.json()
    if "results" not in data:
        return None
    result = data["results"][0]
    return result["latitude"], result["longitude"], result["name"], result["country"]

# ---------- TODAY TAB ----------

def get_today_weather(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,apparent_temperature,relative_humidity_2m,precipitation,weathercode,uv_index"
        f"&hourly=temperature_2m,weathercode,precipitation_probability"
        f"&forecast_days=1&timezone=auto"
    )
    response = requests.get(url)
    return response.json()

def get_tip(temp, precipitation, uv_index):
    tips = []
    if temp >= 28:
        tips.append("Vruće je - stavi kremu za sunčanje i pij dosta vode ☀️")
    elif temp <= 5:
        tips.append("Hladno je - obuci se toplije 🧥")
    if precipitation and precipitation > 0:
        tips.append("Očekuje se kiša - ponesi kišobran ☂️")
    if uv_index and uv_index >= 6:
        tips.append("Visok UV indeks - izbjegavaj sunce u podne 🕶️")
    if not tips:
        tips.append("Uslovi su prijatni, uživaj u danu! 🙂")
    return " | ".join(tips)

# ---------- SEA TAB ----------

def get_sea_data(lat, lon):
    url = (
        f"https://marine-api.open-meteo.com/v1/marine?"
        f"latitude={lat}&longitude={lon}"
        f"&current=wave_height,wave_direction,wave_period,sea_surface_temperature,"
        f"ocean_current_velocity,ocean_current_direction"
        f"&timezone=auto"
    )
    response = requests.get(url)
    return response.json()

def get_wind_for_sea(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=wind_speed_10m,wind_direction_10m&timezone=auto"
    )
    response = requests.get(url)
    return response.json()

def get_moon_tide_estimate():
    # Referentni mlad mjesec (poznat datum)
    known_new_moon = datetime.date(2000, 1, 6)
    days_since = (datetime.date.today() - known_new_moon).days
    lunations = days_since / 29.53058867
    phase = lunations % 1

    if phase < 0.03 or phase > 0.97:
        moon_name = "Mlad mjesec 🌑"
        tide_strength = "Jača plima/oseka (spring tide)"
    elif 0.22 < phase < 0.28:
        moon_name = "Prva četvrt 🌓"
        tide_strength = "Slabija plima/oseka (neap tide)"
    elif 0.47 < phase < 0.53:
        moon_name = "Pun mjesec 🌕"
        tide_strength = "Jača plima/oseka (spring tide)"
    elif 0.72 < phase < 0.78:
        moon_name = "Zadnja četvrt 🌗"
        tide_strength = "Slabija plima/oseka (neap tide)"
    else:
        moon_name = "Prelazna faza 🌒"
        tide_strength = "Umjerena plima/oseka"

    return moon_name, tide_strength

# ---------- AIR TAB ----------

def get_air_data(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=wind_speed_10m,wind_direction_10m,pressure_msl,visibility"
        f"&hourly=wind_speed_80m,wind_speed_120m"
        f"&forecast_days=1&timezone=auto"
    )
    response = requests.get(url)
    return response.json()

# ---------- LAND TAB ----------

def get_air_quality(lat, lon):
    url = (
        f"https://air-quality-api.open-meteo.com/v1/air-quality?"
        f"latitude={lat}&longitude={lon}"
        f"&current=pm2_5,pm10,european_aqi,alder_pollen,birch_pollen,grass_pollen,ragweed_pollen"
        f"&timezone=auto"
    )
    response = requests.get(url)
    return response.json()

def get_soil_data(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=soil_temperature_0cm,soil_moisture_0_to_1cm"
        f"&timezone=auto"
    )
    response = requests.get(url)
    return response.json()

def get_earthquakes(lat, lon):
    # Nedavni zemljotresi (zadnjih 30 dana, u radijusu 300km)
    start = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
    url = (
        f"https://earthquake.usgs.gov/fdsnws/event/1/query?"
        f"format=geojson&latitude={lat}&longitude={lon}"
        f"&maxradiuskm=300&minmagnitude=2.5&starttime={start}"
        f"&orderby=time&limit=5"
    )
    response = requests.get(url)
    return response.json()

def get_seismic_risk(lat, lon):
    # Seizmicki rizik na osnovu ucestalosti u zadnjih godinu dana, radijus 500km
    start = (datetime.date.today() - datetime.timedelta(days=365)).isoformat()
    url = (
        f"https://earthquake.usgs.gov/fdsnws/event/1/query?"
        f"format=geojson&latitude={lat}&longitude={lon}"
        f"&maxradiuskm=500&minmagnitude=3.0&starttime={start}"
    )
    response = requests.get(url)
    data = response.json()
    count = len(data.get("features", []))

    if count == 0:
        return "Nizak seizmički rizik"
    elif count < 10:
        return "Umjeren seizmički rizik"
    else:
        return "Visok seizmički rizik (seizmički aktivna zona)" 

# ---------- HELPER ZA FORMATIRANJE ----------

def safe_get(d, *keys, default="N/A"):
    for k in keys:
        if d is None:
            return default
        d = d.get(k) if isinstance(d, dict) else None
    return d if d is not None else default

# ---------- TODAY TAB ----------

def load_today(city):
    coords = get_coordinates(city)
    if coords is None:
        today_result.config(text="Grad nije pronađen.")
        return
    lat, lon, name, country = coords

    data = get_today_weather(lat, lon)
    current = data.get("current", {})
    hourly = data.get("hourly", {})

    temp = current.get("temperature_2m", "N/A")
    feels = current.get("apparent_temperature", "N/A")
    humidity = current.get("relative_humidity_2m", "N/A")
    precip = current.get("precipitation", 0)
    uv = current.get("uv_index", 0)

    tip = get_tip(temp if isinstance(temp, (int, float)) else 0,
                  precip, uv)

    # 24h prognoza - sledecih 8 termina (svaka 3h da stane)
    hourly_temps = hourly.get("temperature_2m", [])[:24]
    hourly_times = hourly.get("time", [])[:24]

    hourly_text = ""
    for i in range(0, len(hourly_times), 3):
        t = hourly_times[i][-5:]  # samo HH:MM
        temp_h = hourly_temps[i]
        hourly_text += f"{t}  {temp_h}°C\n"

    today_result.config(
        text=f"📍 {name}, {country}\n\n"
             f"Temperatura: {temp}°C\n"
             f"Osjećaj: {feels}°C\n"
             f"Vlažnost: {humidity}%\n"
             f"Padavine: {precip} mm\n"
             f"UV indeks: {uv}\n\n"
             f"— 24h prognoza —\n{hourly_text}\n"
             f"💡 {tip}"
    )

# ---------- SEA TAB ----------

def load_sea(city):
    coords = get_coordinates(city)
    if coords is None:
        sea_result.config(text="Grad nije pronađen.")
        return
    lat, lon, name, country = coords

    sea_data = get_sea_data(lat, lon)
    wind_data = get_wind_for_sea(lat, lon)
    moon_name, tide_strength = get_moon_tide_estimate()

    current = sea_data.get("current", {})
    wind_current = wind_data.get("current", {})

    wave_h = current.get("wave_height", "N/A")
    wave_dir = current.get("wave_direction", "N/A")
    wave_period = current.get("wave_period", "N/A")
    sea_temp = current.get("sea_surface_temperature", "N/A")
    current_vel = current.get("ocean_current_velocity", "N/A")
    current_dir = current.get("ocean_current_direction", "N/A")

    wind_speed = wind_current.get("wind_speed_10m", "N/A")
    wind_dir = wind_current.get("wind_direction_10m", "N/A")

    sea_result.config(
        text=f"📍 {name}, {country}\n\n"
             f"Visina talasa: {wave_h} m\n"
             f"Smjer talasa: {wave_dir}°\n"
             f"Period talasa: {wave_period} s\n"
             f"Temperatura mora: {sea_temp}°C\n"
             f"Morska struja: {current_vel} km/h ({current_dir}°)\n\n"
             f"Vjetar (za dokiranje): {wind_speed} km/h ({wind_dir}°)\n\n"
             f"🌙 {moon_name}\n"
             f"Procjena: {tide_strength}\n"
             f"(napomena: okvirna procjena, nije precizna)"
    )

# ---------- AIR TAB ----------

def load_air(city):
    coords = get_coordinates(city)
    if coords is None:
        air_result.config(text="Grad nije pronađen.")
        return
    lat, lon, name, country = coords

    data = get_air_data(lat, lon)
    current = data.get("current", {})
    hourly = data.get("hourly", {})

    wind_speed = current.get("wind_speed_10m", "N/A")
    wind_dir = current.get("wind_direction_10m", "N/A")
    pressure = current.get("pressure_msl", "N/A")
    visibility = current.get("visibility", "N/A")

    wind_80 = hourly.get("wind_speed_80m", ["N/A"])[0]
    wind_120 = hourly.get("wind_speed_120m", ["N/A"])[0]

    air_result.config(
        text=f"📍 {name}, {country}\n\n"
             f"Vjetar (10m): {wind_speed} km/h ({wind_dir}°)\n"
             f"Vjetar (80m): {wind_80} km/h\n"
             f"Vjetar (120m): {wind_120} km/h\n"
             f"Pritisak: {pressure} hPa\n"
             f"Vidljivost: {visibility} m"
    )

# ---------- LAND TAB ----------

def load_land(city):
    coords = get_coordinates(city)
    if coords is None:
        land_result.config(text="Grad nije pronađen.")
        return
    lat, lon, name, country = coords

    aq_data = get_air_quality(lat, lon)
    soil_data = get_soil_data(lat, lon)
    quakes = get_earthquakes(lat, lon)
    risk = get_seismic_risk(lat, lon)

    aq_current = aq_data.get("current", {})
    soil_current = soil_data.get("current", {})

    pm25 = aq_current.get("pm2_5", "N/A")
    pm10 = aq_current.get("pm10", "N/A")
    aqi = aq_current.get("european_aqi", "N/A")
    grass = aq_current.get("grass_pollen", "N/A")

    soil_temp = soil_current.get("soil_temperature_0cm", "N/A")
    soil_moisture = soil_current.get("soil_moisture_0_to_1cm", "N/A")

    quake_features = quakes.get("features", [])
    if quake_features:
        quake_text = ""
        for f in quake_features[:3]:
            mag = f["properties"]["mag"]
            place = f["properties"]["place"]
            quake_text += f"  M{mag} - {place}\n"
    else:
        quake_text = "  Nema zabilježenih u zadnjih 30 dana\n"

    land_result.config(
        text=f"📍 {name}, {country}\n\n"
             f"— Kvalitet vazduha —\n"
             f"PM2.5: {pm25} µg/m³\n"
             f"PM10: {pm10} µg/m³\n"
             f"AQI (evropski): {aqi}\n"
             f"Polen trave: {grass}\n\n"
             f"— Tlo —\n"
             f"Temperatura tla: {soil_temp}°C\n"
             f"Vlažnost tla: {soil_moisture}\n\n"
             f"— Zemljotresi (zadnjih 30 dana) —\n{quake_text}\n"
             f"Seizmički rizik regije: {risk}"
    )

# ---------- GLAVNA FUNKCIJA PRETRAGE ----------

def search_all():
    city = city_entry.get()
    if not city:
        return
    load_today(city)
    load_sea(city)
    load_air(city)
    load_land(city)

# ---------- GUI SETUP ----------

root = tk.Tk()
root.title("Weather App")
root.geometry("500x600")
root.configure(bg="#1c1c1e")

title_font = font.Font(family="Segoe UI", size=18, weight="bold")
label_font = font.Font(family="Segoe UI", size=12)
result_font = font.Font(family="Segoe UI", size=11)

title = tk.Label(root, text="Weather App", font=title_font, bg="#1c1c1e", fg="#ff9f0a")
title.pack(pady=15)

search_frame = tk.Frame(root, bg="#1c1c1e")
search_frame.pack(pady=5)

city_entry = tk.Entry(search_frame, font=label_font, width=25)
city_entry.pack(side="left", padx=5, ipady=4)

search_btn = tk.Button(
    search_frame, text="Traži", font=label_font,
    bg="#ff9f0a", fg="black", relief="flat",
    command=search_all
)
search_btn.pack(side="left")

# --- Notebook (tabovi) ---
style = ttk.Style()
style.theme_use("default")
style.configure("TNotebook", background="#1c1c1e", borderwidth=0)
style.configure("TNotebook.Tab", background="#2c2c2e", foreground="white", padding=[10, 5])
style.map("TNotebook.Tab", background=[("selected", "#ff9f0a")], foreground=[("selected", "black")])

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=15, pady=15)

# Today tab
today_frame = tk.Frame(notebook, bg="#1c1c1e")
notebook.add(today_frame, text="🏠 Today")
today_result = tk.Label(today_frame, text="Unesi grad i pretraži.", font=result_font,
                         bg="#1c1c1e", fg="white", justify="left", anchor="nw")
today_result.pack(padx=10, pady=10, anchor="nw")

# Sea tab
sea_frame = tk.Frame(notebook, bg="#1c1c1e")
notebook.add(sea_frame, text="🌊 Sea")
sea_result = tk.Label(sea_frame, text="Unesi grad i pretraži.", font=result_font,
                       bg="#1c1c1e", fg="white", justify="left", anchor="nw")
sea_result.pack(padx=10, pady=10, anchor="nw")

# Air tab
air_frame = tk.Frame(notebook, bg="#1c1c1e")
notebook.add(air_frame, text="✈️ Air")
air_result = tk.Label(air_frame, text="Unesi grad i pretraži.", font=result_font,
                       bg="#1c1c1e", fg="white", justify="left", anchor="nw")
air_result.pack(padx=10, pady=10, anchor="nw")

# Land tab
land_frame = tk.Frame(notebook, bg="#1c1c1e")
notebook.add(land_frame, text="🌱 Land")
land_result = tk.Label(land_frame, text="Unesi grad i pretraži.", font=result_font,
                        bg="#1c1c1e", fg="white", justify="left", anchor="nw")
land_result.pack(padx=10, pady=10, anchor="nw")

root.mainloop()