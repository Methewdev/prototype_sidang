from pathlib import Path

ROOT = Path(__file__).resolve().parent

APP_TITLE = "Livin Emotion Analysis"
APP_ICON = "📊"

ASSET_DIR = ROOT / "assets"

CSS_FILE = ASSET_DIR / "style.css"
LOGO = ASSET_DIR / "logo.png"
SLANG_FILE = ASSET_DIR / "new_kamus_alay.csv"

MODEL_NAME = "envidevelopment/livin-emotion-indobert"
USE_LOCAL_MODEL = False

MODEL_PATH = ROOT / "models"
DATA_PATH = ROOT / "data"

MAX_LENGTH = 128
RANDOM_STATE = 42
N_CLUSTER = 3

EMOTION_LABELS = [
    "Frustrasi",
    "Netral",
    "Sedih",
    "Senang"
]
