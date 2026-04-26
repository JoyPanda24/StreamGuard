import os

# When deployed online, use /tmp folder
# When running locally, use your StreamGuardDB folder
IS_PRODUCTION = os.environ.get("RENDER", False)

if IS_PRODUCTION:
    BASE_STORAGE = "/tmp"
else:
    BASE_STORAGE = r"C:\Users\joypa\StreamGuardDB"

DB_PATH     = os.path.join(BASE_STORAGE, "streamguard.db")
MODEL_PATH  = os.path.join(BASE_STORAGE, "isolation_forest.pkl")
SCALER_PATH = os.path.join(BASE_STORAGE, "scaler.pkl")