# 🛡️ StreamGuard — OTT Session Anomaly Detection System

> A real-time cybersecurity system that detects piracy and session hijacking 
> on OTT platforms like Netflix, Amazon Prime, and Hotstar.

![Status](https://img.shields.io/badge/Status-Live-brightgreen)
![Python](https://img.shields.io/badge/Python-3.14-blue)
![ML](https://img.shields.io/badge/ML-Isolation%20Forest-orange)
![Deploy](https://img.shields.io/badge/Deployed-Render-purple)

---

## 🌐 Live Demo

| | URL |
|---|---|
| 🎨 **Dashboard** | https://joypanda24.github.io/SteamGuard/ |
| ⚙️ **API** | https://steamguard.onrender.com |
| 🔍 **GeoIP Test** | https://steamguard.onrender.com/api/geoip/8.8.8.8 |

---

## 🎯 The Problem I'm Solving

Sites like **NetMirror** and **CineHD** illegally stream Netflix, 
Amazon Prime, and other OTT content by:
- Stealing user session cookies
- Hijacking authenticated accounts
- Streaming from multiple locations simultaneously

**StreamGuard detects all of this in real time.**

---

## 🧠 How It Works

### Detection Modules

| Module | What It Detects |
|---|---|
| 🌍 **Impossible Travel** | User in India, then USA 8 mins later — physically impossible |
| 📱 **Simultaneous Streams** | Same account streaming from 4 different IPs at once |
| 🔒 **VPN/Proxy Detection** | User hiding real location behind a proxy |
| 💻 **Unknown Device** | Stream from a device never seen before |
| 🤖 **ML Anomaly Detection** | Isolation Forest model flags abnormal behavior patterns |

### Threat Levels
- 🔴 **CRITICAL** — Account almost certainly compromised
- 🟠 **HIGH** — Strong indicators of abuse
- 🟡 **MEDIUM** — Suspicious but needs monitoring
- 🟢 **LOW** — Normal behavior

---

## 🛠️ Tech Stack

- Backend:   Python + Flask REST API
- ML Model:  scikit-learn Isolation Forest
- Database:  SQLite (persistent session storage)
- GeoIP:     ip-api.com (real-time IP geolocation)
- Frontend:  Vanilla HTML/CSS/JS
- Hosting:   Render (API) + GitHub Pages (Dashboard)

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API status and endpoint list |
| GET | `/api/geoip/<ip>` | Geolocate any IP address |
| POST | `/api/simulate/attack` | Simulate a cookie hijacking attack |
| GET | `/api/analyze/<user_id>` | Run full threat analysis on a user |
| GET | `/api/history/<user_id>` | Get threat history from database |
| GET | `/api/flagged-users` | List all flagged accounts |
| GET | `/api/ml/analyze/<user_id>` | Run ML-only anomaly detection |
| POST | `/api/ml/train` | Retrain the ML model |

---

## 🚀 Run Locally

```bash
# Clone the repo
git clone https://github.com/JoyPanda24/SteamGuard.git
cd SteamGuard/StreamGuard

# Install dependencies
pip install -r requirements.txt

# Start the server
cd backend
python app.py

# Open the dashboard
# Open frontend/index.html in your browser
```

---

## 📁 Project Structure

```
StreamGuard/
├── backend/
│   ├── app.py              # Flask API server
│   ├── session_tracker.py  # Session logging
│   ├── anomaly_detector.py # Rule-based detection
│   ├── ml_model.py         # Isolation Forest ML model
│   ├── geo_locator.py      # IP geolocation
│   ├── database.py         # SQLite persistence
│   └── config.py           # Environment config
├── frontend/
│   └── index.html          # Dashboard UI
├── docs/
│   └── index.html          # GitHub Pages deployment
├── Procfile                # Render deployment
└── requirements.txt        # Python dependencies
```

---

## 🔬 ML Model Details

The **Isolation Forest** algorithm detects anomalies by learning 
what normal streaming behavior looks like:

**Features analyzed:**
- Hour of day (normal users watch at regular times)
- Number of unique IPs in last hour
- Number of unique countries
- Proxy/VPN usage count
- Datacenter IP count
- Session frequency
- Maximum travel speed between sessions
- Number of unique devices

Normal behavior takes many splits to isolate.
Anomalies are isolated in very few splits — they stand out.

---

## 💡 Real-World Impact

This system addresses the same attack vectors used by piracy 
sites to steal OTT content:

1. **Cookie theft** → Detected by impossible travel + unknown device
2. **Credential stuffing** → Detected by simultaneous streams
3. **Account sharing abuse** → Detected by multiple IPs/locations
4. **Bot streaming** → Detected by datacenter IP flagging + ML model

---

## 📄 License

MIT License — feel free to use and build on this project.
