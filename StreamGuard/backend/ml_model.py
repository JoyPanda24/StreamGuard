import numpy as np
import json
import os
import time
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pickle
from config import MODEL_PATH, SCALER_PATH

# Where we save the trained model so it persists across restarts
MODEL_PATH = r"C:\Users\joypa\StreamGuardDB\isolation_forest.pkl"
SCALER_PATH = r"C:\Users\joypa\StreamGuardDB\scaler.pkl"

# ── Feature extraction ────────────────────────────────────────────────────────

def extract_features(sessions):
    """
    Convert raw session data into numbers the ML model can understand.
    Each session becomes a row of numbers (a feature vector).
    
    Features we extract:
    1. hour_of_day       — what time is the user watching? (0-23)
    2. unique_ips        — how many different IPs in last hour?
    3. unique_countries  — how many different countries?
    4. proxy_count       — how many sessions from VPN/proxy?
    5. hosting_count     — how many sessions from datacenters?
    6. session_count     — total number of sessions in window
    7. speed_kmh         — max travel speed detected (0 if none)
    8. unique_devices    — how many different devices?
    """
    if not sessions:
        return None

    now = time.time()

    # Time-based features
    latest = max(s["timestamp"] for s in sessions)
    hour_of_day = (latest % 86400) / 3600  # convert to 0-23

    # IP/location features
    unique_ips       = len(set(s["ip"]      for s in sessions))
    unique_countries = len(set(s["country"] for s in sessions))
    unique_devices   = len(set(s["device"]  for s in sessions))

    # Suspicious IP features
    proxy_count   = sum(1 for s in sessions if s.get("proxy")   in [1, True])
    hosting_count = sum(1 for s in sessions if s.get("hosting") in [1, True])

    session_count = len(sessions)

    # Calculate max travel speed between consecutive sessions
    max_speed = 0
    sorted_sessions = sorted(sessions, key=lambda x: x["timestamp"])
    for i in range(1, len(sorted_sessions)):
        prev = sorted_sessions[i-1]
        curr = sorted_sessions[i]
        if prev.get("lat") and curr.get("lat"):
            from session_tracker import haversine_distance
            dist = haversine_distance(
                prev["lat"], prev["lon"],
                curr["lat"], curr["lon"]
            )
            time_diff_h = (curr["timestamp"] - prev["timestamp"]) / 3600
            if time_diff_h > 0:
                speed = dist / time_diff_h
                max_speed = max(max_speed, speed)

    return [
        hour_of_day,
        unique_ips,
        unique_countries,
        proxy_count,
        hosting_count,
        session_count,
        min(max_speed, 20000),  # cap at 20000 to avoid outlier distortion
        unique_devices
    ]

# ── Training data generation ──────────────────────────────────────────────────

def generate_normal_training_data(n_samples=500):
    """
    Generate synthetic 'normal' user behavior for training.
    In a real company you'd use real historical data.
    Normal users:
    - Watch at regular hours
    - Use 1-2 IPs max
    - Stay in one country
    - Use known devices
    - Never use proxies or datacenters
    """
    np.random.seed(42)
    data = []

    for _ in range(n_samples):
        hour         = np.random.choice(range(7, 24))  # watch between 7am-midnight
        unique_ips   = np.random.choice([1, 1, 1, 2])  # mostly 1 IP
        unique_ctrs  = 1                                # always same country
        proxy        = 0                                # never proxy
        hosting      = np.random.choice([0, 0, 0, 1])  # rarely datacenter
        sessions     = np.random.randint(1, 5)          # 1-4 sessions
        speed        = np.random.uniform(0, 50)         # low travel speed (same city)
        devices      = np.random.choice([1, 1, 2])      # 1-2 devices

        data.append([hour, unique_ips, unique_ctrs,
                     proxy, hosting, sessions, speed, devices])

    return np.array(data)


