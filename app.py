"""
CV AI Analyzer - Application principale
Analyse intelligente de CVs et matching emploi avec IA
"""
import streamlit as st
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="CV AI Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Imports des modules
from ui.candidate_mode import render_candidate_mode
from ui.recruiter_mode import render_recruiter_mode
from ui.components import show_api_key_input
from utils.helpers import load_analysis_history, delete_analysis, format_date, truncate_text
from utils.config import AVAILABLE_MODELS

# CSS personnalisé
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation des états de session
if 'groq_api_key' not in st.session_state:
    st.session_state.groq_api_key = ""

if 'current_mode' not in st.session_state:
    st.session_state.current_mode = "Candidat"

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("# ⚙️ Configuration")
    
    # Clé API
    api_key = show_api_key_input()
    
    st.markdown("---")
    
    # Sélection du modèle
    if api_key:
        st.markdown("### 🤖 Modèle IA")
        selected_model = st.selectbox(
            "Choisir le modèle",
            options=list(AVAILABLE_MODELS.keys())
        )
        
        st.session_state.selected_model = AVAILABLE_MODELS[selected_model]
        st.caption(f"Modèle actif: `{st.session_state.selected_model}`")
    
    st.markdown("---")
    
    # Navigation entre modes
    st.markdown("### 🔄 Mode d'Utilisation")
    mode = st.radio(
        "Choisissez votre profil:",
        ["Candidat", "Recruteur"],
        index=0 if st.session_state.current_mode == "Candidat" else 1,
        help="Candidat: Analyser votre CV | Recruteur: Comparer plusieurs CVs"
    )
    
    st.session_state.current_mode = mode
    
    st.markdown("---")
    
    # Historique
    st.markdown("### 📚 Historique")
    
    history = load_analysis_history()
    
    if history:
        st.caption(f"{len(history)} analyse(s) sauvegardée(s)")
        
        if st.button("🗑️ Effacer tout l'historique", use_container_width=True):
            for item in history:
                delete_analysis(item['id'])
            st.rerun()
        
        st.markdown("---")
        
        # Afficher les 5 dernières analyses
        for item in history[:5]:
            with st.expander(f"📄 {truncate_text(item.get('cv_name', 'Analyse'), 25)}"):
                st.caption(f"📅 {format_date(item.get('timestamp', ''))}")
                st.metric("Score", f"{item.get('score', 0)}/100")
                
                if st.button("❌ Supprimer", key=f"del_{item['id']}"):
                    delete_analysis(item['id'])
                    st.rerun()
    else:
        st.info("Aucune analyse enregistrée")
    
    st.markdown("---")
    
    # À propos
    with st.expander("ℹ️ À propos"):
        st.markdown("""
        **CV AI Analyzer v1.0**
        
        Analyseur intelligent de CVs propulsé par IA.
        
        🚀 **Fonctionnalités:**
        - Analyse de matching CV/Emploi
        - Score de compatibilité
        - Suggestions d'amélioration
        - Génération de lettres
        - Mode recruteur
        
        💻 **Technologies:**
        - Streamlit
        - Groq API (Llama 3.3)
        - Python
        
        📧 **Support:**
        Signalez un bug ou suggérez une amélioration sur GitHub.
        """)

# ==================== MAIN ====================

# En-tête principal
st.markdown('<h1 class="main-title">🤖 CV AI Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Analyse intelligente de CVs et matching emploi propulsée par IA</p>', unsafe_allow_html=True)

# Vérification de la clé API
if not st.session_state.groq_api_key:
    st.warning("⚠️ Veuillez configurer votre clé API Groq dans la barre latérale pour commencer")
    
    # Instructions
    st.markdown("---")
    st.markdown("## 🚀 Démarrage Rapide")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 1️⃣ Obtenir une clé API
        
        1. Allez sur [console.groq.com](https://console.groq.com)
        2. Créez un compte gratuit
        3. Générez une clé API
        4. Copiez-la
        """)
    
    with col2:
        st.markdown("""
        ### 2️⃣ Configurer
        
        1. Collez la clé dans la sidebar
        2. Choisissez votre mode
        3. Sélectionnez le modèle IA
        """)
    
    with col3:
        st.markdown("""
        ### 3️⃣ Analyser
        
        1. Uploadez votre CV (PDF)
        2. Collez l'offre d'emploi
        3. Lancez l'analyse !
        """)
    
    st.markdown("---")
    
    # Démonstration visuelle
    st.markdown("## 📊 Fonctionnalités")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 👤 Mode Candidat
        
        - ✅ Score de matching précis
        - 📊 Analyse détaillée par sections
        - 💡 Suggestions d'amélioration
        - ✍️ Génération de lettre de motivation
        - 📥 Export des résultats
        """)
    
    with col2:
        st.markdown("""
        ### 👔 Mode Recruteur
        
        - 🏆 Classement automatique des candidats
        - 📊 Comparaison multi-CVs
        - 💪 Points forts/réserves par candidat
        - 📄 Rapport d'analyse exportable
        - ⚡ Gain de temps considérable
        """)
    
    st.info("💡 **Astuce:** Ce projet est 100% gratuit et open-source. Parfait pour votre portfolio !")

else:
    # Afficher le mode sélectionné
    st.markdown("---")
    
    # Indicateur du mode actif
    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
    
    with col2:
        if st.session_state.current_mode == "Candidat":
            st.markdown("""
            <div class="metric-card">
                <h3>👤 Mode Candidat</h3>
                <p>Optimisez votre CV</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        if st.session_state.current_mode == "Recruteur":
            st.markdown("""
            <div class="metric-card">
                <h3>👔 Mode Recruteur</h3>
                <p>Comparez les candidats</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Rendu du mode sélectionné
    if st.session_state.current_mode == "Candidat":
        render_candidate_mode()
    else:
        render_recruiter_mode()

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #999; font-size: 0.9rem;">Développé avec ❤️ | '
    'Propulsé par Groq AI & Streamlit | '
    '<a href="https://github.com" target="_blank">⭐ Star sur GitHub</a></p>',
    unsafe_allow_html=True
)