import os

# Render automatically sets the RENDER environment variable
IS_PRODUCTION = "RENDER" in os.environ

if IS_PRODUCTION:
    BASE_STORAGE = "/tmp"
else:
    BASE_STORAGE = r"C:\Users\joypa\StreamGuardDB"

DB_PATH     = os.path.join(BASE_STORAGE, "streamguard.db")
MODEL_PATH  = os.path.join(BASE_STORAGE, "isolation_forest.pkl")
SCALER_PATH = os.path.join(BASE_STORAGE, "scaler.pkl")

# Debug print so we can see in Render logs
print(f"Storage path: {BASE_STORAGE}")
print(f"DB: {DB_PATH}")
print(f"Model: {MODEL_PATH}")
