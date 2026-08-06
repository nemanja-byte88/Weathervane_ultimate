import tkinter as tk
from tkinter import ttk, font
import requests
import datetime

# ============================================================
# DATA FUNKCIJE (isto kao v2 + jedna nova za 7-dnevnu prognozu)
# ============================================================

def get_coordinates(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    response = requests.get(url)
    data = response.json()
    if "results" not in data:
        return None
    result = data["results"][0]
    return result["latitude"], result["longitude"], result["name"], result["country"]

def weather_icon(code):
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

def get_weekly_forecast(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,weathercode,precipitation_sum"
        f"&forecast_days=7&timezone=auto"
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
        return "Nizak seizmički rizik", "#30d158"
    elif count < 10:
        return "Umjeren seizmički rizik", "#ff9f0a"
    else:
        return "Visok seizmički rizik (seizmički aktivna zona)", "#ff453a"

def get_aqi_color(aqi):
    if aqi == "N/A":
        return "#8e8e93"
    if aqi <= 50:
        return "#30d158"
    elif aqi <= 100:
        return "#ff9f0a"
    else:
        return "#ff453a"

# ============================================================
# GUI HELPER FUNKCIJE ZA "KARTICE"
# ============================================================

BG = "#1c1c1e"
CARD_BG = "#2c2c2e"
ORANGE = "#ff9f0a"
WHITE = "white"
GRAY = "#a1a1a6"

def make_scrollable(parent):
    """Napravi scroll-abilan frame unutar taba."""
    canvas = tk.Canvas(parent, bg=BG, highlightthickness=0)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas, bg=BG)

    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=inner, anchor="nw", width=460)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return inner

def make_card(parent, title):
    """Napravi karticu (frame) sa naslovom unutar taba."""
    card = tk.Frame(parent, bg=CARD_BG, padx=15, pady=12)
    card.pack(fill="x", padx=10, pady=6)

    title_label = tk.Label(card, text=title, font=("Segoe UI", 12, "bold"),
                            bg=CARD_BG, fg=ORANGE, anchor="w")
    title_label.pack(fill="x", pady=(0, 8))
    return card

def add_row(card, label_text, value_text, value_color=WHITE):
    row = tk.Frame(card, bg=CARD_BG)
    row.pack(fill="x", pady=2)
    tk.Label(row, text=label_text, font=("Segoe UI", 10), bg=CARD_BG, fg=GRAY,
              anchor="w").pack(side="left")
    tk.Label(row, text=value_text, font=("Segoe UI", 10, "bold"), bg=CARD_BG,
              fg=value_color, anchor="e").pack(side="right")

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# ============================================================
# STANJE APLIKACIJE (za lazy loading)
# ============================================================

app_state = {
    "coords": None,     # (lat, lon, name, country)
    "loaded": {"today": False, "sea": False, "air": False, "land": False}
}

# ============================================================
# TODAY TAB
# ============================================================

