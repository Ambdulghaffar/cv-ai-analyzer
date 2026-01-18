"""
Interface Mode Candidat
"""
import streamlit as st
from src.pdf_processor import PDFProcessor
from src.ai_analyzer import CVAnalyzer
from ui.components import (
    display_score_gauge,
    display_skills_comparison,
    display_section_scores,
    display_points_list,
    create_download_button,
    display_analysis_card
)
from utils.helpers import save_analysis_history

def render_candidate_mode():
    """Interface principale du mode candidat"""
    
    st.title("👤 Mode Candidat")
    st.markdown("Analysez votre CV par rapport à une offre d'emploi et obtenez des recommandations personnalisées.")
    
    st.markdown("---")
    
    # Vérifier la clé API
    if 'groq_api_key' not in st.session_state or not st.session_state.groq_api_key:
        st.error("⚠️ Veuillez configurer votre clé API Groq dans la barre latérale")
        return
    
    # Zone d'upload et saisie
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📄 Votre CV")
        uploaded_cv = st.file_uploader(
            "Uploadez votre CV (PDF)",
            type=['pdf'],
            help="Format PDF uniquement, max 10 MB"
        )
        
        if uploaded_cv:
            st.success(f"✅ Fichier chargé: {uploaded_cv.name}")
            
            # Informations sur le PDF
            pdf_info = PDFProcessor.get_pdf_info(uploaded_cv)
            st.caption(f"📊 {pdf_info.get('num_pages', 0)} page(s)")
    
    with col2:
        st.markdown("### 💼 Offre d'Emploi")
        job_offer = st.text_area(
            "Collez l'offre d'emploi complète",
            height=200,
            placeholder="Copiez-collez ici le texte de l'offre d'emploi (titre, description, compétences requises, etc.)"
        )
    
    st.markdown("---")
    
    # Bouton d'analyse
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        analyze_button = st.button(
            "🔍 Analyser le Matching",
            use_container_width=True,
            type="primary",
            disabled=not (uploaded_cv and job_offer)
        )
    
    if analyze_button:
        with st.spinner("🤖 Analyse en cours... Cela peut prendre 10-20 secondes"):
            try:
                # Extraction du texte
                cv_text = PDFProcessor.extract_text(uploaded_cv)
                
                if not cv_text or len(cv_text) < 100:
                    st.error("❌ Le CV semble vide ou illisible. Vérifiez le fichier.")
                    return
                
                # Initialiser l'analyseur
                analyzer = CVAnalyzer(api_key=st.session_state.groq_api_key)
                
                # Analyse principale
                analysis = analyzer.analyze_cv_matching(cv_text, job_offer)
                
                # Sauvegarder dans la session
                st.session_state.current_analysis = analysis
                st.session_state.current_cv_text = cv_text
                st.session_state.current_job_offer = job_offer
                
                # Sauvegarder dans l'historique
                save_analysis_history({
                    'type': 'candidat',
                    'cv_name': uploaded_cv.name,
                    'score': analysis.get('score_global', 0),
                    'analysis': analysis
                })
                
                st.success("✅ Analyse terminée !")
                
            except Exception as e:
                st.error(f"❌ Erreur lors de l'analyse: {str(e)}")
                return
    
    # Affichage des résultats
    if 'current_analysis' in st.session_state:
        analysis = st.session_state.current_analysis
        
        st.markdown("---")
        st.markdown("## 📊 Résultats de l'Analyse")
        
        # Score global
        display_score_gauge(analysis.get('score_global', 0))
        
        st.markdown("---")
        
        # Scores détaillés
        col1, col2 = st.columns([1, 1])
        
        with col1:
            display_section_scores(analysis)
        
        with col2:
            st.markdown("### 📈 Détails par Section")
            
            # Expérience
            exp = analysis.get('experience', {})
            st.metric(
                "Années d'expérience",
                f"{exp.get('annees_experience', 0)} ans",
                delta=None
            )
            st.caption(exp.get('pertinence', ''))
            
            st.markdown("---")
            
            # Formation
            formation = analysis.get('formation', {})
            st.metric("Niveau de formation", formation.get('niveau', 'N/A'))
            st.caption(formation.get('adequation', ''))
        
        st.markdown("---")
        
        # Compétences
        st.markdown("## 🎯 Compétences Techniques")
        comp_tech = analysis.get('competences_techniques', {})
        display_skills_comparison(
            comp_tech.get('presentes', []),
            comp_tech.get('manquantes', [])
        )
        
        st.markdown("---")
        
        # Soft Skills
        st.markdown("## 💡 Soft Skills")
        col1, col2 = st.columns(2)
        
        soft = analysis.get('soft_skills', {})
        with col1:
            st.markdown("**✅ Identifiées**")
            for skill in soft.get('identifies', []):
                st.markdown(f"- {skill}")
        
        with col2:
            st.markdown("**📝 À mettre en avant**")
            for skill in soft.get('manquantes', []):
                st.markdown(f"- {skill}")
        
        st.markdown("---")
        
        # Points forts et amélioration
        col1, col2 = st.columns(2)
        
        with col1:
            display_points_list(
                analysis.get('points_forts', []),
                "Points Forts",
                "💪",
                "#e8f5e9"
            )
        
        with col2:
            display_points_list(
                analysis.get('points_amelioration', []),
                "Points d'Amélioration",
                "🎯",
                "#fff3e0"
            )
        
        st.markdown("---")
        
        # Synthèse
        display_analysis_card(
            "Synthèse Globale",
            analysis.get('synthese', ''),
            "📝"
        )
        
        st.markdown("---")
        
        # Options supplémentaires
        st.markdown("## 🚀 Aller plus loin")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✍️ Générer une Lettre de Motivation", use_container_width=True):
                with st.spinner("Génération de la lettre..."):
                    try:
                        analyzer = CVAnalyzer(api_key=st.session_state.groq_api_key)
                        cover_letter = analyzer.generate_cover_letter(
                            st.session_state.current_cv_text,
                            st.session_state.current_job_offer,
                            analysis
                        )
                        
                        st.session_state.cover_letter = cover_letter
                        st.success("✅ Lettre générée !")
                    except Exception as e:
                        st.error(f"Erreur: {str(e)}")
        
        with col2:
            if st.button("💡 Obtenir des Suggestions d'Amélioration", use_container_width=True):
                with st.spinner("Génération des suggestions..."):
                    try:
                        analyzer = CVAnalyzer(api_key=st.session_state.groq_api_key)
                        suggestions = analyzer.generate_improvement_suggestions(
                            st.session_state.current_cv_text,
                            st.session_state.current_job_offer,
                            analysis
                        )
                        
                        st.session_state.suggestions = suggestions
                        st.success("✅ Suggestions générées !")
                    except Exception as e:
                        st.error(f"Erreur: {str(e)}")
        
        # Afficher la lettre si générée
        if 'cover_letter' in st.session_state:
            st.markdown("---")
            st.markdown("### ✍️ Lettre de Motivation")
            st.text_area(
                "Votre lettre personnalisée",
                st.session_state.cover_letter,
                height=400
            )
            
            create_download_button(
                st.session_state.cover_letter,
                "lettre_motivation.txt",
                "Télécharger la lettre"
            )
        
        # Afficher les suggestions si générées
        if 'suggestions' in st.session_state:
            st.markdown("---")
            st.markdown("### 💡 Suggestions d'Amélioration")
            
            for i, suggestion in enumerate(st.session_state.suggestions, 1):
                st.markdown(f"""
                <div style="
                    background-color: #e3f2fd;
                    padding: 15px;
                    border-radius: 8px;
                    margin: 10px 0;
                    border-left: 4px solid #2196f3;
                ">
                    <strong>Suggestion {i}:</strong> {suggestion}
                </div>
                """, unsafe_allow_html=True)