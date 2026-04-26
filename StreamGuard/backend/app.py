from flask import Flask, request, jsonify
from flask_cors import CORS
from session_tracker import log_session
from anomaly_detector import run_full_analysis
from geo_locator import get_location
from database import init_db, get_threat_history, get_all_flagged_users, save_threat_log
import time

app = Flask(__name__)
CORS(app)
init_db()

@app.route("/")
def home():
    return jsonify({
        "name": "StreamGuard API",
        "version": "1.0",
        "status": "online",
        "description": "OTT Session Anomaly Detection System",
        "author": "JoyPanda24",
        "endpoints": {
            "geoip":           "/api/geoip/<ip>",
            "analyze":         "/api/analyze/<user_id>",
            "simulate_attack": "/api/simulate/attack",
            "history":         "/api/history/<user_id>",
            "flagged_users":   "/api/flagged-users",
            "ml_analyze":      "/api/ml/analyze/<user_id>",
            "retrain_model":   "/api/ml/train"
        }
    })
CORS(app)

init_db()

@app.route("/api/session/log", methods=["POST"])
def log_new_session():
    data = request.json
    session = log_session(
        user_id=data["user_id"],
        ip_address=data["ip"],
        device=data["device"]
    )
    analysis = run_full_analysis(data["user_id"])
    save_threat_log(data["user_id"], analysis["overall_risk"], analysis["flags"])
    return jsonify({"session_logged": session, "threat_analysis": analysis})

@app.route("/api/analyze/<user_id>", methods=["GET"])
def analyze_user(user_id):
    analysis = run_full_analysis(user_id)
    save_threat_log(user_id, analysis["overall_risk"], analysis["flags"])
    return jsonify(analysis)

@app.route("/api/geoip/<ip_address>", methods=["GET"])
def geoip_lookup(ip_address):
    return jsonify(get_location(ip_address))

@app.route("/api/history/<user_id>", methods=["GET"])
def threat_history(user_id):
    history = get_threat_history(user_id)
    return jsonify({"user_id": user_id, "history": history})

@app.route("/api/flagged-users", methods=["GET"])
def flagged_users():
    risk = request.args.get("risk")
    users = get_all_flagged_users(risk_level=risk)
    return jsonify({"flagged_users": users})

@app.route("/api/simulate/attack", methods=["POST"])
def simulate_attack():
    user_id = request.json.get("user_id", "demo_user")
    now = time.time()
    log_session(user_id, "103.21.244.10", "mobile_android", now - 600)
    log_session(user_id, "52.91.100.200", "web_chrome",     now - 100)
    log_session(user_id, "91.108.4.50",   "unknown_device", now - 50)
    log_session(user_id, "185.220.101.5", "web_firefox",    now)
    analysis = run_full_analysis(user_id)
    save_threat_log(user_id, analysis["overall_risk"], analysis["flags"])
    return jsonify({"message": "Attack simulated", "analysis": analysis})

@app.route("/api/ml/train", methods=["POST"])
def retrain_model():
    from ml_model import train_model
    train_model()
    return jsonify({"message": "Model retrained successfully!"})

@app.route("/api/ml/analyze/<user_id>", methods=["GET"])
def ml_analyze(user_id):
    from session_tracker import get_recent_sessions
    from ml_model import predict_anomaly
    sessions = get_recent_sessions(user_id, window_seconds=3600)
    result = predict_anomaly(sessions)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)