def load_today():
    lat, lon, name, country = app_state["coords"]
    clear_frame(today_scroll)

    header = tk.Label(today_scroll, text=f"📍 {name}, {country}", font=("Segoe UI", 13, "bold"),
                       bg=BG, fg=WHITE)
    header.pack(anchor="w", padx=10, pady=(5, 10))

    data = get_today_weather(lat, lon)
    current = data.get("current", {})
    hourly = data.get("hourly", {})

    temp = current.get("temperature_2m", "N/A")
    feels = current.get("apparent_temperature", "N/A")
    humidity = current.get("relative_humidity_2m", "N/A")
    precip = current.get("precipitation", 0)
    uv = current.get("uv_index", 0)
    code = current.get("weathercode", 0)

    # Trenutno vrijeme - velika kartica
    now_card = make_card(today_scroll, f"{weather_icon(code)} Trenutno vrijeme")
    add_row(now_card, "Temperatura", f"{temp}°C")
    add_row(now_card, "Osjećaj", f"{feels}°C")
    add_row(now_card, "Vlažnost", f"{humidity}%")
    add_row(now_card, "Padavine", f"{precip} mm")
    add_row(now_card, "UV indeks", f"{uv}")

    # Tip kartica
    tip = get_tip(temp if isinstance(temp, (int, float)) else 0, precip, uv)
    tip_card = tk.Frame(today_scroll, bg="#3a2a12", padx=15, pady=10)
    tip_card.pack(fill="x", padx=10, pady=6)
    tk.Label(tip_card, text=f"💡 {tip}", font=("Segoe UI", 10), bg="#3a2a12",
              fg=ORANGE, wraplength=420, justify="left").pack(anchor="w")

    # 24h prognoza
    hourly_card = make_card(today_scroll, "🕒 24h prognoza")
    hourly_times = hourly.get("time", [])[:24]
    hourly_temps = hourly.get("temperature_2m", [])[:24]
    hourly_codes = hourly.get("weathercode", [])[:24]

    grid = tk.Frame(hourly_card, bg=CARD_BG)
    grid.pack(fill="x")
    col = 0
    for i in range(0, len(hourly_times), 3):
        t = hourly_times[i][-5:]
        temp_h = hourly_temps[i]
        icon_h = weather_icon(hourly_codes[i])
        cell = tk.Frame(grid, bg=CARD_BG)
        cell.grid(row=0, column=col, padx=8)
        tk.Label(cell, text=t, font=("Segoe UI", 9), bg=CARD_BG, fg=GRAY).pack()
        tk.Label(cell, text=icon_h, font=("Segoe UI", 16), bg=CARD_BG, fg=WHITE).pack()
        tk.Label(cell, text=f"{temp_h}°", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=WHITE).pack()
        col += 1

    # 7-dnevni pregled
    week_data = get_weekly_forecast(lat, lon)
    daily = week_data.get("daily", {})
    week_card = make_card(today_scroll, "📅 7 dana")

    days = daily.get("time", [])
    max_t = daily.get("temperature_2m_max", [])
    min_t = daily.get("temperature_2m_min", [])
    codes = daily.get("weathercode", [])
    precip_sum = daily.get("precipitation_sum", [])

    for i in range(len(days)):
        date_obj = datetime.date.fromisoformat(days[i])
        day_name = date_obj.strftime("%a %d.%m")
        icon = weather_icon(codes[i])
        avg = round((max_t[i] + min_t[i]) / 2, 1)

        row = tk.Frame(week_card, bg=CARD_BG)
        row.pack(fill="x", pady=3)
        tk.Label(row, text=day_name, font=("Segoe UI", 10), bg=CARD_BG, fg=GRAY, width=12,
                  anchor="w").pack(side="left")
        tk.Label(row, text=icon, font=("Segoe UI", 12), bg=CARD_BG, fg=WHITE, width=3).pack(side="left")
        tk.Label(row, text=f"↑{max_t[i]}° ↓{min_t[i]}°  (Ø{avg}°)", font=("Segoe UI", 10, "bold"),
                  bg=CARD_BG, fg=WHITE).pack(side="left", padx=5)
        if precip_sum[i] and precip_sum[i] > 0:
            tk.Label(row, text=f"🌧 {precip_sum[i]}mm", font=("Segoe UI", 9),
                      bg=CARD_BG, fg="#64d2ff").pack(side="right")

    app_state["loaded"]["today"] = True

# ============================================================
# SEA TAB
# ============================================================

