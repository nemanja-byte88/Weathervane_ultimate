# 🌦️ Weathervane

A weather web app that goes beyond a simple forecast — the background changes to a real photographic scene matching the actual sunrise/sunset phase of the day at your location, so the app *looks* like the moment you're in.

**Live demo:** [Add your Netlify URL here]

---

## ✨ Features

- **Multi-tab interface** for browsing current conditions, forecast, and details
- **Phase-based backgrounds** — photographic imagery tied to real sunrise/sunset times (dawn, day, dusk, night) rather than generic icons
- **Beaufort wind scale integration** — wind speed shown in a scale sailors and meteorologists actually use, not just raw km/h
- **Optimized images** — backgrounds converted to WebP and embedded as base64 to keep load times fast without external image requests

## 🛠️ Built With

- HTML / CSS / JavaScript
- Weather data API
- Netlify (hosting/deployment)

## 🚀 Run Locally

Open `index.html` directly in any browser — no build step, no dependencies.

## 📦 Deploy

1. Go to [netlify.com](https://netlify.com)
2. Drag & drop the project folder (or connect the GitHub repo for auto-deploy)
3. Get a public link instantly

## 📁 Project Structure

```
Weathervane_ultimate/
├── index.html          # Main web app
├── archive/             # Earlier Python prototype iterations (dev history)
└── README.md
```

## 🗺️ Development Notes

This project evolved from early Python prototypes (see `/archive`) into a polished single-file web app. Along the way it involved resolving Git merge conflicts and iterating on image-loading performance.

## 👤 Author

**nemanja-byte88** — [GitHub](https://github.com/nemanja-byte88)\