def generate_attack_training_data(n_samples=100):
    """
    Generate synthetic 'attack' behavior for reference.
    (Isolation Forest is unsupervised so this is just for understanding)
    Attackers:
    - Stream from many IPs simultaneously
    - Appear in multiple countries impossibly fast
    - Use proxies/VPNs
    - Use unknown devices
    """
    np.random.seed(99)
    data = []

    for _ in range(n_samples):
        hour         = np.random.randint(0, 24)
        unique_ips   = np.random.randint(3, 10)    # many IPs
        unique_ctrs  = np.random.randint(2, 6)     # multiple countries
        proxy        = np.random.randint(1, 4)     # using proxies
        hosting      = np.random.randint(1, 4)     # datacenter IPs
        sessions     = np.random.randint(5, 20)    # many sessions
        speed        = np.random.uniform(2000, 15000)  # impossible speeds
        devices      = np.random.randint(3, 8)     # many devices

        data.append([hour, unique_ips, unique_ctrs,
                     proxy, hosting, sessions, speed, devices])

    return np.array(data)

# ── Model training ────────────────────────────────────────────────────────────

def train_model():
    """
    Train the Isolation Forest model on normal behavior data.
    Isolation Forest works by isolating anomalies — 
    normal points need many splits to isolate, 
    anomalies need very few splits (they're already isolated).
    """
    print("Training ML anomaly detection model...")

    # Generate training data
    normal_data = generate_normal_training_data(500)

    # Scale the features (important for ML models)
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(normal_data)

    # Train Isolation Forest
    # contamination=0.05 means we expect ~5% of real data to be anomalous
    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )
    model.fit(scaled_data)

    # Save model and scaler to disk
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(SCALER_PATH, "wb") as f:
        pickle.dump(scaler, f)

    print("Model trained and saved successfully!")
    return model, scaler


def load_model():
    """Load existing model from disk, or train a new one."""
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        with open(SCALER_PATH, "rb") as f:
            scaler = pickle.load(f)
        print("ML model loaded from disk.")
        return model, scaler
    else:
        return train_model()

# ── Prediction ────────────────────────────────────────────────────────────────

def predict_anomaly(sessions):
    """
    Given a list of sessions, predict if the behavior is anomalous.
    Returns a dict with:
    - is_anomaly: True/False
    - anomaly_score: float (more negative = more anomalous)
    - confidence: percentage confidence it's an attack
    - features: the extracted feature values
    """
    features = extract_features(sessions)
    if features is None:
        return {
            "is_anomaly": False,
            "anomaly_score": 0,
            "confidence": 0,
            "reason": "Not enough session data",
            "features": {}
        }

    model, scaler = load_model()

    # Scale and predict
    feature_array = np.array(features).reshape(1, -1)
    scaled = scaler.transform(feature_array)

    # Isolation Forest returns: 1 = normal, -1 = anomaly
    prediction = model.predict(scaled)[0]
    
    # Score: more negative = more anomalous (range roughly -0.5 to 0.5)
    score = model.decision_function(scaled)[0]

    is_anomaly = prediction == -1

    # Convert score to a 0-100 confidence percentage
    # Score of -0.5 or below = 100% confidence anomaly
    confidence = min(100, max(0, int((-score + 0.1) * 200)))

    feature_labels = {
        "hour_of_day":       round(features[0], 1),
        "unique_ips":        int(features[1]),
        "unique_countries":  int(features[2]),
        "proxy_count":       int(features[3]),
        "hosting_count":     int(features[4]),
        "session_count":     int(features[5]),
        "max_speed_kmh":     round(features[6], 1),
        "unique_devices":    int(features[7])
    }

    return {
        "is_anomaly":    is_anomaly,
        "anomaly_score": round(float(score), 4),
        "confidence":    confidence,
        "severity":      "CRITICAL" if confidence > 70 else "HIGH" if confidence > 40 else "MEDIUM",
        "reason":        f"ML model flagged abnormal behavior pattern (confidence: {confidence}%)",
        "features":      feature_labels
    }