def load_sea():
    lat, lon, name, country = app_state["coords"]
    clear_frame(sea_scroll)

    tk.Label(sea_scroll, text=f"📍 {name}, {country}", font=("Segoe UI", 13, "bold"),
             bg=BG, fg=WHITE).pack(anchor="w", padx=10, pady=(5, 10))

    sea_data = get_sea_data(lat, lon)
    wind_data = get_wind_for_sea(lat, lon)
    moon_name, tide_strength = get_moon_tide_estimate()

    current = sea_data.get("current", {})
    wind_current = wind_data.get("current", {})

    wave_card = make_card(sea_scroll, "🌊 Talasi")
    add_row(wave_card, "Visina", f"{current.get('wave_height', 'N/A')} m")
    add_row(wave_card, "Smjer", f"{current.get('wave_direction', 'N/A')}°")
    add_row(wave_card, "Period", f"{current.get('wave_period', 'N/A')} s")

    water_card = make_card(sea_scroll, "🌡️ Temperatura i struje")
    add_row(water_card, "Temperatura mora", f"{current.get('sea_surface_temperature', 'N/A')}°C")
    add_row(water_card, "Brzina struje", f"{current.get('ocean_current_velocity', 'N/A')} km/h")
    add_row(water_card, "Smjer struje", f"{current.get('ocean_current_direction', 'N/A')}°")

    wind_card = make_card(sea_scroll, "💨 Vjetar (dokiranje)")
    add_row(wind_card, "Brzina", f"{wind_current.get('wind_speed_10m', 'N/A')} km/h")
    add_row(wind_card, "Smjer", f"{wind_current.get('wind_direction_10m', 'N/A')}°")

    moon_card = make_card(sea_scroll, "🌙 Mjesec i plima/oseka")
    add_row(moon_card, "Faza", moon_name)
    add_row(moon_card, "Procjena", tide_strength, ORANGE)
    tk.Label(moon_card, text="(okvirna procjena, nije precizna)", font=("Segoe UI", 8, "italic"),
              bg=CARD_BG, fg=GRAY).pack(anchor="w", pady=(5, 0))

    app_state["loaded"]["sea"] = True

# ============================================================
# AIR TAB
# ============================================================

def load_air():
    lat, lon, name, country = app_state["coords"]
    clear_frame(air_scroll)

    tk.Label(air_scroll, text=f"📍 {name}, {country}", font=("Segoe UI", 13, "bold"),
             bg=BG, fg=WHITE).pack(anchor="w", padx=10, pady=(5, 10))

    data = get_air_data(lat, lon)
    current = data.get("current", {})
    hourly = data.get("hourly", {})

    wind_card = make_card(air_scroll, "💨 Vjetar po visinama")
    add_row(wind_card, "10m", f"{current.get('wind_speed_10m', 'N/A')} km/h ({current.get('wind_direction_10m', 'N/A')}°)")
    add_row(wind_card, "80m", f"{hourly.get('wind_speed_80m', ['N/A'])[0]} km/h")
    add_row(wind_card, "120m", f"{hourly.get('wind_speed_120m', ['N/A'])[0]} km/h")

    cond_card = make_card(air_scroll, "📊 Uslovi")
    add_row(cond_card, "Pritisak", f"{current.get('pressure_msl', 'N/A')} hPa")
    add_row(cond_card, "Vidljivost", f"{current.get('visibility', 'N/A')} m")

    app_state["loaded"]["air"] = True

# ============================================================
# LAND TAB
# ============================================================

def load_land():
    lat, lon, name, country = app_state["coords"]
    clear_frame(land_scroll)

    tk.Label(land_scroll, text=f"📍 {name}, {country}", font=("Segoe UI", 13, "bold"),
             bg=BG, fg=WHITE).pack(anchor="w", padx=10, pady=(5, 10))

    aq_data = get_air_quality(lat, lon)
    soil_data = get_soil_data(lat, lon)
    quakes = get_earthquakes(lat, lon)
    risk_text, risk_color = get_seismic_risk(lat, lon)

    aq_current = aq_data.get("current", {})
    soil_current = soil_data.get("current", {})

    aqi = aq_current.get("european_aqi", "N/A")
    aq_card = make_card(land_scroll, "🌫️ Kvalitet vazduha")
    add_row(aq_card, "PM2.5", f"{aq_current.get('pm2_5', 'N/A')} µg/m³")
    add_row(aq_card, "PM10", f"{aq_current.get('pm10', 'N/A')} µg/m³")
    add_row(aq_card, "AQI (evropski)", f"{aqi}", get_aqi_color(aqi))
    add_row(aq_card, "Polen trave", f"{aq_current.get('grass_pollen', 'N/A')}")

    soil_card = make_card(land_scroll, "🌱 Tlo")
    add_row(soil_card, "Temperatura tla", f"{soil_current.get('soil_temperature_0cm', 'N/A')}°C")
    add_row(soil_card, "Vlažnost tla", f"{soil_current.get('soil_moisture_0_to_1cm', 'N/A')}")

    quake_card = make_card(land_scroll, "🌍 Seizmička aktivnost")
    quake_features = quakes.get("features", [])
    if quake_features:
        for f in quake_features[:3]:
            mag = f["properties"]["mag"]
            place = f["properties"]["place"]
            add_row(quake_card, f"M{mag}", place)
    else:
        tk.Label(quake_card, text="Nema zabilježenih u zadnjih 30 dana", font=("Segoe UI", 9),
                  bg=CARD_BG, fg=GRAY).pack(anchor="w")
    add_row(quake_card, "Rizik regije", risk_text, risk_color)

    app_state["loaded"]["land"] = True

