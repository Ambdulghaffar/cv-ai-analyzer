"""
Fonctions utilitaires
"""
import json
import hashlib
from datetime import datetime
from pathlib import Path
from utils.config import HISTORY_DIR, SCORE_THRESHOLDS, SCORE_COLORS

def get_score_category(score: int) -> str:
    """Retourne la catégorie du score"""
    if score >= SCORE_THRESHOLDS["excellent"]:
        return "excellent"
    elif score >= SCORE_THRESHOLDS["bon"]:
        return "bon"
    elif score >= SCORE_THRESHOLDS["moyen"]:
        return "moyen"
    else:
        return "faible"

def get_score_color(score: int) -> str:
    """Retourne la couleur associée au score"""
    category = get_score_category(score)
    return SCORE_COLORS[category]

def generate_analysis_id() -> str:
    """Génère un ID unique pour l'analyse"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_hash = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
    return f"analysis_{timestamp}_{random_hash}"

def save_analysis_history(analysis_data: dict) -> str:
    """Sauvegarde l'historique d'une analyse"""
    analysis_id = generate_analysis_id()
    analysis_data['id'] = analysis_id
    analysis_data['timestamp'] = datetime.now().isoformat()
    
    filepath = HISTORY_DIR / f"{analysis_id}.json"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, ensure_ascii=False, indent=2)
    
    return analysis_id

def load_analysis_history() -> list:
    """Charge l'historique des analyses"""
    history = []
    
    if not HISTORY_DIR.exists():
        return history
    
    for filepath in sorted(HISTORY_DIR.glob("*.json"), reverse=True):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                history.append(data)
        except Exception as e:
            print(f"Erreur lors du chargement de {filepath}: {e}")
    
    return history

def delete_analysis(analysis_id: str) -> bool:
    """Supprime une analyse de l'historique"""
    filepath = HISTORY_DIR / f"{analysis_id}.json"
    
    try:
        if filepath.exists():
            filepath.unlink()
            return True
    except Exception as e:
        print(f"Erreur lors de la suppression: {e}")
    
    return False

def format_date(iso_date: str) -> str:
    """Formate une date ISO en format lisible"""
    try:
        dt = datetime.fromisoformat(iso_date)
        return dt.strftime("%d/%m/%Y à %H:%M")
    except:
        return iso_date

def truncate_text(text: str, max_length: int = 100) -> str:
    """Tronque un texte avec des points de suspension"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."