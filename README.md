# 🌳 Green Spaces Mapper - Chennai

> **[🚀 Live Demo](https://green-space-mapperr.vercel.app/)** | **[📊 Analytics](https://green-space-mapperr.vercel.app/analytics)**

An interactive map tool that visualizes Chennai's parks, pollution levels, and EV stations — with ML predictions for where the city needs more trees.

---

## 💡 Why I Built This

Chennai lost 70% of its green cover in the last decade. I wanted to build something that actually helps identify where we need more trees — not just another pretty dashboard.

This tool lets you click anywhere on Chennai's map and get an instant ML-based prediction: "Does this area need more trees?" Based on AQI, temperature, existing green cover, and population density.

Built as part of my MSc Sustainability Management application portfolio.

---

## ✨ Features

| Feature | What It Does |
|---------|--------------|
| 🗺️ **Interactive Map** | 360+ parks & EV stations plotted with toggleable layers |
| 🤖 **AI Analysis** | Click anywhere → get ML prediction if area needs trees |
| 📊 **Analytics Dashboard** | City-wide stats, trends, district comparisons |
| 📈 **Before/After** | 2022 vs 2026 projected impact visualization |
| 💡 **Suggestions** | Community can suggest new park locations |
| 🌙 **Dark Mode** | Full theme toggle with localStorage persistence |

---

## 🛠️ Tech Stack

| Layer | Tech |
|-------|------|
| Backend | Python 3.12, Flask |
| Frontend | HTML, CSS, Vanilla JS |
| Maps | Folium, Leaflet.js, OpenStreetMap |
| Charts | Plotly.js |
| ML | scikit-learn (Random Forest) |
| Database | SQLite |
| Deployment | Vercel |

---

## 🚀 Run Locally

    # Clone
    git clone https://github.com/barishavm29-ui/green-spaces-mapper.git
    cd green-spaces-mapper

    # Setup
    conda create -n greenmap python=3.12 -y
    conda activate greenmap
    pip install -r requirements.txt

    # Fetch data & generate map
    python utils/data_fetcher.py
    python utils/map_generator.py
    python utils/ml_predictor.py

    # Run
    python app.py

Open http://localhost:5000

---

## 📂 Project Structure

    green-spaces-mapper/
    ├── app.py                  # Flask app
    ├── templates/              # HTML pages
    │   ├── index.html          # Map homepage
    │   ├── analytics.html      # Dashboard
    │   ├── compare.html        # Before/After
    │   └── suggest.html        # Suggestion form
    ├── static/
    │   ├── css/style.css       # Styling + dark mode
    │   └── js/                 # Interactivity
    ├── utils/
    │   ├── data_fetcher.py     # OpenStreetMap API
    │   ├── map_generator.py    # Folium map creation
    │   └── ml_predictor.py     # Random Forest model
    ├── data/
    │   └── green_spaces.db     # SQLite database
    └── models/
        └── tree_predictor.pkl  # Trained ML model

---

## 🤖 ML Model

**Algorithm:** Random Forest Classifier (100 trees)

**Features:** AQI, Temperature, Green Cover %, Population Density

**Logic:** Area needs trees if → High AQI (>120) + Low green cover (<25%) + High temp (>32°C)

**Accuracy:** 99.5% on test data

**Note:** Currently trained on simulated data for demo. Production needs real ground-truth data.

---

## 📊 Impact Metrics (Projected)

| Metric | 2022 | 2026 | Change |
|--------|------|------|--------|
| Green Cover | 28% | 35% | +7% |
| Parks | 135 | 165 | +30 |
| Avg AQI | 135 | 98 | -37 |
| Temperature | 34.2°C | 32.7°C | -1.5°C |

---

## 🔮 What's Next

- [ ] Real-time AQI integration (CPCB/IQAir API)
- [ ] More cities (Bangalore, Mumbai)
- [ ] Satellite imagery for green cover (Google Earth Engine)
- [ ] Mobile app
- [ ] Ward-level granular analysis

---

## 🐛 Known Limitations

- AQI & green cover data is simulated (demo purposes)
- Only 4 EV stations in OpenStreetMap for Chennai
- No caching — fresh data fetch on each load
- ML model needs real training data for production

---

## 👨‍💻 About Me

**Barishav M** — Building tech for sustainability

Currently applying for MSc Sustainability Management programs in Germany.

**Other Projects:**
- [EcoScore Carbon Calculator](https://eco-score-carbon-calculator.vercel.app/)
- [ESG Ranking Tracker](https://esg-ranking-v2.vercel.app/)

**GitHub:** [@barishavm29-ui](https://github.com/barishavm29-ui)

---

## 📄 License

MIT License — Use it, modify it, just give credit.

---

## 🙏 Credits

- [OpenStreetMap](https://www.openstreetmap.org/) for map data
- [Folium](https://python-visualization.github.io/folium/) & [Leaflet](https://leafletjs.com/) for mapping
- [scikit-learn](https://scikit-learn.org/) for ML
- [Plotly](https://plotly.com/) for charts

---

**Built with 💚 for a greener Chennai**
