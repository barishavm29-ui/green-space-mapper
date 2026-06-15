# app.py - COMPLETE FIXED VERSION

from pathlib import Path

from flask import Flask, render_template, jsonify, request
import sqlite3
import pandas as pd
import random

# Import utilities
from utils.ml_predictor import predict_tree_need
from utils.analyzer import get_city_stats, get_aqi_category

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'data' / 'green_spaces.db'

# Config
app.config['CITY_NAME'] = 'Chennai'
app.config['YEAR_RANGE'] = (2020, 2026)
app.config['DATA_SOURCE'] = 'OpenStreetMap'

def get_db():
    """Database connection helper"""
    if not DB_PATH.exists():
        raise FileNotFoundError("Database not available")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ========== PAGE ROUTES ==========

@app.route('/')
def index():
    """Homepage with map"""
    try:
        stats = get_city_stats()
        return render_template('index.html', stats=stats, city=app.config['CITY_NAME'])
    except Exception as e:
        print(f"Error loading homepage: {e}")
        return render_template('index.html', stats={
            'total_parks': 0,
            'total_ev_stations': 0,
            'avg_aqi': 0,
            'green_cover_percent': 0
        }, city=app.config['CITY_NAME'])


@app.route('/compare')
def compare():
    """Before/After comparison"""
    return render_template('compare.html', city=app.config['CITY_NAME'])


@app.route('/analytics')
def analytics():
    """Analytics dashboard"""
    try:
        stats = get_city_stats()
        return render_template('analytics.html', stats=stats, city=app.config['CITY_NAME'])
    except Exception as e:
        print(f"Error loading analytics: {e}")
        return render_template('analytics.html', stats={
            'total_parks': 0,
            'total_ev_stations': 0,
            'avg_aqi': 0,
            'green_cover_percent': 0
        }, city=app.config['CITY_NAME'])


@app.route('/suggest')
def suggest():
    """Community suggestion form"""
    return render_template('suggest.html', city=app.config['CITY_NAME'])


# ========== API ROUTES ==========

@app.route('/api/map-data')
def map_data():
    """Get all map data (parks, EV stations, pollution)"""
    try:
        if not DB_PATH.exists():
            return jsonify({
                'success': True,
                'parks': [],
                'ev_stations': [],
                'pollution': [],
                'stats': get_city_stats()
            })

        conn = get_db()
        
        parks = pd.read_sql("SELECT * FROM parks LIMIT 100", conn).to_dict('records')
        ev_stations = pd.read_sql("SELECT * FROM ev_stations LIMIT 100", conn).to_dict('records')
        pollution = pd.read_sql("SELECT * FROM air_quality", conn).to_dict('records')
        
        conn.close()
        
        stats = get_city_stats()
        
        return jsonify({
            'success': True,
            'parks': parks,
            'ev_stations': ev_stations,
            'pollution': pollution,
            'stats': stats
        })
    except Exception as e:
        print(f"Error fetching map data: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/area-details')
def area_details():
    """Get details for a specific area (for ML prediction)"""
    try:
        lat = float(request.args.get('lat', 13.0827))
        lon = float(request.args.get('lon', 80.2707))
        
        # Simulate realistic data based on location
        # In production, fetch from actual APIs/database
        aqi = random.randint(80, 160)
        temperature = random.randint(28, 38)
        green_cover = random.randint(10, 50)
        population = random.randint(8000, 22000)
        
        # Get ML prediction
        prediction = predict_tree_need(aqi, temperature, green_cover, population)
        
        return jsonify({
            'success': True,
            'latitude': round(lat, 4),
            'longitude': round(lon, 4),
            'aqi': aqi,
            'aqi_category': get_aqi_category(aqi),
            'temperature': temperature,
            'green_cover': green_cover,
            'population_density': population,
            'prediction': prediction
        })
    except Exception as e:
        print(f"Error analyzing area: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/suggest-location', methods=['POST'])
def suggest_location():
    """Submit community suggestion"""
    try:
        data = request.get_json(silent=True) or {}
        
        # Validate required fields
        required = ['name', 'latitude', 'longitude', 'type']
        for field in required:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400

        if not DB_PATH.exists():
            return jsonify({
                'success': False,
                'error': 'Database not available in this deployment environment.'
            }), 503
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO suggestions (name, latitude, longitude, type, description, user_email)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data['name'],
            float(data['latitude']),
            float(data['longitude']),
            data['type'],
            data.get('description', ''),
            data.get('email', '')
        ))
        
        conn.commit()
        suggestion_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Suggestion submitted successfully!',
            'id': suggestion_id
        })
    except Exception as e:
        print(f"Error submitting suggestion: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/suggestions')
def get_suggestions():
    """Get recent community suggestions"""
    try:
        if not DB_PATH.exists():
            return jsonify({'success': True, 'suggestions': []})

        conn = get_db()
        suggestions = pd.read_sql(
            "SELECT * FROM suggestions ORDER BY created_at DESC LIMIT 20",
            conn
        ).to_dict('records')
        conn.close()
        
        return jsonify({'success': True, 'suggestions': suggestions})
    except Exception as e:
        print(f"Error fetching suggestions: {e}")
        return jsonify({'success': False, 'suggestions': []})


@app.route('/api/district-comparison')
def district_comparison():
    """Get district-wise comparison data"""
    data = {
        'districts': ['Central', 'North', 'South', 'East', 'West', 'Suburban'],
        'green_cover_2022': [22, 28, 35, 25, 30, 40],
        'green_cover_2026': [28, 35, 42, 32, 38, 48],
        'parks_2022': [18, 22, 28, 20, 24, 32],
        'parks_2026': [25, 30, 35, 28, 32, 40]
    }
    return jsonify(data)


@app.route('/api/yearly-trend')
def yearly_trend():
    """Get green cover trend over years"""
    data = {
        'years': list(range(2020, 2027)),
        'green_cover': [22, 24, 28, 30, 32, 33.5, 35],
        'parks': [120, 125, 135, 142, 150, 158, 165],
        'aqi': [145, 140, 135, 128, 120, 110, 98]
    }
    return jsonify(data)


# ========== ERROR HANDLERS ==========

@app.errorhandler(404)
def not_found(e):
    """Custom 404 page"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    """Custom 500 page"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Check if database exists
    if not DB_PATH.exists():
        print("⚠️ Database not found! Run: python utils/data_fetcher.py")
    
    app.run(debug=True, port=5000)
