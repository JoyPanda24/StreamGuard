import os
from pathlib import Path

# Detect environment
IS_PRODUCTION = "RENDER" in os.environ

# Cross-platform data directory
if IS_PRODUCTION:
    # Render cloud deployment
    BASE_STORAGE = "/tmp"
else:
    # Local development - use user's home directory
    if os.name == 'nt':  # Windows
        BASE_STORAGE = os.path.join(os.path.expanduser("~"), "StreamGuardDB")
    else:  # Linux/Mac/Unix
        BASE_STORAGE = os.path.join(os.path.expanduser("~"), ".streamguard")

# Ensure directory exists
Path(BASE_STORAGE).mkdir(parents=True, exist_ok=True)

DB_PATH     = os.path.join(BASE_STORAGE, "streamguard.db")
MODEL_PATH  = os.path.join(BASE_STORAGE, "isolation_forest.pkl")
SCALER_PATH = os.path.join(BASE_STORAGE, "scaler.pkl")

# Debug print so we can see in Render logs
print(f"Storage path: {BASE_STORAGE}")
print(f"DB: {DB_PATH}")
print(f"Model: {MODEL_PATH}")
