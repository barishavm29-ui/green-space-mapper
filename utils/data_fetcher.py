# utils/data_fetcher.py

import requests
import pandas as pd
import sqlite3
import time
import os

def fetch_parks(city="Chennai"):
    print(f"🌳 Fetching parks in {city}...")
    
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    query = f"""
    [out:json][timeout:60];
    area["name"="{city}"]["admin_level"="5"]->.searchArea;
    (
      node["leisure"="park"](area.searchArea);
      way["leisure"="park"](area.searchArea);
      relation["leisure"="park"](area.searchArea);
    );
    out center;
    """
    
    try:
        response = requests.post(overpass_url, data={'data': query}, timeout=90)
        data = response.json()
        
        parks = []
        for element in data['elements']:
            if 'lat' in element and 'lon' in element:
                lat, lon = element['lat'], element['lon']
            elif 'center' in element:
                lat, lon = element['center']['lat'], element['center']['lon']
            else:
                continue
            
            name = element.get('tags', {}).get('name', 'Unnamed Park')
            parks.append({'name': name, 'latitude': lat, 'longitude': lon, 'type': 'park'})
        
        df = pd.DataFrame(parks)
        print(f"✅ Found {len(df)} parks!")
        return df
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return pd.DataFrame()


def fetch_ev_stations(city="Chennai"):
    print(f"🔌 Fetching EV stations in {city}...")
    
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    query = f"""
    [out:json][timeout:60];
    area["name"="{city}"]["admin_level"="5"]->.searchArea;
    (
      node["amenity"="charging_station"](area.searchArea);
      way["amenity"="charging_station"](area.searchArea);
    );
    out center;
    """
    
    try:
        response = requests.post(overpass_url, data={'data': query}, timeout=90)
        data = response.json()
        
        stations = []
        for element in data['elements']:
            if 'lat' in element and 'lon' in element:
                lat, lon = element['lat'], element['lon']
            elif 'center' in element:
                lat, lon = element['center']['lat'], element['center']['lon']
            else:
                continue
            
            name = element.get('tags', {}).get('name', 'EV Charging Station')
            stations.append({'name': name, 'latitude': lat, 'longitude': lon, 'type': 'ev_station'})
        
        df = pd.DataFrame(stations)
        print(f"✅ Found {len(df)} EV stations!")
        return df
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return pd.DataFrame()


def create_database():
    print("📊 Creating database...")
    os.makedirs('data', exist_ok=True)
    
    conn = sqlite3.connect('data/green_spaces.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS parks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, latitude REAL NOT NULL, longitude REAL NOT NULL, type TEXT DEFAULT 'park')''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS ev_stations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, latitude REAL NOT NULL, longitude REAL NOT NULL, type TEXT DEFAULT 'ev_station')''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS air_quality (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        latitude REAL NOT NULL, longitude REAL NOT NULL, aqi INTEGER NOT NULL, location TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS suggestions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, latitude REAL NOT NULL, longitude REAL NOT NULL,
        type TEXT NOT NULL, description TEXT, user_email TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()
    print("✅ Database created!")


def save_to_db(df, table_name):
    if df.empty:
        print(f"⚠️ No data to save for {table_name}")
        return
    conn = sqlite3.connect('data/green_spaces.db')
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    print(f"✅ Saved {len(df)} records to {table_name}")


def add_dummy_pollution_data():
    print("🏭 Adding pollution data...")
    pollution_data = [
        {'latitude': 13.0827, 'longitude': 80.2707, 'aqi': 120, 'location': 'Central Chennai'},
        {'latitude': 13.0569, 'longitude': 80.2425, 'aqi': 95, 'location': 'Adyar'},
        {'latitude': 13.0475, 'longitude': 80.2809, 'aqi': 150, 'location': 'Velachery'},
        {'latitude': 13.1067, 'longitude': 80.0982, 'aqi': 85, 'location': 'Porur'},
        {'latitude': 13.0524, 'longitude': 80.2506, 'aqi': 110, 'location': 'Guindy'},
        {'latitude': 13.0878, 'longitude': 80.2785, 'aqi': 130, 'location': 'T Nagar'},
        {'latitude': 12.9916, 'longitude': 80.2336, 'aqi': 100, 'location': 'Pallavaram'},
        {'latitude': 13.0358, 'longitude': 80.2572, 'aqi': 105, 'location': 'Saidapet'},
        {'latitude': 13.1143, 'longitude': 80.2849, 'aqi': 140, 'location': 'Anna Nagar'},
        {'latitude': 13.0674, 'longitude': 80.2376, 'aqi': 90, 'location': 'Nungambakkam'},
    ]
    df = pd.DataFrame(pollution_data)
    save_to_db(df, 'air_quality')


if __name__ == "__main__":
    print("=" * 60)
    print("GREEN SPACES MAPPER - DATA COLLECTION")
    print("=" * 60)
    
    create_database()
    parks_df = fetch_parks("Chennai")
    save_to_db(parks_df, 'parks')
    
    print("\n⏳ Waiting 5 seconds...")
    time.sleep(5)
    
    ev_df = fetch_ev_stations("Chennai")
    save_to_db(ev_df, 'ev_stations')
    add_dummy_pollution_data()
    
    print("\n" + "=" * 60)
    print("✅ DATA COLLECTION COMPLETE!")
    print("=" * 60)