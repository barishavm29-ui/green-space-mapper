from pathlib import Path
import sqlite3

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "green_spaces.db"


def _fallback_stats():
    return {
        'total_parks': 135,
        'total_ev_stations': 4,
        'avg_aqi': 135.0,
        'green_cover_percent': 32,
        'trees_planted_2024': 2500,
        'co2_reduced': 125
    }

def get_city_stats():
    if not DB_PATH.exists():
        return _fallback_stats()

    try:
        conn = sqlite3.connect(DB_PATH)

        parks = pd.read_sql("SELECT COUNT(*) as count FROM parks", conn)
        ev_stations = pd.read_sql("SELECT COUNT(*) as count FROM ev_stations", conn)
        avg_aqi = pd.read_sql("SELECT AVG(aqi) as avg_aqi FROM air_quality", conn)

        conn.close()

        avg_aqi_value = avg_aqi['avg_aqi'].iloc[0]
        return {
            'total_parks': int(parks['count'].iloc[0]),
            'total_ev_stations': int(ev_stations['count'].iloc[0]),
            'avg_aqi': round(float(avg_aqi_value), 1) if pd.notna(avg_aqi_value) else 0.0,
            'green_cover_percent': 32,
            'trees_planted_2024': 2500,
            'co2_reduced': 125
        }
    except Exception:
        return _fallback_stats()


def get_aqi_category(aqi):
    if aqi <= 50: return 'Good'
    elif aqi <= 100: return 'Moderate'
    elif aqi <= 150: return 'Unhealthy for Sensitive'
    elif aqi <= 200: return 'Unhealthy'
    else: return 'Hazardous'
