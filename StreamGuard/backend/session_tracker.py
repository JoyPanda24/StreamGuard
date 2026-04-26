import time
import math
from geo_locator import get_location
from database import save_session, get_sessions

def log_session(user_id, ip_address, device, timestamp=None):
    if timestamp is None:
        timestamp = time.time()

    location = get_location(ip_address)

    session_data = {
        "user_id":   user_id,
        "ip":        ip_address,
        "country":   location["countryCode"],
        "city":      location["city"],
        "lat":       location["lat"],
        "lon":       location["lon"],
        "isp":       location["isp"],
        "proxy":     1 if location["proxy"] else 0,
        "hosting":   1 if location["hosting"] else 0,
        "device":    device,
        "timestamp": timestamp
    }

    # Save to database instead of memory
    save_session(session_data)
    return session_data

def get_recent_sessions(user_id, window_seconds=300):
    # Now reads from database — persists across restarts!
    return get_sessions(user_id, window_seconds)

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon/2)**2)
    return R * 2 * math.asin(math.sqrt(a))