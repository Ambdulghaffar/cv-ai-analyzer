"""
Configuration et constantes de l'application
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Chemins
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
HISTORY_DIR = DATA_DIR / "history"
EXPORTS_DIR = DATA_DIR / "exports"

# Créer les dossiers s'ils n'existent pas
for directory in [DATA_DIR, UPLOADS_DIR, HISTORY_DIR, EXPORTS_DIR]:
    directory.mkdir(exist_ok=True, parents=True)

# Configuration API
GROQ_API_KEY = os.getenv("GROQ_API_KEY", None)  # Changé de "" à None
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama-3.3-70b-versatile")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4000"))

# Configuration Application
APP_TITLE = os.getenv("APP_TITLE", "CV AI Analyzer")
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
ALLOWED_FILE_TYPES = ["pdf"]

# Modèles disponibles
AVAILABLE_MODELS = {
    "Llama 3.3 70B (Recommandé)": "llama-3.3-70b-versatile",
    "Llama 3.1 70B": "llama-3.1-70b-versatile",
    "Mixtral 8x7B": "mixtral-8x7b-32768",
}

# Scores de matching
SCORE_THRESHOLDS = {
    "excellent": 80,
    "bon": 60,
    "moyen": 40,
    "faible": 0
}

# Couleurs pour les scores
SCORE_COLORS = {
    "excellent": "#28a745",
    "bon": "#ffc107",
    "moyen": "#fd7e14",
    "faible": "#dc3545"
}