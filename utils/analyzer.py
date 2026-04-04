# utils/analyzer.py

import sqlite3
import pandas as pd

def get_city_stats():
    conn = sqlite3.connect('data/green_spaces.db')
    
    parks = pd.read_sql("SELECT COUNT(*) as count FROM parks", conn)
    ev_stations = pd.read_sql("SELECT COUNT(*) as count FROM ev_stations", conn)
    avg_aqi = pd.read_sql("SELECT AVG(aqi) as avg_aqi FROM air_quality", conn)
    
    conn.close()
    
    return {
        'total_parks': int(parks['count'].iloc[0]),
        'total_ev_stations': int(ev_stations['count'].iloc[0]),
        'avg_aqi': round(float(avg_aqi['avg_aqi'].iloc[0]), 1),
        'green_cover_percent': 32,  # Placeholder
        'trees_planted_2024': 2500,
        'co2_reduced': 125
    }


def get_aqi_category(aqi):
    if aqi <= 50: return 'Good'
    elif aqi <= 100: return 'Moderate'
    elif aqi <= 150: return 'Unhealthy for Sensitive'
    elif aqi <= 200: return 'Unhealthy'
    else: return 'Hazardous'