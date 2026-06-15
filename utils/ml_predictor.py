"""Tree-need prediction helpers.

The deployed Vercel environment is read-only, so this module avoids
training or writing model files at import time. Local development can still
train and persist the model when needed.
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "tree_predictor.pkl"

def generate_training_data():
    np.random.seed(42)
    n_samples = 1000
    
    data = pd.DataFrame({
        'aqi': np.random.randint(50, 250, n_samples),
        'temperature': np.random.randint(25, 40, n_samples),
        'green_cover_percent': np.random.randint(5, 60, n_samples),
        'population_density': np.random.randint(5000, 25000, n_samples)
    })
    
    data['needs_trees'] = ((data['aqi'] > 120) & (data['green_cover_percent'] < 25) & (data['temperature'] > 32)).astype(int)
    return data


def train_model():
    print("🤖 Training ML model...")
    
    data = generate_training_data()
    X = data[['aqi', 'temperature', 'green_cover_percent', 'population_density']]
    y = data['needs_trees']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    print(f"✅ Training Accuracy: {model.score(X_train, y_train) * 100:.2f}%")
    print(f"✅ Testing Accuracy: {model.score(X_test, y_test) * 100:.2f}%")
    
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print("💾 Model saved!")
    return model


def _load_model():
    if not MODEL_PATH.exists():
        return None
    try:
        return joblib.load(MODEL_PATH)
    except Exception:
        return None


def _heuristic_prediction(aqi, temperature, green_cover, population_density):
    needs_trees = bool((aqi > 120) and (green_cover < 25) and (temperature > 32))
    confidence = 82.0 if needs_trees else 76.0

    if needs_trees:
        severity = "HIGH" if aqi > 150 else "MODERATE"
        recommendation = f"{severity} priority. Plant {int((100 - green_cover) / 2)} trees/hectare."
    else:
        recommendation = "Sufficient green cover. Focus on maintenance."

    return {
        "needs_trees": needs_trees,
        "confidence": confidence,
        "recommendation": recommendation,
        "fallback": True,
    }


def predict_tree_need(aqi, temperature, green_cover, population_density):
    model = _load_model()
    if model is None:
        return _heuristic_prediction(aqi, temperature, green_cover, population_density)

    features = np.array([[aqi, temperature, green_cover, population_density]])
    
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]
    confidence = probability[1] * 100 if prediction == 1 else probability[0] * 100
    
    if prediction:
        severity = "HIGH" if aqi > 150 else "MODERATE"
        recommendation = f"{severity} priority. Plant {int((100-green_cover)/2)} trees/hectare."
    else:
        recommendation = "Sufficient green cover. Focus on maintenance."
    
    return {'needs_trees': bool(prediction), 'confidence': round(confidence, 2), 'recommendation': recommendation, 'fallback': False}


if __name__ == "__main__":
    train_model()
    result = predict_tree_need(150, 35, 15, 15000)
    print(f"\nTest: {result}")
