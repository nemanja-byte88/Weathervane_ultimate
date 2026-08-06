# Weathervane 🌤️

A multi-tab weather web app with real photographic scenes that shift with the time of day — read the sky before you head out.

**Live demo:** [mellifluous-faloodeh-71e879.netlify.app](https://mellifluous-faloodeh-71e879.netlify.app)

## Features

- **5 tabs** — Today, Sea, Air, Land, and Activities, each pulling different data for the searched location
- **Phase-based scenery** — every tab has 4 real photographs (day / dusk / dawn / night) that swap automatically based on the actual sunrise/sunset time at the searched city
- **City search with autocomplete** — debounced search with keyboard navigation
- **Unit toggles** — °C/°F, km/h/mph, m/ft, applied instantly from cached data (no extra API calls)
- **Activities rating** — rates hiking, cycling, camping, fishing and more against the next 24h of weather
- **Beaufort scale** — wind force description on the Sea tab, for a sailing-relevant read on wind speed
- **Lazy loading** — each tab only fetches data when opened, and caches it for instant unit conversion

## Data sources

- [Open-Meteo](https://open-meteo.com/) — forecast, marine, and air quality APIs
- [USGS](https://earthquake.usgs.gov/) — recent earthquake and seismic risk data
- Moon phase and tide estimate calculated locally (no API)

## Tech stack

Vanilla HTML, CSS, and JavaScript — no frameworks, no build step. Deployed on Netlify.

## Project history

This app started as a Python terminal script, evolved into a Tkinter desktop GUI, and was finally rebuilt as this web app. The earlier Python versions are included in this repo for reference.

## Screenshots

*(add a couple of screenshots here later — Today tab at day and Sea tab at night look great side by side)*
