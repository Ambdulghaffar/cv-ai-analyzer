"""
Composants UI réutilisables
"""
import streamlit as st
import plotly.graph_objects as go
from utils.helpers import get_score_color, get_score_category

def display_score_gauge(score: int, title: str = "Score de Matching"):
    """
    Affiche une jauge de score
    """
    color = get_score_color(score)
    category = get_score_category(score)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 24}},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#ffebee'},
                {'range': [40, 60], 'color': '#fff3e0'},
                {'range': [60, 80], 'color': '#fff9c4'},
                {'range': [80, 100], 'color': '#e8f5e9'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Message selon le score
    messages = {
        "excellent": "🎉 Excellent matching ! Le profil correspond parfaitement.",
        "bon": "✅ Bon matching. Quelques ajustements mineurs possibles.",
        "moyen": "⚠️ Matching moyen. Des améliorations sont recommandées.",
        "faible": "❌ Matching faible. CV à retravailler significativement."
    }
    
    st.info(messages[category])

def display_skills_comparison(present_skills: list, missing_skills: list):
    """
    Affiche la comparaison des compétences
    """
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Compétences Présentes")
        if present_skills:
            for skill in present_skills:
                st.markdown(f"- ✓ {skill}")
        else:
            st.info("Aucune compétence identifiée")
    
    with col2:
        st.markdown("### ❌ Compétences Manquantes")
        if missing_skills:
            for skill in missing_skills:
                st.markdown(f"- ✗ {skill}")
        else:
            st.success("Toutes les compétences sont présentes !")

def display_analysis_card(title: str, content: str, icon: str = "📊"):
    """
    Carte d'affichage d'analyse
    """
    st.markdown(f"""
    <div style="
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 10px 0;
    ">
        <h3 style="margin: 0 0 10px 0;">{icon} {title}</h3>
        <p style="margin: 0; color: #333;">{content}</p>
    </div>
    """, unsafe_allow_html=True)

def display_section_scores(analysis: dict):
    """
    Affiche les scores par section sous forme de barres
    """
    sections = {
        "Compétences Techniques": analysis.get('competences_techniques', {}).get('score', 0),
        "Expérience": analysis.get('experience', {}).get('score', 0),
        "Formation": analysis.get('formation', {}).get('score', 0)
    }
    
    fig = go.Figure()
    
    for section, score in sections.items():
        color = get_score_color(score)
        fig.add_trace(go.Bar(
            y=[section],
            x=[score],
            orientation='h',
            marker=dict(color=color),
            text=f"{score}%",
            textposition='outside',
            name=section
        ))
    
    fig.update_layout(
        title="Scores par Section",
        xaxis_title="Score (%)",
        showlegend=False,
        height=250,
        margin=dict(l=150, r=20, t=60, b=20),
        xaxis=dict(range=[0, 100])
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_points_list(points: list, title: str, icon: str, color: str):
    """
    Affiche une liste de points (forts ou amélioration)
    """
    st.markdown(f"### {icon} {title}")
    
    for i, point in enumerate(points, 1):
        st.markdown(f"""
        <div style="
            background-color: {color};
            padding: 10px 15px;
            border-radius: 5px;
            margin: 8px 0;
        ">
            <strong>{i}.</strong> {point}
        </div>
        """, unsafe_allow_html=True)

def show_api_key_input():
    """
    Affiche l'input pour la clé API dans la sidebar
    """
    with st.sidebar:
        st.markdown("### 🔑 Configuration API")
        
        api_key = st.text_input(
            "Clé API Groq",
            type="password",
            value=st.session_state.get('groq_api_key', ''),
            help="Obtenez votre clé gratuite sur console.groq.com"
        )
        
        if api_key:
            st.session_state.groq_api_key = api_key
            st.success("✅ API configurée")
            return api_key
        else:
            st.warning("⚠️ Clé API requise")
            st.markdown("[📖 Obtenir une clé gratuite](https://console.groq.com)")
            return None

def create_download_button(content: str, filename: str, label: str, mime_type: str = "text/plain"):
    """
    Crée un bouton de téléchargement stylisé
    """
    st.download_button(
        label=f"📥 {label}",
        data=content,
        file_name=filename,
        mime=mime_type,
        use_container_width=True
    )