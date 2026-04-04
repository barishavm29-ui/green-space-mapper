# utils/map_generator.py

import folium
from folium.plugins import HeatMap, MarkerCluster, Fullscreen
import pandas as pd
import sqlite3
import os

def create_base_map(city="Chennai"):
    city_coords = {'Chennai': [13.0827, 80.2707], 'Bangalore': [12.9716, 77.5946]}
    m = folium.Map(location=city_coords.get(city, [13.0827, 80.2707]), zoom_start=12, tiles='OpenStreetMap')
    folium.TileLayer('CartoDB positron', name='Light Map').add_to(m)
    folium.TileLayer('CartoDB dark_matter', name='Dark Map').add_to(m)
    return m


def add_parks_layer(map_obj):
    if not os.path.exists('data/green_spaces.db'):
        return map_obj
    
    conn = sqlite3.connect('data/green_spaces.db')
    parks = pd.read_sql("SELECT * FROM parks", conn)
    conn.close()
    
    if parks.empty:
        return map_obj
    
    marker_cluster = MarkerCluster(name='Parks 🌳').add_to(map_obj)
    
    for idx, park in parks.iterrows():
        folium.Marker(
            location=[park['latitude'], park['longitude']],
            popup=f"<b>🌳 {park['name']}</b><br>Type: Park<br>Lat: {park['latitude']:.4f}<br>Lon: {park['longitude']:.4f}",
            icon=folium.Icon(color='green', icon='tree', prefix='fa'),
            tooltip=park['name']
        ).add_to(marker_cluster)
    
    return map_obj


def add_ev_stations(map_obj):
    conn = sqlite3.connect('data/green_spaces.db')
    ev_stations = pd.read_sql("SELECT * FROM ev_stations", conn)
    conn.close()
    
    if ev_stations.empty:
        return map_obj
    
    ev_cluster = MarkerCluster(name='EV Stations 🔌').add_to(map_obj)
    
    for idx, station in ev_stations.iterrows():
        folium.Marker(
            location=[station['latitude'], station['longitude']],
            popup=f"<b>🔌 {station['name']}</b><br>Type: EV Charging",
            icon=folium.Icon(color='blue', icon='bolt', prefix='fa'),
            tooltip=station['name']
        ).add_to(ev_cluster)
    
    return map_obj


def add_pollution_heatmap(map_obj):
    conn = sqlite3.connect('data/green_spaces.db')
    pollution = pd.read_sql("SELECT * FROM air_quality", conn)
    conn.close()
    
    if pollution.empty:
        return map_obj
    
    heat_data = [[row['latitude'], row['longitude'], row['aqi'] / 200] for idx, row in pollution.iterrows()]
    
    HeatMap(heat_data, name='Pollution Heatmap 🏭', min_opacity=0.3, max_opacity=0.8,
            radius=25, blur=30, gradient={0.0: 'green', 0.5: 'yellow', 0.7: 'orange', 1.0: 'red'}).add_to(map_obj)
    
    return map_obj


def generate_full_map(city="Chennai"):
    print(f"🗺️ Generating map for {city}...")
    
    m = create_base_map(city)
    m = add_parks_layer(m)
    m = add_ev_stations(m)
    m = add_pollution_heatmap(m)
    
    folium.LayerControl(collapsed=False).add_to(m)
    Fullscreen().add_to(m)
    
    os.makedirs('templates', exist_ok=True)
    m.save('templates/generated_map.html')
    print("✅ Map saved!")
    return m


if __name__ == "__main__":
    generate_full_map("Chennai")