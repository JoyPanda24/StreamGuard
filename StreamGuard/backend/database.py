import sqlite3
import os
import time
import json
from config import DB_PATH

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     TEXT NOT NULL,
            ip          TEXT NOT NULL,
            country     TEXT,
            city        TEXT,
            lat         REAL,
            lon         REAL,
            isp         TEXT,
            proxy       INTEGER DEFAULT 0,
            hosting     INTEGER DEFAULT 0,
            device      TEXT,
            timestamp   REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS threat_logs (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      TEXT NOT NULL,
            overall_risk TEXT NOT NULL,
            flags_json   TEXT NOT NULL,
            timestamp    REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def save_session(session_data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sessions
            (user_id, ip, country, city, lat, lon, isp, proxy, hosting, device, timestamp)
        VALUES
            (:user_id, :ip, :country, :city, :lat, :lon, :isp, :proxy, :hosting, :device, :timestamp)
    """, session_data)
    conn.commit()
    conn.close()

def get_sessions(user_id, window_seconds=300):
    conn = get_connection()
    cursor = conn.cursor()
    cutoff = time.time() - window_seconds
    cursor.execute("""
        SELECT * FROM sessions
        WHERE user_id = ? AND timestamp >= ?
        ORDER BY timestamp ASC
    """, (user_id, cutoff))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def save_threat_log(user_id, overall_risk, flags):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO threat_logs (user_id, overall_risk, flags_json, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user_id, overall_risk, json.dumps(flags), time.time()))
    conn.commit()
    conn.close()

def get_threat_history(user_id, limit=20):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM threat_logs
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    history = []
    for row in rows:
        entry = dict(row)
        entry["flags"] = json.loads(entry["flags_json"])
        history.append(entry)
    return history

def get_all_flagged_users(risk_level=None):
    conn = get_connection()
    cursor = conn.cursor()
    if risk_level:
        cursor.execute("""
            SELECT DISTINCT user_id, overall_risk, timestamp
            FROM threat_logs
            WHERE overall_risk = ?
            ORDER BY timestamp DESC
        """, (risk_level,))
    else:
        cursor.execute("""
            SELECT DISTINCT user_id, overall_risk, timestamp
            FROM threat_logs
            ORDER BY timestamp DESC
        """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]