from pathlib import Path

ROOT = Path(__file__).resolve().parent

APP_TITLE = "Livin Emotion Analysis"

APP_ICON = "📊"

MODEL_NAME = "username/livin-emotion-indobert"

LOGO = ROOT / "assets" / "logo.png"

CSS_FILE = ROOT / "assets" / "style.css"

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