# ============================================================
# PRETRAGA I LAZY LOADING LOGIKA
# ============================================================

def search_city():
    city = city_entry.get()
    if not city:
        return
    coords = get_coordinates(city)
    if coords is None:
        clear_frame(today_scroll)
        tk.Label(today_scroll, text="Grad nije pronađen.", font=("Segoe UI", 11),
                  bg=BG, fg=WHITE).pack(pady=20)
        return

    app_state["coords"] = coords
    app_state["loaded"] = {"today": False, "sea": False, "air": False, "land": False}

    # Ucitaj samo trenutno aktivan tab
    load_current_tab()

def load_current_tab():
    if app_state["coords"] is None:
        return
    current_tab = notebook.index(notebook.select())
    tab_names = ["today", "sea", "air", "land"]
    tab_name = tab_names[current_tab]

    if app_state["loaded"][tab_name]:
        return  # vec ucitano, ne ucitavaj ponovo

    if tab_name == "today":
        load_today()
    elif tab_name == "sea":
        load_sea()
    elif tab_name == "air":
        load_air()
    elif tab_name == "land":
        load_land()

def on_tab_changed(event):
    load_current_tab()

# ============================================================
# GUI SETUP
# ============================================================

root = tk.Tk()
root.title("Weather App v3")
root.geometry("520x650")
root.configure(bg=BG)

title_font = font.Font(family="Segoe UI", size=18, weight="bold")
label_font = font.Font(family="Segoe UI", size=12)

title = tk.Label(root, text="Weather App", font=title_font, bg=BG, fg=ORANGE)
title.pack(pady=15)

search_frame = tk.Frame(root, bg=BG)
search_frame.pack(pady=5)

city_entry = tk.Entry(search_frame, font=label_font, width=25)
city_entry.pack(side="left", padx=5, ipady=4)
city_entry.bind("<Return>", lambda e: search_city())

search_btn = tk.Button(search_frame, text="Traži", font=label_font, bg=ORANGE, fg="black",
                        relief="flat", command=search_city)
search_btn.pack(side="left")

style = ttk.Style()
style.theme_use("default")
style.configure("TNotebook", background=BG, borderwidth=0)
style.configure("TNotebook.Tab", background=CARD_BG, foreground="white", padding=[10, 5])
style.map("TNotebook.Tab", background=[("selected", ORANGE)], foreground=[("selected", "black")])

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)
notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

today_frame = tk.Frame(notebook, bg=BG)
notebook.add(today_frame, text="🏠 Today")
today_scroll = make_scrollable(today_frame)

sea_frame = tk.Frame(notebook, bg=BG)
notebook.add(sea_frame, text="🌊 Sea")
sea_scroll = make_scrollable(sea_frame)

air_frame = tk.Frame(notebook, bg=BG)
notebook.add(air_frame, text="✈️ Air")
air_scroll = make_scrollable(air_frame)

land_frame = tk.Frame(notebook, bg=BG)
notebook.add(land_frame, text="🌱 Land")
land_scroll = make_scrollable(land_frame)

# Placeholder poruke prije prve pretrage
for frame in [today_scroll, sea_scroll, air_scroll, land_scroll]:
    tk.Label(frame, text="Unesi grad i pretraži.", font=("Segoe UI", 11),
              bg=BG, fg=GRAY).pack(pady=30)

root.mainloop()