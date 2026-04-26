from session_tracker import get_recent_sessions, haversine_distance
from geo_locator import check_ip_reputation
from ml_model import predict_anomaly
import time

def check_simultaneous_streams(user_id, max_allowed=2):
    recent = get_recent_sessions(user_id, window_seconds=60)
    unique_ips = set(s["ip"] for s in recent)
    if len(unique_ips) > max_allowed:
        return {
            "flag": True,
            "reason": f"Simultaneous streams from {len(unique_ips)} different IPs",
            "severity": "HIGH",
            "ips": list(unique_ips)
        }
    return {"flag": False}


def check_impossible_travel(user_id):
    sessions = get_recent_sessions(user_id, window_seconds=3600)
    if len(sessions) < 2:
        return {"flag": False}
    sessions = sorted(sessions, key=lambda x: x["timestamp"])
    for i in range(1, len(sessions)):
        prev = sessions[i-1]
        curr = sessions[i]
        if not prev.get("lat") or not curr.get("lat"):
            continue
        if prev["lat"] == curr["lat"] and prev["lon"] == curr["lon"]:
            continue
        distance_km = haversine_distance(
            prev["lat"], prev["lon"],
            curr["lat"], curr["lon"]
        )
        time_diff_hours = (curr["timestamp"] - prev["timestamp"]) / 3600
        if time_diff_hours > 0:
            required_speed = distance_km / time_diff_hours
            if required_speed > 900:
                return {
                    "flag": True,
                    "reason": (
                        f"Impossible travel: {prev['city']}, {prev['country']} → "
                        f"{curr['city']}, {curr['country']} "
                        f"({distance_km:.0f}km in {time_diff_hours*60:.0f} mins)"
                    ),
                    "severity": "CRITICAL",
                    "from": f"{prev['city']}, {prev['country']}",
                    "to":   f"{curr['city']}, {curr['country']}",
                    "distance_km":       round(distance_km),
                    "time_minutes":      round(time_diff_hours * 60),
                    "required_speed_kmh": round(required_speed)
                }
    return {"flag": False}


def check_device_anomaly(user_id, known_devices=None):
    if known_devices is None:
        known_devices = ["mobile_android", "web_chrome"]
    recent = get_recent_sessions(user_id, window_seconds=300)
    unknown = [s for s in recent if s["device"] not in known_devices]
    if unknown:
        return {
            "flag": True,
            "reason": f"Stream from unrecognized device: {unknown[0]['device']}",
            "severity": "MEDIUM",
            "device": unknown[0]["device"]
        }
    return {"flag": False}


def check_proxy_vpn(user_id):
    recent = get_recent_sessions(user_id, window_seconds=300)
    for session in recent:
        ip_flags, _ = check_ip_reputation(session["ip"])
        if ip_flags:
            return ip_flags[0]
    return {"flag": False}


def check_ml_anomaly(user_id):
    """
    NEW: Run the Isolation Forest ML model on the user's sessions.
    This catches patterns that rule-based checks might miss.
    """
    sessions = get_recent_sessions(user_id, window_seconds=3600)
    if not sessions:
        return {"flag": False}

    result = predict_anomaly(sessions)

    if result["is_anomaly"]:
        return {
            "flag":       True,
            "reason":     result["reason"],
            "severity":   result["severity"],
            "confidence": result["confidence"],
            "score":      result["anomaly_score"],
            "features":   result["features"]
        }
    return {"flag": False}


def run_full_analysis(user_id):
    results = {
        "user_id":      user_id,
        "timestamp":    time.time(),
        "flags":        [],
        "overall_risk": "LOW"
    }

    checks = [
        check_simultaneous_streams(user_id),
        check_impossible_travel(user_id),
        check_device_anomaly(user_id),
        check_proxy_vpn(user_id),
        check_ml_anomaly(user_id),   # ML check added here
    ]

    for check in checks:
        if isinstance(check, list):
            for c in check:
                if c.get("flag"):
                    results["flags"].append(c)
        elif check.get("flag"):
            results["flags"].append(check)

    severities = [f["severity"] for f in results["flags"]]
    if "CRITICAL" in severities:
        results["overall_risk"] = "CRITICAL"
    elif "HIGH" in severities:
        results["overall_risk"] = "HIGH"
    elif "MEDIUM" in severities:
        results["overall_risk"] = "MEDIUM"

    return results